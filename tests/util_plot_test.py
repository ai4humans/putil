"""
util_plot unit tests
"""

import numpy
import pytest

import util_plot

###
# Reusable tests
###
def indep_min_max_type(func, param):
	""" Tests indep_min and indep_max type validation """
	comp = list()
	# __init__ path
	# Wrong types
	for param_value in ['a', False]:
		with pytest.raises(TypeError) as excinfo:
			func(**{param:param_value})	#pylint: disable=W0142
		comp.append(excinfo.value.message == 'Parameter `{0}` is of the wrong type'.format(param))
	# Valid values, these should not raise an exception
	for param_value in [None, 1, 2.0]:
		kwarg = {param:param_value}	#pylint: disable=W0612
		exec('comp.append(func(**kwarg).{0} == {1})'.format(param, param_value))	#pylint: disable=W0142,W0122
	# Managed attribute path
	# Wrong types
	obj = func()	#pylint: disable=W0612
	for param_value in ['a', False]:
		with pytest.raises(TypeError) as excinfo:
			exec("obj.{0} = {1}".format(param, "'{0}'".format(param_value) if isinstance(param_value, str) else param_value))	#pylint: disable=W0122
		comp.append(excinfo.value.message == 'Parameter `{0}` is of the wrong type'.format(param))
	# Valid values, these should not raise an exception
	for param_value in [None, 1, 2.0]:
		exec('obj.{0} = {1}'.format(param, param_value))	#pylint: disable=W0122
		exec('comp.append(obj.{0} == {1})'.format(param, param_value))	#pylint: disable=W0122
	assert comp == 10*[True]

def indep_min_greater_than_indep_max(func):	#pylint: disable=C0103
	""" Test if object behaves correctly when indep_min and indep_max are incongrous """
	comp = list()
	# Assign indep_min first
	obj = func(indep_min=45)
	with pytest.raises(ValueError) as excinfo:
		obj.indep_max = 0
	comp.append(excinfo.value.message == 'Parameter `indep_min` is greater than parameter `indep_max`')
	# Assign indep_max first
	obj = func()
	obj.indep_max = 40
	with pytest.raises(ValueError) as excinfo:
		obj.indep_min = 50
	comp.append(excinfo.value.message == 'Parameter `indep_min` is greater than parameter `indep_max`')
	assert comp == 2*[True]

###
# Tests for BasicSource
###
def test_basic_source_indep_min_type():	#pylint: disable=C0103
	""" Tests indep_min type validation """
	indep_min_max_type(util_plot.BasicSource, 'indep_min')

def test_basic_source_indep_max_type():	#pylint: disable=C0103
	""" Tests indep_max type validation """
	indep_min_max_type(util_plot.BasicSource, 'indep_max')

def test_basic_source_indep_min_greater_than_indep_max():	#pylint: disable=C0103
	""" Test if object behaves correctly when indep_min and indep_max are incongrous """
	indep_min_greater_than_indep_max(util_plot.BasicSource)

def test_basic_source_indep_var_type():	#pylint: disable=C0103
	""" Tests indep_var type validation """
	comp = list()
	# __init__ path
	# Wrong type
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(indep_var='a')
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	# Non monotonically increasing vector
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(indep_var=numpy.array([1.0, 2.0, 0.0, 3.0]))
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	# Empty vector
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(indep_var=numpy.array([]))
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	# Valid values, these should not raise any exception
	comp.append(util_plot.BasicSource(indep_var=None).indep_var == None)
	comp.append((util_plot.BasicSource(indep_var=numpy.array([1, 2, 3])).indep_var == numpy.array([1, 2, 3])).all())
	comp.append((util_plot.BasicSource(indep_var=numpy.array([4.0, 5.0, 6.0])).indep_var == numpy.array([4.0, 5.0, 6.0])).all())
	# Invalid thresholding
	# Assign indep_min via __init__ path
	obj = util_plot.BasicSource(indep_min=45)
	with pytest.raises(ValueError) as excinfo:
		obj.indep_var = numpy.array([1, 2, 3])
	comp.append(excinfo.value.message == 'Parameter `indep_var` is empty after `indep_min`/`indep_max` thresholding')
	# Assign indep_min via attribute
	obj = util_plot.BasicSource(indep_var=numpy.array([1, 2, 3]))
	with pytest.raises(ValueError) as excinfo:
		obj.indep_min = 10
	comp.append(excinfo.value.message == 'Parameter `indep_var` is empty after `indep_min`/`indep_max` thresholding')
	# Assign indep_max via attribute
	obj = util_plot.BasicSource(indep_max=0)
	with pytest.raises(ValueError) as excinfo:
		obj.indep_var = numpy.array([1, 2, 3])
	comp.append(excinfo.value.message == 'Parameter `indep_var` is empty after `indep_min`/`indep_max` thresholding')
	# Assign indep_max via attribute
	obj = util_plot.BasicSource(indep_var=numpy.array([1, 2, 3]))
	with pytest.raises(ValueError) as excinfo:
		obj.indep_max = 0
	comp.append(excinfo.value.message == 'Parameter `indep_var` is empty after `indep_min`/`indep_max` thresholding')
	# Assign both indep_min and indep_max via __init__ path
	with pytest.raises(ValueError) as excinfo:
		util_plot.BasicSource(indep_var=numpy.array([1, 2, 3]), indep_min=4, indep_max=10)
	comp.append(excinfo.value.message == 'Parameter `indep_var` is empty after `indep_min`/`indep_max` thresholding')
	# Managed attribute path
	obj = util_plot.BasicSource()
	# Wrong type
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(indep_var='a')
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	# Non monotonically increasing vector
	with pytest.raises(TypeError) as excinfo:
		obj.indep_var = numpy.array([1.0, 2.0, 0.0, 3.0])
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	# Empty vector
	with pytest.raises(TypeError) as excinfo:
		obj.indep_var = numpy.array([])
	comp.append(excinfo.value.message == 'Parameter `indep_var` is of the wrong type')
	obj.indep_var = None
	comp.append(obj.indep_var == None)
	obj.indep_var = numpy.array([1, 2, 3])
	comp.append((obj.indep_var == numpy.array([1, 2, 3])).all())
	obj.indep_var = numpy.array([4.0, 5.0, 6.0])
	comp.append((obj.indep_var == numpy.array([4.0, 5.0, 6.0])).all())
	assert comp == 17*[True]

def test_basic_source_dep_var_type():	#pylint: disable=C0103
	""" Tests dep_var type validation """
	comp = list()
	# __init__ path
	# Wrong type
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(dep_var='a')
	comp.append(excinfo.value.message == 'Parameter `dep_var` is of the wrong type')
	# Empty vector
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(dep_var=numpy.array([]))
	comp.append(excinfo.value.message == 'Parameter `dep_var` is of the wrong type')
	# Valid values, these should not raise any exception
	comp.append(util_plot.BasicSource(dep_var=None).dep_var == None)
	comp.append((util_plot.BasicSource(dep_var=numpy.array([1, 2, 3])).dep_var == numpy.array([1, 2, 3])).all())
	comp.append((util_plot.BasicSource(dep_var=numpy.array([4.0, 5.0, 6.0])).dep_var == numpy.array([4.0, 5.0, 6.0])).all())
	# Managed attribute path
	obj = util_plot.BasicSource()
	# Wrong type
	with pytest.raises(TypeError) as excinfo:
		util_plot.BasicSource(dep_var='a')
	comp.append(excinfo.value.message == 'Parameter `dep_var` is of the wrong type')
	# Empty vector
	with pytest.raises(TypeError) as excinfo:
		obj.dep_var = numpy.array([])
	comp.append(excinfo.value.message == 'Parameter `dep_var` is of the wrong type')
	obj.dep_var = None
	comp.append(obj.dep_var == None)
	obj.dep_var = numpy.array([1, 2, 3])
	comp.append((obj.dep_var == numpy.array([1, 2, 3])).all())
	obj.dep_var = numpy.array([4.0, 5.0, 6.0])
	comp.append((obj.dep_var == numpy.array([4.0, 5.0, 6.0])).all())
	assert comp == 10*[True]

def test_basic_source_indep_var_and_dep_var_do_not_have_the_same_number_of_elements():	#pylint: disable=C0103
	""" Tests dep_var type validation """
	comp = list()
	# indep_var set first
	obj = util_plot.BasicSource(indep_var=numpy.array([10, 20, 30, 40, 50, 60]), indep_min=30, indep_max=50)
	with pytest.raises(ValueError) as excinfo:
		obj.dep_var = numpy.array([100, 200, 300])
	comp.append(excinfo.value.message == 'Parameters `indep_var` and `dep_var` must have the same number of elements')
	# dep_var set first
	obj = util_plot.BasicSource(dep_var=numpy.array([100, 200, 300]), indep_min=30, indep_max=50)
	with pytest.raises(ValueError) as excinfo:
		obj.indep_var = numpy.array([10, 20, 30, 40, 50, 60])
	comp.append(excinfo.value.message == 'Parameters `indep_var` and `dep_var` must have the same number of elements')
	assert comp == 2*[True]

def test_basic_source_complete():	#pylint: disable=C0103
	""" Test that _complete() method behaves correctly """
	comp = list()
	obj = util_plot.BasicSource(indep_min=0, indep_max=50)
	comp.append(obj._complete() == False)	#pylint: disable=W0212
	obj.indep_var = numpy.array([1, 2, 3])
	comp.append(obj._complete() == False)	#pylint: disable=W0212
	obj.indep_var = numpy.array([10, 20, 30])
	comp.append(obj._complete() == False)	#pylint: disable=W0212
	assert comp == 3*[True]

def test_basic_source_str():	#pylint: disable=C0103
	""" Test that str behaves correctly """
	comp = list()
	# Null object
	obj = str(util_plot.BasicSource())
	ref = 'Independent variable minimum: -inf\nIndependent variable maximum: +inf\nIndependent variable: None\nDependent variable: None'
	comp.append(obj == ref)
	# indep_min set
	obj = str(util_plot.BasicSource(indep_min=10))
	ref = 'Independent variable minimum: 10\nIndependent variable maximum: +inf\nIndependent variable: None\nDependent variable: None'
	comp.append(obj == ref)
	# indep_max set
	obj = str(util_plot.BasicSource(indep_min=10, indep_max=20))
	ref = 'Independent variable minimum: 10\nIndependent variable maximum: 20\nIndependent variable: None\nDependent variable: None'
	comp.append(obj == ref)
	# indep_var set
	obj = str(util_plot.BasicSource(indep_var=numpy.array([1, 2, 3]), indep_min=-10, indep_max=20.0))
	ref = 'Independent variable minimum: -10\nIndependent variable maximum: 20.0\nIndependent variable: [ 1.0, 2.0, 3.0 ]\nDependent variable: None'
	comp.append(obj == ref)
	# dep_var set
	obj = str(util_plot.BasicSource(indep_var=numpy.array([1, 2, 3]), dep_var=numpy.array([10, 20, 30]), indep_min=-10, indep_max=20.0))
	ref = 'Independent variable minimum: -10\nIndependent variable maximum: 20.0\nIndependent variable: [ 1.0, 2.0, 3.0 ]\nDependent variable: [ 10.0, 20.0, 30.0 ]'
	comp.append(obj == ref)
	assert comp == 5*[True]

def test_basic_source_cannot_delete_attributes():	#pylint: disable=C0103
	""" Test that del method raises an exception on all class attributes """
	obj = util_plot.BasicSource()
	test_list = list()
	with pytest.raises(AttributeError) as excinfo:
		del obj.indep_min
	test_list.append(excinfo.value.message == "can't delete attribute")
	with pytest.raises(AttributeError) as excinfo:
		del obj.indep_max
	test_list.append(excinfo.value.message == "can't delete attribute")
	with pytest.raises(AttributeError) as excinfo:
		del obj.indep_var
	test_list.append(excinfo.value.message == "can't delete attribute")
	with pytest.raises(AttributeError) as excinfo:
		del obj.dep_var
	test_list.append(excinfo.value.message == "can't delete attribute")
	assert test_list == 4*[True]

###
# Tests for CsvSource
###

@pytest.fixture
def tmp_csv_file(tmpdir):
	""" Fixture to create temporary CSV file for testing purposes """
	file_handle = tmpdir.mkdir('sub').join('tmp.csv')
	file_handle.write('Col1,Col2,Col3,Col4,Col5,Col6\n', mode='w')
	file_handle.write('0,1,2,3,,5\n', mode='a')
	file_handle.write('0,2,4,5,,4\n', mode='a')
	file_handle.write('0,3,1,8,,3\n', mode='a')
	file_handle.write('1,1,5,7,8,0\n', mode='a')
	file_handle.write('1,2,3,7,9,7\n', mode='a')
	return True

def test_csv_source_indep_min_type():	#pylint: disable=C0103
	""" Tests indep_min type validation """
	indep_min_max_type(util_plot.CsvSource, 'indep_min')

def test_csv_source_indep_max_type():	#pylint: disable=C0103
	""" Tests indep_max type validation """
	indep_min_max_type(util_plot.CsvSource, 'indep_max')

def test_csv_source_indep_min_greater_than_indep_max():	#pylint: disable=C0103
	""" Test if object behaves correctly when indep_min and indep_max are incongrous """
	indep_min_greater_than_indep_max(util_plot.CsvSource)

def test_csv_source_file_name_wrong_type():	#pylint: disable=C0103
	""" Test if object behaves correctly when file_name is of the wrong type """
	# This assignment should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(file_name=5)
	comp = excinfo.value.message == 'Parameter `file_name` is of the wrong type'
	# This assignment should not raise an exception
	util_plot.CsvSource(file_name=None)
	assert comp == True

def test_csv_source_file_does_not_exist():	#pylint: disable=C0103
	""" Test if object behaves correctly when CSV file does not exist """
	file_name = 'nonexistent_file_name.csv'
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name)
	assert excinfo.value.message == 'File {0} could not be found'.format(file_name)

def test_csv_source_file_exist(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when CSV file exists """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	util_plot.CsvSource(file_name=file_name)

def test_csv_source_data_filter_wrong_type():	#pylint: disable=C0103
	""" Test if object behaves correctly when dfilter is of the wrong type """
	# This assignment should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(dfilter=5)
	comp = excinfo.value.message == 'Parameter `dfilter` is of the wrong type'
	# This assignment should not raise an exception
	util_plot.CsvSource(dfilter=None)
	assert comp == True

def test_csv_source_data_filter_operation(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when data filter and file name are given """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	# This assignment should raise an exeption
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, dfilter={'Col99':500})
	comp = excinfo.value.message == 'Column COL99 in data filter not found in comma-separated file {0} header'.format(file_name)
	util_plot.CsvSource(file_name=file_name, dfilter={'Col1':0})
	assert comp == True

def test_csv_source_indep_col_label_wrong_type(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when indep_col_label is of the wrong type """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	comp_list = list()
	# These assignments should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(indep_col_label=5)
	comp_list.append(excinfo.value.message == 'Parameter `indep_col_label` is of the wrong type')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col99')
	comp_list.append(excinfo.value.message == 'Column COL99 (independent column label) could not be found in comma-separated file {0} header'.format(file_name))
	# These assignments should not raise an exception
	util_plot.CsvSource(indep_col_label=None)
	util_plot.CsvSource(file_name=file_name, dfilter={'Col1':0}, indep_col_label='Col2')
	assert comp_list == [True, True]

def test_csv_source_dep_col_label_wrong_type(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when dep_col_label is of the wrong type """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	comp_list = list()
	# This assignment should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(dep_col_label=5)
	comp_list.append(excinfo.value.message == 'Parameter `dep_col_label` is of the wrong type')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, dep_col_label='Col99')
	comp_list.append(excinfo.value.message == 'Column COL99 (dependent column label) could not be found in comma-separated file {0} header'.format(file_name))	# Thess assignments should not raise an exception
	# These assignments should not raise an exception
	util_plot.CsvSource(dep_col_label=None)
	util_plot.CsvSource(file_name=file_name, dep_col_label='Col3')
	assert comp_list == [True, True]

def test_csv_source_empty_indep_var_after_filter(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when the independent variable is empty after data filter is applied """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':10})
	assert excinfo.value.message == 'Filtered independent variable is empty'

def test_csv_source_empty_dep_var_after_filter(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when the dependent variable is empty after data filter is applied """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col5', dfilter={'Col1':0})
	assert excinfo.value.message == 'Filtered dependent variable is empty'

def test_csv_source_data_reversed(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when the independent dat is descending order """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	obj = util_plot.CsvSource(file_name=file_name, indep_col_label='Col6', dep_col_label='Col3', dfilter={'Col1':0})
	assert ((obj.indep_var == numpy.array([3, 4, 5])).all(), (obj.dep_var == numpy.array([1, 4, 2])).all()) == (True, True)

def test_csv_source_fproc_wrong_type():	#pylint: disable=C0103
	""" Test if object behaves correctly when fproc is of the wrong type """
	def fproc1():	#pylint: disable=C0111
		return True
	def fproc2(*args):	#pylint: disable=C0111,W0613
		return True
	def fproc3(**kwargs):	#pylint: disable=C0111,W0613
		return True
	def fproc4(*args, **kwargs):	#pylint: disable=C0111,W0613
		return True
	comp_list = list()
	# These assignments should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(fproc=5)
	comp_list.append(excinfo.value.message == 'Parameter `fproc` is of the wrong type')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(fproc=fproc1)
	comp_list.append(excinfo.value.message == 'Parameter `fproc` (function fproc1) does not have at least 2 arguments')
	# These assignments should not raise an exception
	util_plot.CsvSource(fproc=fproc2)
	util_plot.CsvSource(fproc=fproc3)
	util_plot.CsvSource(fproc=fproc4)
	assert comp_list == [True]*2

def test_csv_source_fproc_wrong_return(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103,R0912,R0914
	""" Test if object behaves correctly when fproc returns the wrong type and/or number of parameters """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	def fproc1(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return True
	def fproc2(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 2])]
	def fproc3(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 2]), numpy.array([1, 2])]
	def fproc4(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [5, numpy.array([1, 2])]
	def fproc5(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([3, 2, 1]), numpy.array([1, 2, 3])]
	def fproc6(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 2]), 6]
	def fproc7(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 2]), numpy.array([3, 1])]
	def fproc8(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([]), numpy.array([3, 1])]
	def fproc9(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 3]), numpy.array([])]
	def fproc10(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([None, None]), numpy.array([3, 1])]
	def fproc11(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 3]), numpy.array([None, None])]
	def fproc12(indep_var, dep_var):	#pylint: disable=C0111,W0613
		return [numpy.array([1, 3]), numpy.array([1, 2, 3])]
	def fproc13(indep_var, dep_var, par1):	#pylint: disable=C0111,W0613
		raise RuntimeError('Test exception message')
	comp_list = list()
	# These assignments should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc1)
	comp_list.append(excinfo.value.message == 'Parameter `fproc` (function fproc1) return value is of the wrong type')
	with pytest.raises(RuntimeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc2)
	comp_list.append(excinfo.value.message == 'Parameter `fproc` (function fproc2) returned an illegal number of values')
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc4)
	comp_list.append(excinfo.value.message == 'Processed independent variable is of the wrong type')
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc5)
	comp_list.append(excinfo.value.message == 'Processed independent variable is of the wrong type')
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc6)
	comp_list.append(excinfo.value.message == 'Processed dependent variable is of the wrong type')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc8)
	comp_list.append(excinfo.value.message == 'Processed independent variable is empty')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc9)
	comp_list.append(excinfo.value.message == 'Processed dependent variable is empty')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc10)
	comp_list.append(excinfo.value.message == 'Processed independent variable is empty')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc11)
	comp_list.append(excinfo.value.message == 'Processed dependent variable is empty')
	with pytest.raises(ValueError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc12)
	comp_list.append(excinfo.value.message == 'Processed independent and dependent variables are of different length')
	with pytest.raises(RuntimeError) as excinfo:
		util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc13, fproc_eargs={'par1':13})
	msg = 'Processing function fproc13 threw an exception when called with the following arguments:\n'
	msg += 'indep_var: [ 1.0, 2.0, 3.0 ]\n'
	msg += 'dep_var: [ 1.0, 2.0, 3.0 ]\n'
	msg += 'par1: 13\n'
	msg += 'Exception error: Test exception message'
	comp_list.append(excinfo.value.message == msg)
	# These assignments should not raise an exception
	util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc3)
	util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc7)
	assert comp_list == [True]*11

def test_csv_source_fproc_eargs_wrong_type():	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when fprog_eargs is of the wrong type """
	# This assignment should raise an exeption
	with pytest.raises(TypeError) as excinfo:
		util_plot.CsvSource(fproc_eargs=5)
	comp = excinfo.value.message == 'Parameter `fproc_eargs` is of the wrong type'
	# These assignments should not raise an exception
	util_plot.CsvSource(fproc_eargs=None)
	util_plot.CsvSource(fproc_eargs={'arg1':23})
	assert comp == True

def test_csv_source_fproc_eargs_parameter_name_validation():	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when checking if the arguments in the fprog_eargs dictionary exist """
	def fproc1(indep_var, dep_var):	#pylint: disable=C0111,W0613
		pass
	def fproc2(indep_var, dep_var, par1, par2):	#pylint: disable=C0111,W0613
		pass
	def fproc3(indep_var, dep_var, par3, par4, *args):	#pylint: disable=C0111,W0613
		pass
	def fproc4(indep_var, dep_var, par5, par6, **kwargs):	#pylint: disable=C0111,W0613
		pass
	def fproc5(indep_var, dep_var, par7, par8, *args, **kwargs):	#pylint: disable=C0111,W0613
		pass
	comp_list = list()
	# These assignments should raise an exeption
	with pytest.raises(RuntimeError) as excinfo:
		util_plot.CsvSource(fproc=fproc1, fproc_eargs={'par1':5})
	comp_list.append(excinfo.value.message == 'Extra argument `par1` not found in parameter `fproc` (function fproc1) definition')
	with pytest.raises(RuntimeError) as excinfo:
		util_plot.CsvSource(fproc=fproc2, fproc_eargs={'par3':5})
	comp_list.append(excinfo.value.message == 'Extra argument `par3` not found in parameter `fproc` (function fproc2) definition')
	# These assignments should not raise an exception
	util_plot.CsvSource(fproc=fproc3, fproc_eargs={'par99':5})
	util_plot.CsvSource(fproc=fproc4, fproc_eargs={'par98':5})
	util_plot.CsvSource(fproc=fproc5, fproc_eargs={'par97':5})
	assert comp_list == [True]*2

def test_fproc_works(tmpdir, tmp_csv_file):	#pylint: disable=W0621,W0613,C0103
	""" Test if object behaves correctly when executing function defined in fproc parameter with extra arguments defined in fproc_eargs parameter """
	file_name = str(tmpdir.join('sub/tmp.csv'))
	def fproc1(indep_var, dep_var, indep_offset, dep_offset):	#pylint: disable=C0111,W0613
		return indep_var+indep_offset, dep_var+dep_offset
	obj = util_plot.CsvSource(file_name=file_name, indep_col_label='Col2', dep_col_label='Col3', dfilter={'Col1':0}, fproc=fproc1, fproc_eargs={'indep_offset':3, 'dep_offset':100})
	print obj.indep_var
	print obj.dep_var
	assert [(obj.indep_var == numpy.array([4, 5, 6])).all(), (obj.dep_var == numpy.array([102, 104, 101])).all()] == [True]*2

