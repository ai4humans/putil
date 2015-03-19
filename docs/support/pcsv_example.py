﻿# pcsv_example.py
# pylint: disable=C0111,W0104
import os, putil.pcsv

def main():
	""" Usage example for pcsv module """
	data = [['Item', 'Cost'], [1, 9.99], [2, 10000], [3, 0.10]]
	file_name = './my_file.csv'
	# Write data to a file, first sub-list in the data list is _always_ considered the headers
	putil.pcsv.write(file_name, data, append=False)
	# Read the data back
	obj = putil.pcsv.CsvFile(file_name)
	# After the object creation the I/O is done, can safely remove file
	os.remove(file_name)
	# Check that data read is correct
	assert obj.header == ['Item', 'Cost']
	assert obj.data() == [[1, 9.99], [2, 10000], [3, 0.10]]
	# Add a simple filter, only look at rows that have values 1 and 3 in the "Items" column
	obj.dfilter = {'Item':[1, 3]}
	assert obj.data(filtered=True) == [[1, 9.99], [3, 0.10]]

if __name__ == '__main__':
	main()