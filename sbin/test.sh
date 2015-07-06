#!/bin/bash
# test.sh
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details

source $(dirname "${BASH_SOURCE[0]}")/functions.sh

print_usage_message () {
	echo -e "test.sh\n" >&2
	echo -e "Usage:" >&2
	echo -e "  test.sh -h" >&2
	echo -e "  test.sh -d [-e env] [-n num-cpus]" >&2
	echo -e "  test.sh -c [-e env] [-n num-cpus] [module-name]" >&2
	echo -e "  test.sh [-e env] [-n num-cpus] [module-name]"\
	        "[test-name]\n" >&2
	echo -e "Options:" >&2
	echo -e "  -h  Show this screen" >&2
	echo -e "  -c  Measure test coverage" >&2
	echo -e "  -d  Verify doctests" >&2
	echo -e "  -e  Interpreter version [default: PY27|py34]" >&2
	echo -e "  -n  Number of CPUs to use [default: 1]" >&2
	echo -e "" >&2
	echo -e "If no module name is given all package modules" \
		"are processed" >&2
}

pkg_dir=$(dirname $(current_dir "${BASH_SOURCE[0]}"))
src_dir=${pkg_dir}/putil
cpwd=${PWD}

source ${pkg_dir}/sbin/functions.sh

# Read command line options
num_cpus=""
coverage=0
doctest=0
interp=""
while getopts ":hcde:n:" opt; do
	case ${opt} in
		h)
			print_usage_message
			exit 0
			;;
		c)
			coverage=1
			;;
		d)
			doctest=1
			;;
		e)
			interp=${OPTARG}
			;;
		n)
			num_cpus=${OPTARG}
			;;
		\?)
			echo "test.sh: invalid option" >&2
			print_usage_message
			exit 1
			;;
	esac
done
shift $((${OPTIND} - 1))
if [ "${coverage}" == 1 ] && [ "${doctest}" == 1 ]; then
	echo "test.sh: coverage and doctests cannot be measured simultaneously"
	exit 1
fi
if [ "${doctest}" == 1 ] && [ "$#" -gt 0 ]; then
	echo "test.sh: too many command line arguments" >&2
	exit 1
fi
if [ "${coverage}" == 0 ] && [ "$#" -gt 2 ]; then
	echo "test.sh: too many command line arguments" >&2
	exit 1
fi
if [ "${coverage}" == 1 ] && [ "$#" -gt 1 ]; then
	echo "test.sh: too many command line arguments" >&2
	exit 1
fi


# Argument validation
module=""
if [ "$#" -gt 0 ]; then
	module=$1
	file=${pkg_dir}/tests/test_${module}.py
	if [ ! -f "${file}" ]; then
		echo "test.sh: test bench for module ${module}"\
		     "could not be found"
		exit 1
	fi
	fmodule="test_${module}.py"
fi

kopt=""
if [ "$#" == 2 ]; then
	kopt="-k $2"
fi

nopt=$(validate_num_cpus "test.sh" "${num_cpus}")
if [ $? != 0 ]; then
	exit 1
fi

fmodules=""
if [ "${fmodule}" == "" ] && [ "${doctest}" == 0 ] && [ "${coverage}" == 0 ]
then
	modules=(
		eng
		exdoc
		exh
		misc
		pcontracts
		pcsv
		pinspect
		plot
		ptypes
		"test"
		tree
	)
	for module in ${modules[@]}; do
		fmodules+="test_${module}.py "
	done
elif [ "${fmodule}" != "" ]; then
	fmodules=(${fmodule})
fi

interp=${interp,,}
if [ "${interp}" != "py27" ] && [ "${interp}" != "py34" ] && [ "${interp}" != "" ]; then
	echo "test.sh: invalid interpreter version" >&2
fi
if [ "${interp}" == "py27" ]; then
	print_green_line "Python 2.7 tests"
	interps=(py27)
elif [ "${interp}" == "py34" ]; then
	print_green_line  "Python 3.4 tests"
	interps=(py34)
else
	print_green_line "Python 2.7 and 3.4 tests"
	interps=(py27 py34)
fi


cd ${pkg_dir}

for interp in ${interps[@]}; do
	if [ "${interp}" == "py27" ]; then
		tox_pkg_dir=".tox/py27/lib/python2.7/site-packages/putil/"
		docs_dir="${pkg_dir}/.tox/py27/usr/share/putil/docs"
		eopt="-e py27"
	elif [ "${interp}" == "py34" ]; then
		tox_pkg_dir=".tox/py34/lib/python3.4/site-packages/putil/"
		docs_dir="${pkg_dir}/.tox/py34/usr/share/putil/docs"
		eopt="-e py34"
	fi
	coverage_file=".coveragerc_tox_${interp}"
	popts=""
	if [ "${doctest}" == 1 ]; then
		print_banner "Doctests"
		# Run doctests in Sphinx files
		popts="
			--doctest-glob='*.rst'
			${docs_dir}
		"
		tox ${eopt} -- ${nopt} ${kopt} ${popts}
		# Run embedded doctests in Python modules
		ecode=$?
		if [ "${ecode}" == 0 ]; then
			popts="
				--doctest-modules
				${pkg_dir}/${tox_pkg_dir}
			"
			tox ${eopt} -- ${nopt} ${kopt} ${popts}
		fi
	elif [ "${coverage}" == 0 ]; then
		print_banner "Unit tests"
		popts="-x -s -vv"
		for fmodule in ${fmodules[@]}; do
			tox ${eopt} -- ${nopt} ${kopt} ${popts} ${fmodule}
			if [ "$?" != 0 ]; then
				break
			fi
		done
	else
		print_banner "Coverage"
		rtype="term"
		if [ "${fmodules}" != "" ]; then
			popts="
				-x -s -vv --cov-config ${pkg_dir}/${coverage_file}
				--cov ${pkg_dir}/${tox_pkg_dir} --cov-report html
			"
			for fmodule in ${fmodules[@]}; do
				tox ${eopt} -- ${nopt} ${kopt} ${popts} ${fmodule}
				if [ "$?" != 0 ]; then
					break
				fi

			done
		else
			popts="
				--cov-config ${pkg_dir}/${coverage_file}
				--cov ${pkg_dir}/${tox_pkg_dir} --cov-report term
			"
			tox ${eopt} -- ${nopt} ${kopt} ${popts}
		fi
	fi
	ecode=$?
	cd ${cpwd}
	if [ "${ecode}" != 0 ]; then
		exit 1
	fi
done
