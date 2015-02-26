﻿# test_exh.py
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0302,W0212

"""
putil.exh unit tests
"""

import copy
import mock
import pytest

import putil.exh
import putil.test
import putil.pcontracts

def test_star_exh_obj():
	""" Test [get|set|del]_exh_obj() function """
	putil.test.assert_exception(putil.exh.set_exh_obj, {'value':5}, TypeError, 'Argument `value` is not valid')
	exobj = putil.exh.ExHandle()
	putil.exh.set_exh_obj(exobj)
	assert id(putil.exh.get_exh_obj()) == id(exobj)
	putil.exh.del_exh_obj()
	assert putil.exh.get_exh_obj() == None
	putil.exh.del_exh_obj()	# Test that nothing happens if del_exh_obj is called when there is no global object handler set
	new_exh_obj = putil.exh.get_or_create_exh_obj()
	assert id(new_exh_obj) != id(exobj)
	assert id(putil.exh.get_or_create_exh_obj()) == id(new_exh_obj)


def test_ex_type_str():
	""" test _ex_type_str() function """
	assert putil.exh._ex_type_str(RuntimeError) == 'RuntimeError'
	assert putil.exh._ex_type_str(IOError) == 'IOError'

def test_add_exception_errors():
	""" Test add_exception() function errors """
	def mock_get_code_id(obj):	#pylint: disable=W0612,W0613
		""" Return unique identity tuple to individualize callable object """
		return None
	obj = putil.exh.ExHandle()
	putil.test.assert_exception(obj.add_exception, {'exname':5, 'extype':RuntimeError, 'exmsg':'Message'}, TypeError, 'Argument `exname` is not valid')
	putil.test.assert_exception(obj.add_exception, {'exname':'exception', 'extype':5, 'exmsg':'Message'}, TypeError, 'Argument `extype` is not valid')
	putil.test.assert_exception(obj.add_exception, {'exname':'exception', 'extype':RuntimeError, 'exmsg':True}, TypeError, 'Argument `exmsg` is not valid')
	# These should not raise an exception
	obj = putil.exh.ExHandle()
	obj.add_exception(exname='exception name', extype=RuntimeError, exmsg='exception message for exception #1')
	obj.add_exception(exname='exception name', extype=TypeError, exmsg='exception message for exception #2')
	# Test case where callable is not found in callable database
	with mock.patch('putil.exh._get_code_id') as mock_get_code_id:
		#test_list.append(putil.test.trigger_exception(obj.add_exception, {'exname':'exception name', 'extype':RuntimeError, 'exmsg':'exception message for exception #1'}, RuntimeError, 'Callable full name could not be obtained'))
		putil.test.assert_exception(obj.add_exception, {'exname':'exception name', 'extype':RuntimeError, 'exmsg':'exception message for exception #1'}, RuntimeError, \
			r'Callable with call ID <([\w|\W|\s]+)> not found in reverse callables database')

def test_add_exception_works():	# pylint: disable=R0912,R0914,R0915
	""" Test add_exception() function works """
	exobj = putil.exh.ExHandle()
	def func1():	#pylint: disable=C0111,W0612
		exobj.add_exception('first_exception', TypeError, 'This is the first exception')
		print "Hello"
	def prop_decorator(func):	#pylint: disable=C0111,W0612
		return func
	@putil.pcontracts.contract(text=str)
	@prop_decorator
	def func2(text):	#pylint: disable=C0111,W0612
		exobj.add_exception('second_exception', ValueError, 'This is the second exception')
		exobj.add_exception('third_exception', IOError, 'This is the third exception')
		print text
	class Class1(object):	#pylint: disable=C0111,R0903
		def __init__(self, exobj):
			self._value = None
			self._exobj = exobj
		@property
		def value3(self):	#pylint: disable=C0111
			self._exobj.add_exception('getter_exception', TypeError, 'Get function exception')
			return self._value
		@value3.setter
		@putil.pcontracts.contract(value=int)
		def value3(self, value):	#pylint: disable=C0111
			self._exobj.add_exception('setter_exception', TypeError, 'Set function exception')
			self._value = value
		@value3.deleter
		def value3(self):	#pylint: disable=C0111,R0201
			self._exobj.add_exception('deleter_exception', TypeError, 'Delete function exception')
			print 'Cannot delete attribute'
	def func7():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_7', TypeError, 'Total exception #7')
	def func8():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_8', TypeError, 'Total exception #8')
	def func9():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_9', TypeError, 'Total exception #9')
	def func10():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_10', TypeError, 'Total exception #10')
	def func11():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_11', TypeError, 'Total exception #11')
	def func12():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_12', TypeError, 'Total exception #12')
	def func13():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_13', TypeError, 'Total exception #13')
	def func14():	#pylint: disable=C0111,W0612
		exobj.add_exception('total_exception_14', TypeError, 'Total exception #14')
	dobj = Class1(exobj)	#pylint: disable=W0612
	dobj.value3 = 5
	print dobj.value3
	del dobj.value3
	cdb = exobj._ex_dict
	func1()
	func2("world")
	func7()
	func8()
	func9()
	func10()
	func11()
	func12()
	func13()
	func14()
	if not cdb:
		assert False
	for exname in cdb:
		erec = cdb[exname]
		if exname.endswith('/first_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func1') and (erec['type'] == TypeError) and (erec['msg'] == 'This is the first exception') and (erec['checked'] == False)
		elif exname.endswith('/second_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func2') and (erec['type'] == ValueError) and (erec['msg'] == 'This is the second exception') and (erec['checked'] == False)
		elif exname.endswith('/third_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func2') and (erec['type'] == IOError) and (erec['msg'] == 'This is the third exception') and (erec['checked'] == False)
		elif exname.endswith('/setter_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.Class1.value3(setter)') and (erec['type'] == TypeError) and (erec['msg'] == 'Set function exception') and (erec['checked'] == False)
		elif exname.endswith('/getter_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.Class1.value3(getter)') and (erec['type'] == TypeError) and (erec['msg'] == 'Get function exception') and (erec['checked'] == False)
		elif exname.endswith('/deleter_exception'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.Class1.value3(deleter)') and (erec['type'] == TypeError) and (erec['msg'] == 'Delete function exception') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_7'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func7') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #7') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_8'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func8') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #8') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_9'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func9') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #9') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_10'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func10') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #10') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_11'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func11') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #11') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_12'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func12') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #12') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_13'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func13') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #13') and (erec['checked'] == False)
		elif exname.endswith('/total_exception_14'):
			assert erec['function'].endswith('test_exh.test_add_exception_works.func14') and (erec['type'] == TypeError) and (erec['msg'] == 'Total exception #14') and (erec['checked'] == False)
		else:
			assert False
	# Test that function IDs are unique
	repeated_found = False
	exlist = []
	for exname in cdb:
		if (exname.endswith('/second_exception') or exname.endswith('/third_exception')) and (not repeated_found):
			func_id = exname.split('/')[0]
			repeated_found = True
			exlist.append(func_id)
		elif exname.endswith('/second_exception') or exname.endswith('/third_exception'):
			if exname.split('/')[0] != func_id:
				assert False
		else:
			exlist.append(exname.split('/')[0])
	assert len(set(exlist)) == len(exlist)

def test_raise_exception():
	""" Test raise_exception_if() function errors """
	obj = putil.exh.ExHandle()
	def func3(cond1=False, cond2=False, cond3=False, cond4=False):	#pylint: disable=C0111,W0612
		exobj = putil.exh.ExHandle()
		exobj.add_exception('my_exception1', RuntimeError, 'This is an exception')
		exobj.add_exception('my_exception2', IOError, 'This is an exception with a *[file_name]* field')
		exobj.raise_exception_if('my_exception1', cond1, edata=None)
		exobj.raise_exception_if('my_exception2', cond2, edata={'field':'file_name', 'value':'my_file.txt'})
		if cond3:
			exobj.raise_exception_if('my_exception3', False)
		if cond4:
			exobj.raise_exception_if('my_exception2', cond4, edata={'field':'not_a_field', 'value':'my_file.txt'})
		return exobj
	putil.test.assert_exception(obj.raise_exception_if, {'exname':5, 'condition':False}, TypeError, 'Argument `exname` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':5}, TypeError, 'Argument `condition` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':354}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':{'field':'my_field'}}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':{'field':3, 'value':5}}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':{'value':5}}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':[{'field':'my_field1', 'value':5}, {'field':'my_field'}]}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':[{'field':'my_field1', 'value':5}, {'field':3, 'value':5}]}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(obj.raise_exception_if, {'exname':'my_exception', 'condition':False, 'edata':[{'field':'my_field1', 'value':5}, {'value':5}]}, TypeError, 'Argument `edata` is not valid')
	putil.test.assert_exception(func3, {'cond1':True, 'cond2':False}, RuntimeError, 'This is an exception')
	putil.test.assert_exception(func3, {'cond2':True}, IOError, 'This is an exception with a my_file.txt field')
	putil.test.assert_exception(func3, {'cond3':True}, ValueError, 'Exception name my_exception3 not found')
	putil.test.assert_exception(func3, {'cond4':True}, RuntimeError, 'Field not_a_field not in exception message')
	exobj = func3()	# Test that edata=None works
	cdb = exobj._ex_dict
	if not cdb:
		assert False
	for exname, erec in cdb.items():
		if exname.endswith('test_exh.test_raise_exception.func3.my_exception1'):
			assert erec['function'].endswith('test_exh.test_raise_exception.func3') and (erec['type'] == RuntimeError) and (erec['msg'] == 'This is an exception') and (erec['checked'] == True)
		if exname.endswith('test_exh.test_raise_exception.func3.my_exception2'):
			assert erec['function'].endswith('test_exh.test_raise_exception.func3') and (erec['type'] == IOError) and (erec['msg'] == 'This is an exception with a *[file_name]* field') and (erec['checked'] == True)

def test_exceptions_db():
	""" Test _exceptions_db() property """
	# Functions definitions
	def func4(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exception1', RuntimeError, 'This is exception #1')
	def func5(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exception2', ValueError, 'This is exception #2, *[result]*')
		exobj.add_exception('my_exception3', TypeError, 'This is exception #3')
	exobj = putil.exh.ExHandle()
	func4(exobj)
	func5(exobj)
	# Actual tests
	# Test that property cannot be deleted
	with pytest.raises(AttributeError) as excinfo:
		del exobj.exceptions_db
	assert excinfo.value.message == "can't delete attribute"
	# Test contents
	tdata_in = exobj.exceptions_db
	if (not tdata_in) or (len(tdata_in) != 3):
		assert False
	tdata_out = list()
	for erec in tdata_in:
		if erec['name'].endswith('test_exh.test_exceptions_db.func4'):
			name = 'test_exh.test_exceptions_db.func4'
		elif erec['name'].endswith('test_exh.test_exceptions_db.func5'):
			name = 'test_exh.test_exceptions_db.func5'
		else:
			assert False
		tdata_out.append({'name':name, 'data':erec['data']})
	assert sorted(tdata_out) == sorted([{'name':'test_exh.test_exceptions_db.func4', 'data':'RuntimeError (This is exception #1)'},
										{'name':'test_exh.test_exceptions_db.func5', 'data':'ValueError (This is exception #2, *[result]*)'},
		                                {'name':'test_exh.test_exceptions_db.func5', 'data':'TypeError (This is exception #3)'}])

def test_callables_db():
	""" Test callables_db property """
	# Function definitions
	def func6(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exception', RuntimeError, 'This is an exception')
		return exobj
	# Actual tests
	exobj = func6(putil.exh.ExHandle())
	# Actual contents of what is returned should be checked in pinspect module
	assert exobj.callables_db is not None
	# Test that property cannot be deleted
	with pytest.raises(AttributeError) as excinfo:
		del exobj.callables_db
	assert excinfo.value.message == "can't delete attribute"

def test_callables_separator():
	""" Test callables_separator property """
	exobj = putil.exh.ExHandle()
	# Actual contents of what is returned should be checked in pinspect module
	assert exobj.callables_separator == '/'
	# Test that property cannot be deleted
	with pytest.raises(AttributeError) as excinfo:
		del exobj.callables_separator
	assert excinfo.value.message == "can't delete attribute"

def test_str():
	""" Test str() function """
	# Functions definition
	def func7(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exception7', RuntimeError, 'This is exception #7')
		exobj.raise_exception_if('my_exception7', False)
	def func8(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exception8', ValueError, 'This is exception #8, *[fname]*')
		exobj.add_exception('my_exception9', TypeError, 'This is exception #9')
	exobj = putil.exh.ExHandle()
	func7(exobj)
	func8(exobj)
	# Actual tests
	str_in = str(exobj).split('\n\n')
	str_out = list()
	for str_element in str_in:
		str_list = str_element.split('\n')
		if str_list[0].endswith('/my_exception7'):
			str_list[0] = 'Name....: test_exh.test_str.func7/my_exception7'
		elif str_list[0].endswith('/my_exception8'):
			str_list[0] = 'Name....: test_exh.test_str.func8/my_exception8'
		elif str_list[0].endswith('/my_exception9'):
			str_list[0] = 'Name....: test_exh.test_str.func8/my_exception9'
		if str_list[1].endswith('test_exh.test_str.func7'):
			str_list[1] = 'Function: test_exh.test_str.func7'
		elif str_list[1].endswith('test_exh.test_str.func8'):
			str_list[1] = 'Function: test_exh.test_str.func8'
		str_out.append('\n'.join(str_list))
	#
	str_check = list()
	str_check.append('Name....: test_exh.test_str.func7/my_exception7\nFunction: test_exh.test_str.func7\nType....: RuntimeError\nMessage.: This is exception #7\nChecked.: True')
	str_check.append('Name....: test_exh.test_str.func8/my_exception8\nFunction: test_exh.test_str.func8\nType....: ValueError\nMessage.: This is exception #8, *[fname]*\nChecked.: False')
	str_check.append('Name....: test_exh.test_str.func8/my_exception9\nFunction: test_exh.test_str.func8\nType....: TypeError\nMessage.: This is exception #9\nChecked.: False')
	assert sorted(str_out) == sorted(str_check)

def test_copy():
	""" Test __copy__() magic method """
	# Functions definition
	def funca(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exceptionA', RuntimeError, 'This is exception #A')
	def funcb(exobj):	#pylint: disable=C0111,W0612
		exobj.add_exception('my_exceptionB', ValueError, 'This is exception #B')
		exobj.add_exception('my_exceptionC', TypeError, 'This is exception #C')
	source_obj = putil.exh.ExHandle()
	funca(source_obj)
	funcb(source_obj)
	# Actual tests
	dest_obj = copy.copy(source_obj)
	assert (source_obj._ex_dict == dest_obj._ex_dict) and (id(source_obj._ex_dict) != id(dest_obj._ex_dict))
	assert (source_obj._callables_obj == dest_obj._callables_obj) and (id(source_obj._callables_obj) != id(dest_obj._callables_obj))
