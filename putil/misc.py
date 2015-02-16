﻿# misc.py
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111

import os
import sys
import time
import numpy
import types
import decimal
import inspect
import textwrap
import tempfile
import decorator
import fractions


###
# Context managers
###
@decorator.contextmanager
def ignored(*exceptions):
	"""
	Context manager to execute commands and selectively ignore exceptions (from "Transforming Code into Beautiful, Idiomatic Python" talk at PyCon US 2013 by Raymond Hettinger)

	:param	exceptions: Exception types to ignore
	:type	exceptions: Exception object, i.e. RuntimeError, IOError, etc.

	For example::

		with ignored(OSError):
			os.remove('somefile.tmp')
	"""
	try:
		yield
	except exceptions:
		pass


class TmpFile(object):	#pylint: disable=R0903
	"""
	Context manager for temporary files.

	:param	fpointer: Pointer to a function that writes data to file or *None*. If the argument is not *None* the function pointed to receives exactly one argument, a file-like object as created by the\
	`tempfile.NamedTemporaryFile <https://docs.python.org/2/library/tempfile.html#tempfile.NamedTemporaryFile>`_ function.
	:type	fpointer: function pointer
	:returns:	File name of temporary file
	:raises:	TypeError (Argument `fpointer` is not valid)
	"""
	def __init__(self, fpointer=None):
		if fpointer and (not isinstance(fpointer, types.FunctionType)) and (not isinstance(fpointer, types.LambdaType)):
			raise TypeError('Argument `fpointer` is not valid')
		self._file_name = None
		self._fpointer = fpointer

	def __enter__(self):
		with tempfile.NamedTemporaryFile(delete=False) as fobj:
			self._file_name = fobj.name
			if self._fpointer:
				self._fpointer(fobj)
		return self._file_name

	def __exit__(self, exc_type, exc_value, exc_tb):
		with ignored(OSError):
			os.remove(self._file_name)
		if exc_type is not None:
			return False


class Timer(object):	#pylint: disable=R0903
	"""
	Context manager for profiling blocks of code by calculating elapsed time between context manager enter and exit time points. Largely from `Huy Nguyen blog <http://www.huyng.com/posts/python-performance-analysis/>`_

	:param	verbose: print elapsed time upon exit
	:type	verbose: boolean
	:returns: :py:class:`putil.misc.Timer()` context manager object
	:raises: TypeError (Argument `verbose` is not valid)
	"""
	def __init__(self, verbose=False):
		if not isinstance(verbose, bool):
			raise TypeError('Argument `verbose` is not valid')
		self._start_time, self._stop_time, self._elapsed_time, self._verbose = None, None, None, verbose

	def __enter__(self):
		self._start_time = time.time()
		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		self._stop_time = time.time()
		self._elapsed_time = 1000.0*(self._stop_time-self._start_time)
		if self._verbose:
			print 'Elapsed time: {0}[msec]'.format(self._elapsed_time)
		if exc_type is not None:
			return False

	def _get_elapsed_time(self):
		return self._elapsed_time

	elapsed_time = property(_get_elapsed_time, None, None, doc='Elapsed time')
	"""
	Returns elapsed time between context manager enter and exit time points

	:rtype: float
	"""


def pcolor(text, color, tab=0):
	"""
	Returns a string that once printed is colorized

	:param	text: Text to colorize
	:type	text: string
	:param	color: Color to use, one of `['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'none'] (case insensitive)`
	:type	color: string
	:param	tab: Number of spaces to prefix **text** with
	:type	tab: integer
	:rtype:	string
	:raises:
	 * TypeError (Argument `color` is not valid)

	 * TypeError (Argument `tab` is not valid)

	 * TypeError (Argument `text` is not valid)

	 * ValueError (Unknown color *[color]*)
	"""
	esc_dict = {'black':30, 'red':31, 'green':32, 'yellow':33, 'blue':34, 'magenta':35, 'cyan':36, 'white':37, 'none':-1}
	if not isinstance(text, str):
		raise TypeError('Argument `text` is not valid')
	if not isinstance(color, str):
		raise TypeError('Argument `color` is not valid')
	if not isinstance(tab, int):
		raise TypeError('Argument `tab` is not valid')
	color = color.lower()
	if color not in esc_dict:
		raise ValueError('Unknown color {0}'.format(color))
	return '\033[{0}m{1}{2}\033[0m'.format(esc_dict[color], ' '*tab, text) if esc_dict[color] != -1 else '{0}{1}'.format(' '*tab, text)


def binary_string_to_octal_string(text):	#pylint: disable=C0103
	r"""
	Prints binary-packed string in octal representation aliasing typical codes to their escape sequences.

	:param	text: Text to convert
	:type	text: string
	:rtype: string

	+------+-------+-----------------+
	| Code | Alias |   Description   |
	+======+=======+=================+
	|    0 |   \\0 | Null character  |
	+------+-------+-----------------+
	|    7 |   \\a | Bell / alarm    |
	+------+-------+-----------------+
	|    8 |   \\b | Backspace       |
	+------+-------+-----------------+
	|    9 |   \\t | Horizontal tab  |
	+------+-------+-----------------+
	|   10 |   \\n | Line feed       |
	+------+-------+-----------------+
	|   11 |   \\v | Vertical tab    |
	+------+-------+-----------------+
	|   12 |   \\f | Form feed       |
	+------+-------+-----------------+
	|   13 |   \\r | Carriage return |
	+------+-------+-----------------+

	For example:

		>>> num = range(1, 15)
		>>> putil.misc.binary_string_to_octal_string(''.join([struct.pack('h', num) for num in nums]))
		'\\1\\0\\2\\0\\3\\0\\4\\0\\5\\0\\6\\0\\a\\0\\b\\0\\t\\0\\n\\0\\v\\0\\f\\0\\r\\0\\16\\0'

	"""
	octal_alphabet = [chr(num) if (num >= 32) and (num <= 126) else '\\'+str(oct(num)).lstrip('0') for num in xrange(0, 256)]
	octal_alphabet[0] = '\\0'	# Null character
	octal_alphabet[7] = '\\a'	# Bell/alarm
	octal_alphabet[8] = '\\b'	# Back space
	octal_alphabet[9] = '\\t'	# Horizontal tab
	octal_alphabet[10] = '\\n'	# Line feed
	octal_alphabet[11] = '\\v'	# Vertical tab
	octal_alphabet[12] = '\\f'	# Form feed
	octal_alphabet[13] = '\\r'	# Carriage return
	return ''.join([octal_alphabet[ord(char)] for char in text])


def char_to_decimal(text):
	"""
	Converts a string to its decimal ASCII representation, with spaces between characters

	:param	text: Text to convert
	:type	text: string
	:rtype: string

	For example:

		>>> putil.misc.char_to_decimal('Hello world!')
		'72 101 108 108 111 32 119 111 114 108 100 33'

	"""
	return ' '.join([str(ord(char)) for char in text])


def isnumber(arg):
	"""
	Checks if argument is a number: complex, float or integer

	:param	arg: Argument to check
	:type	arg: any
	:rtype: boolean
	"""
	return (arg is not None) and (not isinstance(arg, bool)) and (isinstance(arg, int) or isinstance(arg, float) or isinstance(arg, complex))


def isreal(arg):
	"""
	Checks if argument is a real number: float or integer

	:param	arg: Argument to check
	:type	arg: any
	:rtype: boolean
	"""
	return (arg is not None) and (not isinstance(arg, bool)) and (isinstance(arg, int) or isinstance(arg, float))


def per(arga, argb, prec=10):
	"""
	Calculates percentage difference between two numbers or the element-wise percentage difference between two list of numbers or Numpy vectors.
	If any of the numbers in the arguments **arga** or **argb** is zero the value returned is 1E+20

	:param	arga: First number, list of numbers or Numpy vector
	:type	arga: float, integer, list of floats or integers, or Numpy vector of floats or integers
	:param	argb: Second numbe, list of numbers or or Numpy vector
	:type	argb: float, integer, list of floats or integers, or Numpy vector of floats or integers
	:param	prec: Number of digits after the decimal point to which the result is rounded to
	:type	prec: integer
	:rtype: Float, list of floats or Numpy vector, depending on the type of **arga** (which is the same as **argb**)
	:raises:
	 * TypError (Argument `arga` is not valid)

	 * TypError (Argument `argb` is not valid)

	 * TypError (Argument `prec` is not valid)

	 * TypeError (Arguments are not of the same type)
	"""
	if not isinstance(prec, int):
		raise TypeError('Argument `prec` is not valid')
	arga_type = 1 if isreal(arga) is True else (2 if (isinstance(arga, numpy.ndarray) is True) or (isinstance(arga, list) is True) else 0)	#pylint: disable=E1101
	argb_type = 1 if isreal(argb) is True else (2 if (isinstance(argb, numpy.ndarray) is True) or (isinstance(argb, list) is True) else 0)	#pylint: disable=E1101
	if not arga_type:
		raise TypeError('Argument `arga` is not valid')
	if not argb_type:
		raise TypeError('Argument `argb` is not valid')
	if arga_type != argb_type:
		raise TypeError('Arguments are not of the same type')
	if arga_type == 1:
		arga = float(arga)
		argb = float(argb)
		num_max = max(arga, argb)
		num_min = min(arga, argb)
		return 0 if arga == argb else (1e20 if (not num_min) else round((num_max/num_min)-1, prec))
	else:
		arga = numpy.array(arga)
		argb = numpy.array(argb)
		num_max = numpy.maximum(arga, argb)	#pylint: disable=E1101
		num_min = numpy.minimum(arga, argb)	#pylint: disable=E1101
		# Numpy where() function seems to evaluate both arguments after the condition, which prints an error to the console if any element in num_min is zero
		lim_num = 1e+20*numpy.ones(len(num_max))	#pylint: disable=E1101
		safe_indexes = numpy.where(num_min != 0)
		lim_num[safe_indexes] = (num_max[safe_indexes]/num_min[safe_indexes])-1	#pylint: disable=E1101
		return numpy.round(numpy.where(arga == argb, 0, lim_num), prec)	#pylint: disable=E1101


class Bundle(object):	#pylint: disable=R0903
	"""
	Bundle a collection of variables into one object.

	:param	elements: Variable(s) value(s)
	:type	elements: any

	For example:

		>>> obj = putil.misc.Bundle(var1=10)
		>>> obj.var2 = 20
		>>> print str(obj)
		var1 = 10
		var2 = 20
		>>> obj.var2
		20
		>>> del obj.var1
		>>> print str(obj)
		var2 = 20

	"""
	def __init__(self, **elements):
		self.__dict__.update(elements)

	def __len__(self):
		return len(self.__dict__)

	def __repr__(self):
		return 'Bundle({0})'.format(', '.join(['{0}={1}'.format(key, self.__dict__[key]) for key in sorted(self.__dict__.iterkeys())]))

	def __str__(self):
		return '\n'.join(['{0} = {1}'.format(key, self.__dict__[key]) for key in sorted(self.__dict__.iterkeys())])


def make_dir(file_name):
	"""
	Creates the directory of a fully qualified file name if it does not exists

	:param	file_name: Fully qualified file name
	:type	file_name: string
	"""
	file_path, file_name = os.path.split(file_name)
	if os.path.exists(file_path) is False:
		os.makedirs(file_path)


def normalize(value, series, offset=0):
	"""
	Scale a value to the range defined by a series

	:param	value: Value to normalize
	:type	value: number
	:param	series: Series that defines the normalization range
	:type	series: list of numbers
	:param	offset: Normalization offset, i.e. the returned value will be in the range [**offset**, 1.0]
	:type	offset: number
	:rtype: number
	:raises:
	 * ValueError (Argument `offset` has to be in the [0.0, 1.0] range)

	 * ValueError (Argument `value` has to be within the bounds of the argument `series`)
	"""
	if (offset < 0) or (offset > 1):
		raise ValueError('Argument `offset` has to be in the [0.0, 1.0] range')
	if (value < min(series)) or (value > max(series)):
		raise ValueError('Argument `value` has to be within the bounds of argument `series`')
	return offset+(((value-float(min(series)))/(float(max(series))-float(min(series))))*(1.0-offset))


def gcd(vector):
	"""
	Calculates the greatest common divisor of a list of numbers or a Numpy vector of numbers. The computations are carried out with a precision of 1E-12 if the objects are not
	`fractions <https://docs.python.org/2/library/fractions.html>`_. When possible it is best to use the `fractions <https://docs.python.org/2/library/fractions.html>`_ data type defined with the **numerator** and
	**denominator** arguments when computing the GCD of floating numbers (see example).

	:param	vector: Vector of numbers
	:type	vector: list of numbers or Numpy vector of numbers

	For example:

		>>> putil.misc.gcd([20, 12, 16])
		4
		>>> putil.misc.gcd([5/3.0, 2/3.0, 10/3])
		0.3333333333333333
		>>> putil.misc.gcd([fractions.Fraction(5/3.0), fractions.Fraction(2/3.0), fractions.Fraction(10/3.0)])
		Fraction(1, 3)
		>>> putil.misc.gcd([fractions.Fraction(5, 3), fractions.Fraction(2, 3), fractions.Fraction(10, 3)])
		Fraction(1, 3)

	"""
	if len(vector) == 0:
		return None
	elif len(vector) == 1:
		return vector[0]
	elif len(vector) == 2:
		return pgcd(vector[0], vector[1])
	else:
		current_gcd = pgcd(vector[0], vector[1])
		for element in vector[2:]:
			current_gcd = pgcd(current_gcd, element)
		return current_gcd


def pgcd(numa, numb):
	"""
	Calculate the greatest common divisor (GCD) of two numbers

	:param	numa: First number
	:type	numa: numbers
	:param	numb: Second number
	:type	numb: numbers
	:rtype: number

	For example:

		>>> putil.misc.pgcd(10, 15)
		5
		>>> putil.misc.pgcd(0.05, 0.02)
		0.01
		>>> putil.misc.pgcd(5/3.0, 2/3.0)
		0.3333333333333333
		>>> putil.misc.pgcd(fractions.Fraction(5/3.0), fractions.Fraction(2/3.0))
		Fraction(1, 3)
		>>> putil.misc.pgcd(fractions.Fraction(5, 3), fractions.Fraction(2, 3))
		Fraction(1, 3)

	"""
	int_args = isinstance(numa, int) and isinstance(numb, int)
	fraction_args = isinstance(numa, fractions.Fraction) and isinstance(numb, fractions.Fraction)
	if (not int_args) and (not fraction_args):
		numa, numb = fractions.Fraction(numa).limit_denominator(), fractions.Fraction(numb).limit_denominator()
	while numb:
		numa, numb = numb, (numa % numb if int_args else (numa % numb).limit_denominator())
	return int(numa) if int_args else (numa if fraction_args else float(numa))


def isalpha(text):
	"""
	Test if the string represents a number

	:param	text: String to test
	:type	text: string
	:rtype: boolean

	For example:

		>>> putil.misc.isalpha('1.5')
		True
		>>> putil.misc.isalpha('1E-20')
		True
		>>> putil.misc.isalpha('1EA-20')
		False

	"""
	try:
		float(text)
		return True
	except ValueError:
		return False


def ishex(obj):
	"""
	Tests whether argument is a valid hexadecimal digit string

	:param  obj: Test object
	:type	obj: any
	:rtype: boolean
	"""
	return True if (isinstance(obj, str) is True) and (len(obj) == 1) and (obj.upper() in '0123456789ABCDEF') else False


def smart_round(arg, decimals=0):
	"""
	Rounds a floating point number or Numpy vector

	:param	arg: Input data
	:type	arg: number, Numpy vector of numbers or None
	:param	decimals: Number of decimal places to round to. For Numpy vectors if decimals is negative, it specifies the number of positions to the left of the decimal point
	:param	decimals: integer
	:rtype: number, Numpy vector of numbers or None depending on type of **arg**
	"""
	if arg is None:
		return arg
	elif isinstance(arg, numpy.ndarray):
		return numpy.around(arg, decimals)
	else:
		return round(arg, decimals)


def isiterable(obj):
	"""
	Tests whether an objects is an iterable

	:param	obj: Test object
	:type	obj: any
	:rtype: boolean
	"""
	try:
		iter(obj)
	except:	#pylint: disable=W0702
		return False
	else:
		return True


def pprint_vector(vector, limit=False, width=None, indent=0, eng=False, mant=3):	#pylint: disable=R0913,R0914
	"""
	Formats a list of numers (vector) or a Numpy vector for printing. If **vector** is *None* the string 'None' is returned

	:param	vector: Vector to pretty print or *None*
	:type	vector: list of numbers, Numpy vector or *None*
	:param	limit: Flag that indicates if at most 6 vector elements should be printed (all vector elements if its length is equal or less than 6, first and last 3 vector elements if it is not) (*True*), or if the entire vector\
	 should be printed (*False*)
	:type	limit: boolean
	:param	width: Number of characters per line available to print vector. If *None* the vector is printed in one line
	:type	width: integer or None
	:param	indent: Flag that indicates whether all subsequent lines after the first one are to be indented (*True*) or not (*False*). Only relevant is **width** is not *None*
	:type	indent: boolean
	:param	eng: Flag that indicates whether engineering notation should be used to print vector contents (*True*) or not (*False*)
	:type	eng: boolean
	:param	mant: Number of mantissa digits (only applicable if **eng** is *True*)
	:type	mant: integer
	:rtype: string

	For example:

		>>> header = 'Vector: '
		>>> data = [1e-3, 20e-6, 300e+6, 4e-12, 5.25e3, -6e-9, 700, 8, 9]
		>>> print header+putil.misc.pprint_vector(data, width=30, eng=True, mant=1, limit=True, indent=len(header))
		Vector: [    1.0m,   20.0u,  300.0M,
		                     ...
		           700.0 ,    8.0 ,    9.0  ]
		>>> print header+putil.misc.pprint_vector(data, width=30, eng=True, mant=0, indent=len(header))
		Vector: [    1m,   20u,  300M,    4p,
		             5k,   -6n,  700 ,    8 ,
		             9  ]
		>>> print putil.misc.pprint_vector(data, eng=True, mant=0)
		[    1m,   20u,  300M,    4p,    5k,   -6n,  700 ,    8 ,    9  ]
		>>> print putil.misc.pprint_vector(data, limit=True)
		[ 0.001, 2e-05, 300000000.0, ..., 700, 8, 9 ]

	"""
	import putil.eng
	def _str(element):
		""" Print a straight number or one with engineering notation """
		return element if not eng else putil.eng.peng(element, mant, True)

	if vector is None:
		return 'None'
	if (not limit) or (limit and (len(vector) < 7)):
		uret = '[ '+(', '.join(['{0}'.format(_str(element)) for element in vector]))+' ]'
	else:
		uret = '[ {0}, {1}, {2}, ..., {3}, {4}, {5} ]'.format(_str(vector[0]), _str(vector[1]), _str(vector[2]), _str(vector[-3]), _str(vector[-2]), _str(vector[-1]))
	if (width is None) or (len(uret) < width):
		return uret
	# Figure out how long the first line needs to be
	wobj = textwrap.TextWrapper(initial_indent='[ ', width=width, subsequent_indent=(indent+2)*' ')
	wrapped_lines_list = wobj.wrap(uret[2:])
	first_line = wrapped_lines_list[0]
	elements_per_row = first_line.count(',')
	if elements_per_row == 0:
		raise ValueError('Argument `width` is too small')
	# "Manually" format limit output so that it is either 3 lines, first and line with 3 elements and the middle with '...' or 7 lines, each with 1 element and the middle with '...'
	if limit:
		if elements_per_row < 3:
			rlist = ['[ {0},'.format(_str(vector[0])), _str(vector[1]), _str(vector[2]), '...', _str(vector[-3]), _str(vector[-2]), '{0} ]'.format(_str(vector[-1]))]
			elements_per_row = 1
		else:
			rlist = ['[ {0}, {1}, {2},'.format(_str(vector[0]), _str(vector[1]), _str(vector[2])), '...', '{0}, {1}, {2} ]'.format(_str(vector[-3]), _str(vector[-2]), _str(vector[-1]))]
		first_line = rlist[0]
	else:
		rlist = wobj.wrap(uret[2:])
	# Use output of wrap() if numbers cannot be aligned at comma (variable width)
	if not eng:
		return '\n'.join(rlist)
	# Align elements across multiple lines
	remainder_list = [line.lstrip() for line in rlist[1:]] if limit else split_every(uret[len(first_line):], ',', elements_per_row, lstrip=True)
	first_comma_index = first_line.find(',')
	actual_width = len(first_line)-2
	new_wrapped_lines_list = [first_line]
	for line in remainder_list[:-1]:
		new_wrapped_lines_list.append('{0},'.format(line).rjust(actual_width) if line != '...' else line.center(actual_width).rstrip())
	# Align last line on fist comma (if it exists) or on length of field if not
	marker = len(remainder_list[-1])-2	if remainder_list[-1].find(',') == -1 else remainder_list[-1].find(',')
	new_wrapped_lines_list.append('{0}{1}'.format((first_comma_index-marker-2)*' ', remainder_list[-1]))
	return '\n'.join([((indent+2)*' ')+line if num > 0 else line for num, line in enumerate(new_wrapped_lines_list)])


def elapsed_time_string(start_time, stop_time):
	""" Returns a formatted string with the elapsed time between two time points. The string includes years (365 days), months (30 days), days (24 hours), hours (60 minutes), minutes (60 seconds) and seconds.
	If **start_time** and **stop_time** are equal, the string returned is 'None'; otherwise, the string returned is [YY year[s], [MM month[s], [DD day[s], [HH hour[s], [MM minute[s] [and SS second[s]]]]]].
	Any piece (year[s], month[s], etc.) is omitted if the number of the token is null/zero.

	:param	start_time:	Starting time point
	:type	start_time:	`datetime <https://docs.python.org/2/library/datetime.html#datetime-objects>`_ object
	:param	stop_time:	Ending time point
	:type	stop_time:	`datetime`_ object
	:rtype:				string
	:raises: RuntimeError (Invalid time delta specification)
	"""
	if start_time > stop_time:
		raise RuntimeError('Invalid time delta specification')
	delta_time = stop_time-start_time
	tot_seconds = int(delta_time.total_seconds())
	years, remainder = divmod(tot_seconds, 365*24*60*60)
	months, remainder = divmod(remainder, 30*24*60*60)
	days, remainder = divmod(remainder, 24*60*60)
	hours, remainder = divmod(remainder, 60*60)
	minutes, seconds = divmod(remainder, 60)
	ret_list = ['{0} {1}{2}'.format(num, desc, 's' if num > 1 else '') for num, desc in zip([years, months, days, hours, minutes, seconds], ['year', 'month', 'day', 'hour', 'minute', 'second']) if num > 0]
	if len(ret_list) == 0:
		return 'None'
	elif len(ret_list) == 1:
		return ret_list[0]
	elif len(ret_list) == 2:
		return ret_list[0]+' and '+ret_list[1]
	else:
		return (', '.join(ret_list[0:-1]))+' and '+ret_list[-1]


def strframe(obj, extended=False):
	"""
	Pretty prints a frame record (typically an item in a list generated by `inspect.stack() <https://docs.python.org/2/library/inspect.html#module-inspect>`_)

	:param	obj: Frame record
	:type	obj: tuple
	:param	extended: Additionally pretty prints contents of frame object of frame record (*True*) or not (*False*)
	:type	extended: boolean
	:rtype:		string
	"""
	# Stack frame -> (frame object [0], filename [1], line number of current line [2], function name [3], list of lines of context from source code [4], index of current line within list [5])
	ret = list()
	ret.append(pcolor('Frame object ID: {0}'.format(hex(id(obj[0]))), 'yellow'))
	ret.append('File name......: {0}'.format(obj[1]))
	ret.append('Line number....: {0}'.format(obj[2]))
	ret.append('Function name..: {0}'.format(obj[3]))
	ret.append('Context........: {0}'.format(obj[4]))
	ret.append('Index..........: {0}'.format(obj[5]))
	if extended:
		ret.append('f_back ID......: {0}'.format(hex(id(obj[0].f_back))))
		ret.append('f_builtins.....: {0}'.format(obj[0].f_builtins))
		ret.append('f_code.........: {0}'.format(obj[0].f_code))
		ret.append('f_globals......: {0}'.format(obj[0].f_globals))
		ret.append('f_lasti........: {0}'.format(obj[0].f_lasti))
		ret.append('f_lineno.......: {0}'.format(obj[0].f_lineno))
		ret.append('f_locals.......: {0}'.format(obj[0].f_locals))
		ret.append('f_restricted...: {0}'.format(obj[0].f_restricted))
		ret.append('f_trace........: {0}'.format(obj[0].f_trace))
	return '\n'.join(ret)


# From https://mail.python.org/pipermail/tutor/2006-August/048596.html
def delete_module(modname):
	""" Deletes a previously imported module

	:param	modname: Module name
	:type	modname: string
	:raises: ValueError (Module *[modname]* is not imported)
	"""
	if modname not in sys.modules:
		raise ValueError('Module {0} is not imported'.format(modname))
	del sys.modules[modname]
	for mod in sys.modules.values():
		try:
			delattr(mod, modname)
		except AttributeError:
			pass


def quote_str(obj):
	"""
	Adds extra quotes to string object

	:param	obj: Object to be quoted if string
	:type	obj: any
	:rtype:	Same as **obj**
	"""
	return obj if not isinstance(obj, str) else ("'{0}'".format(obj) if '"' in obj else '"{0}"'.format(obj))


def strtype_item(type_obj):
	""" Generates a string of a type definition (int, str, etc.) otherwise returns the sting of the object via the str() function """
	return str(type_obj).replace("<type '", '').replace("<class '", '')[:-2] if isinstance(type_obj, type) else (quote_str(type_obj) if isinstance(type_obj, str) else str(type_obj))


def strtype(type_obj):
	"""
	Generates a string of a type definition (int, str, etc.) or type definition list otherwise returns the string or list of the object(s) via the str() function

	:param	type_obj: Object for which to get type string or string of its contents
	:type	type_obj: any
	:rtype: string

	For example:

		>>> putil.misc.strtype({'file':str, 'name':'some_file.txt', 'line':5, 'class':putil.pcsv.CsvFile})
		'{"line":5, "name":"some_file.txt", "file":str, "class":putil.pcsv.CsvFile}'
		>>> putil.misc.strtype(str)
		'str'

	"""
	if (not isiterable(type_obj)) or (type(type_obj) not in [dict, list, set, tuple]):
		return strtype_item(type_obj)
	if isinstance(type_obj, dict):
		return '{'+(', '.join(['"{0}":{1}'.format(key, strtype(type_obj[key])) for key in sorted(type_obj.keys())]))+'}'
	prefix = '[' if isinstance(type_obj, list) else ('(' if isinstance(type_obj, tuple) else 'set(')
	suffix = ']' if isinstance(type_obj, list) else ')'
	type_obj = sorted(type_obj) if isinstance(type_obj, set) else type_obj
	ret_list = [strtype(type_obj_item) for type_obj_item in type_obj]
	return '{0}{1}{2}'.format(prefix, ', '.join(ret_list), suffix)


def flatten_list(lobj):
	"""
	Recursively flattens list

	:param	lobj: List to flatten
	:type	lobj: list
	:rtype: list

	For example:

		>>> putil.misc.flatten_list([1, [2, 3, [4, 5, 6]], 7])
		[1, 2, 3, 4, 5, 6, 7]

	"""
	ret = []
	for item in lobj:
		if isinstance(item, list):
			for sub_item in flatten_list(item):
				ret.append(sub_item)
		else:
			ret.append(item)
	return ret


def isexception(obj):
	"""
	Tests whether an object is an exception object

	:param	obj: Object to test
	:type	obj: any
	:rtype: boolean
	"""
	return False if not inspect.isclass(obj) else issubclass(obj, Exception)


def split_every(text, sep, count, lstrip=False, rstrip=False):
	"""
	Returns a list of the words in the string, using a count of a separator as the delimiter

	:param	text: String to split
	:type	text: string
	:param	sep: Separator
	:type	sep: string
	:param	count: Number of separators to use as delimiter
	:type	count: integer
	:param	lstrip: Flag that indicates whether whitespace should be removed from the beginning of each list item (*True*) or not (*False*)
	:type	lstrip: boolean
	:param	rstrip: Flag that indicates whether whitespace should be removed from the end of each list item (*True*) or not (*False*)
	:type	rstrip: boolean
	:rtype: list
	"""
	tlist = text.split(sep)
	lines = [sep.join(tlist[num:min(num+count, len(tlist))]) for num in range(0, len(tlist), count)]
	return [line.rstrip() if (rstrip and not lstrip) else (line.lstrip() if (lstrip and not rstrip) else (line.strip() if lstrip and rstrip else line)) for line in lines]

def to_scientific_tuple(number):
	"""
	Returns a tuple where the first element is the mantissa (*string*) and the second element is the exponent (*integer*) of a number when expressed in scientific notation. Full precision is maintained if the number is
	represented a string

	:param	number: number to extract information from
	:type	number: number or string of a number
	:rtype: tuple
	"""
	convert = not isinstance(number, str)
	if (convert and (number == 0)) or ((not convert) and (not number.strip('0').strip('.'))):
		return ('0', 0)
	num_sign, digits, exp = decimal.Decimal(str(number) if convert else number).as_tuple()	#num_sign = 1 -> negative number, pylint: disable=W0632
	mant = ('-' if num_sign else '')+(str(digits[0])+('.'+(''.join([str(num) for num in digits[1:]])) if len(digits) > 1 else '')).rstrip('0').rstrip('.')
	exp += len(digits)-1
	return (mant, exp)

def to_scientific_string(number):
	"""
	Converts a number or a string representing a number to a string with the number expressed in scientific notation. Full precision is maintained if the number is represented a string


	:param	number: number to convert
	:type	number: number or string of a number
	:rtype: string
	"""
	mant, exp = to_scientific_tuple(number)
	return '{0}E{1}{2}'.format(mant, '-' if exp < 0 else '+', abs(exp))
