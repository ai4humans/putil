# pcsv.py	pylint:disable=C0111
# Copyright (c) 2014 Pablo Acosta-Serafini
# See LICENSE for details

import csv

import putil.exh
import putil.misc
import putil.check


_EXH = putil.exh.ExHandle()

@putil.check.check_arguments({'file_name':putil.check.File(check_existance=False), 'data':putil.check.ArbitraryLengthList(list), 'append':bool})
def write(file_name, data, append=True):
	"""
	Writes data to a specified comma-separated values (CSV) file

	:param	file_name:	File name of the comma-separated values file to be written
	:type	file_name:	string
	:param	data:	Data to write to file.
	:type	data:	list
	:param	append: Append data flag. If **append** is *True* data is added to **file_name** if it exits, otherwise a new file is created. If **append** is *False*, a new file is created, \
	possibly overwriting an exisiting file with the same name
	:type	append: boolean
	:raises:
	 * TypeError (Argument `file_name` is of the wrong type)

	 * TypeError (Argument `data` is of the wrong type)

	 * TypeError (Argument `data` is empty)

	 * TypeError (Argument `append` is of the wrong type)

	 * IOError (File *[file_name]* could not be created: *[reason]*)

	 * OSError (File *[file_name]* could not be created: *[reason]*)

	 * RuntimeError (File *[file_name]* could not be created: *[reason]*)
	"""
	if (len(data) == 0) or ((len(data) == 1) and (len(data[0]) == 0)):
		raise ValueError('Argument `data` is empty')
	# Process data, turn None to '' and integer to integers
	try:
		putil.misc.make_dir(file_name)
		file_handle = open(file_name, 'wb' if append is False else 'ab')
		csv_handle = csv.writer(file_handle, delimiter=',')
		for row in data:
			csv_handle.writerow(row)
		file_handle.close()
	except IOError as msg:
		raise IOError('File {0} could not be created: {1}'.format(file_name, msg.strerror))
	except OSError as msg:
		raise OSError('File {0} could not be created: {1}'.format(file_name, msg.strerror))
	except Exception as msg:
		raise RuntimeError('File {0} could not be created: {1}'.format(file_name, msg.strerror))


def _number_failsafe(obj):
	""" Convert to float if object is a float string """
	if 'inf' in obj.lower():
		return obj
	try:
		return int(obj)
	except:	#pylint: disable=W0702
		try:
			return float(obj)
		except:	#pylint: disable=W0702
			return obj


class CsvFile(object):
	"""
	Process comma-separated values (CSV) files

	:param	file_name:	File name of the comma-separated values file to be read
	:type	file_name:	string
	:param	dfilter:	Data filter. See :py:attr:`putil.pcsv.CsvFile.dfilter`
	:type	dfilter:	dictionary
	:rtype:	:py:class:`putil.pcsv.CsvFile()` object
	:raises:
	 * TypeError (Argument `file_name` is of the wrong type)

	 * IOError (File *[file_name]* could not be found)

	 * RuntimeError (File *[file_name]* is empty)

	 * RuntimeError (Column headers are not unique)

	 * RuntimeError (File *[file_name]* has no data)

	 * Same as :py:attr:`putil.pcsv.CsvFile.dfilter`
	"""
	@putil.check.check_arguments({'file_name':putil.check.File(check_existance=True), 'dfilter':putil.check.PolymorphicType([None, dict])})
	def __init__(self, file_name, dfilter=None):
		self._header, self._header_upper, self._data, self._fdata, self._dfilter = None, None, None, None, None
		with open(file_name, 'rU') as file_handle:
			self._raw_data = [row for row in csv.reader(file_handle)]
		# Process header
		if len(self._raw_data) == 0:
			raise RuntimeError('File {0} is empty'.format(file_name))
		self._header = self._raw_data[0]
		self._header_upper = [col.upper() for col in self.header]

		if len(set(self._header_upper)) != len(self._header_upper):
			raise RuntimeError('Column headers are not unique')
		# Find start of data row
		num = 0
		for num, row in enumerate(self._raw_data[1:]):
			if any([putil.misc.isnumber(_number_failsafe(col)) for col in row]):
				break
		else:
			raise RuntimeError('File {0} has no data'.format(file_name))
		# Set up class properties
		self._data = [[None if col.strip() == '' else _number_failsafe(col) for col in row] for row in self._raw_data[num+1:]]
		self.reset_dfilter()
		self._set_dfilter(dfilter)

	def _validate_dfilter(self, dfilter):
		""" Validate that all columns in filter are in header """
		if dfilter is not None:
			if len(dfilter) == 0:
				raise ValueError('Argument `dfilter` is empty')
			for key in dfilter:
				self._in_header(key)

	def _get_dfilter(self):	#pylint: disable=C0111
		return self._dfilter	#pylint: disable=W0212

	@putil.check.check_argument(putil.check.PolymorphicType([None, dict]))
	def _set_dfilter(self, dfilter):	#pylint: disable=C0111
		if dfilter is None:
			self._dfilter = None
		else:
			self._validate_dfilter(dfilter)
			col_nums = [self._header_upper.index(key.upper()) for key in dfilter]
			col_values = [[element] if not putil.misc.isiterable(element) else [value for value in element] for element in dfilter.values()]
			self._fdata = [row for row in self._data if all([row[col_num] in col_value for col_num, col_value in zip(col_nums, col_values)])]
			self._dfilter = dfilter

	@putil.check.check_argument(dict)
	def add_dfilter(self, dfilter):
		"""
		Adds more data filter(s) to the existing filter(s). Data is added to the current filter for a particular column if that column was already filtered, duplicate filter values are eliminated.

		:param	dfilter:	Filter specification. See :py:attr:`putil.pcsv.CsvFile.dfilter`
		:type	dfilter:	dictionary
		:raises: Same as :py:attr:`putil.pcsv.CsvFile.dfilter`
		"""
		self._validate_dfilter(dfilter)
		print str(_EXH)
		if dfilter is None:
			self._dfilter = dfilter
		elif self._dfilter is None:
			self._dfilter = dfilter
		else:
			for key in dfilter:
				if key in self._dfilter:
					self._dfilter[key] = list(set((self._dfilter[key] if isinstance(self._dfilter[key], list) else [self._dfilter[key]]) + (dfilter[key] if isinstance(dfilter[key], list) else [dfilter[key]])))
				else:
					self._dfilter[key] = dfilter[key]
		self._set_dfilter(self._dfilter)

	def _get_header(self):	#pylint: disable=C0111
		return self._header	#pylint: disable=W0212

	@putil.check.check_arguments({'col':putil.check.PolymorphicType([None, str, putil.check.ArbitraryLengthList(str)]), 'filtered':bool})
	def data(self, col=None, filtered=False):
		"""
		:param	col:	Column(s) to extract from filtered data. If no column specification is given (or **col** is *None*) all columns are returned
		:type	col:	string, list of strings or None, default is *None*
		:param	filtered: Raw or filtered data flag. If **filtered** is *True*, the filtered data is returned, if **filtered** is *False* the raw (original) file data is returned
		:type	filtered: boolean
		:returns: (filtered) file data. The returned object is a list of lists, where each sub-list corresponds to a row of the CSV file and each element in that sub-list corresponds to a column of the CSV file.
		:rtype:	list
		:raises:
		 * TypeError (Argument `col` is of the wrong type)

		 * TypeError (Argument `filtered` is of the wrong type)

		 * ValueError (Column *[column_name]* not found in header)
		"""
		self._in_header(col)
		return (self._data if not filtered else self._fdata) if col is None else self._core_data((self._data if not filtered else self._fdata), col)

	def reset_dfilter(self):
		""" Resets (clears) data filter """
		self._fdata = self._data[:]
		self._dfilter = None

	@putil.check.check_arguments({'file_name':putil.check.File(check_existance=False), 'col':putil.check.PolymorphicType([None, str, putil.check.ArbitraryLengthList(str)]), 'filtered':bool, 'headers':bool, 'append':bool})
	def write(self, file_name, col=None, filtered=False, headers=True, append=True):	#pylint: disable=R0913
		"""
		Writes (processed) data to a specified comma-separated values (CSV) file

		:param	file_name:	File name of the comma-separated values file to be written
		:type	file_name:	string
		:param	col:	Column(s) to write to file. If no column specification is given (or **col** is *None*) all columns in data are written
		:type	col:	string, list of strings or None, default is *None*
		:param	filtered: Raw or filtered data flag. If **filtered** is *True*, the filtered data is written, if **filtered** is *False* the raw (original) file data is written
		:type	filtered: boolean
		:param	headers: Include headers flag. If **headers** is *True* headers and data are written, if **headers** is *False* only data is written
		:type	headers: boolean
		:param	append: Append data flag. If **append** is *True* data is added to **file_name** if it exits, otherwise a new file is created. If **append** is *False*, a new file is created, \
		possibly overwriting an exisiting file with the same name
		:type	append: boolean
		:raises:
		 * TypeError (Argument `file_name` is of the wrong type)

		 * TypeError (Argument `headers` is of the wrong type)

		 * TypeError (Argument `append` is of the wrong type)

		 * ValueError (There is no data to save to file)

		 * IOError (File *[file_name]* could not be created: *[reason]*)

		 * OSError (File *[file_name]* could not be created: *[reason]*)

		 * RuntimeError (File *[file_name]* could not be created: *[reason]*)

		 * Same as :py:attr:`putil.pcsv.CsvFile.data`
		"""
		self._in_header(col)
		data = self.data(col=col, filtered=filtered)
		if headers:
			col = [col] if isinstance(col, str) else col
			header = self.header if col is None else [self.header[self._header_upper.index(element.upper())] for element in col]
		if (len(data) == 0) or ((len(data) == 1) and (len(data[0]) == 0)):
			raise ValueError('There is no data to save to file')
		data = [["''" if col is None else col for col in row] for row in data]
		write(file_name, [header]+data if headers else data, append=append)

	def _in_header(self, col):
		""" Validate column name(s) against the column names in the file header """
		if col is not None:
			col_list = [col] if isinstance(col, str) else col
			for col in col_list:
				if col.upper() not in self._header_upper:
					raise ValueError('Column {0} not found in header'.format(col))

	def _core_data(self, data, col=None):
		""" Extract columns from data """
		if isinstance(col, str):
			col_num = self._header_upper.index(col.upper())
			return [[row[col_num]] for row in data]
		elif isinstance(col, list):
			col_list = col[:]
			col_index_list = [self._header_upper.index(col.upper()) for col in col_list]
			return [[row[index] for index in col_index_list] for row in data]

	# Managed attributes
	dfilter = property(_get_dfilter, _set_dfilter, None, doc='Data filter')
	"""
	The data filter consisting of a series of individual filters. Each individual filter in turn consists of column name (dictionary key) and either a value representing a column value or an iterable (dictionary value). If the
	dictionary value is a column value all rows which cointain the specified value in the specified column are kept for that particular individual filter. The overall data set is the intersection of all the data sets specified
	by each individual filter. For example, if the file name to be processed is:

	+------+-----+--------+
	| Ctrl | Ref | Result |
	+======+=====+========+
	|    1 |   3 |     10 |
	+------+-----+--------+
	|    1 |   4 |     20 |
	+------+-----+--------+
	|    2 |   4 |     30 |
	+------+-----+--------+
	|    2 |   5 |     40 |
	+------+-----+--------+
	|    3 |   5 |     50 |
	+------+-----+--------+

	Then the filter specification ``dfilter = {'Ctrl':2, 'Ref':5}`` would result in the following filtered data set:

	+------+-----+--------+
	| Ctrl | Ref | Result |
	+======+=====+========+
	|    2 |   5 |     40 |
	+------+-----+--------+

	However, the filter specification ``dfilter = {'Ctrl':2, 'Ref':3}`` would result in an empty list because the data set specified by the `Ctrl` individual filter does not overlap with the data set specified by
	the `Ref` individual filter.

	If the dictionarly value is an iterable (typically a list), the element of the iterable represent all the values to be kept for a particular column. So for example ``dfilter = {'Ctrl':[2, 3], 'Ref':5}`` would
	result in the following filtered data set:

	+------+-----+--------+
	| Ctrl | Ref | Result |
	+======+=====+========+
	|    2 |   5 |     40 |
	+------+-----+--------+
	|    3 |   5 |     50 |
	+------+-----+--------+

	:type:		dictionary, default is *None*
	:returns:	current data filter
	:rtype:		dictionary or None
	:raises:
	 * TypeError (Argument `dfilter` is of the wrong type)

	 * ValueError (Argument `dfilter` is empty)

	 * ValueError (Column *[column name]* not found in header)
	"""	#pylint: disable=W0105

	header = property(_get_header, None, None, doc='Comma-separated file (CSV) header')
	"""
	:returns: Header of the comma-separated values file. Each column is an element of the list.
	:rtype:	list of strings
	"""	#pylint: disable=W0105
