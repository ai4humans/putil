﻿# test_test.py
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=W0212,C0111

import pytest

import putil.test


def test_exception_type_str():
	""" Test exception_type_str() function """
	class MyException(Exception):
		pass
	assert putil.test.exception_type_str(RuntimeError) == 'RuntimeError'
	assert putil.test.exception_type_str(Exception) == 'Exception'
	assert putil.test.exception_type_str(MyException) == 'MyException'

def test_assert_exception():
	""" Test assert_exception() function """
	def func1(par1):
		if par1 == 1:
			raise RuntimeError('Exception 1')
		elif par1 == 2:
			raise ValueError('The number 1234 is invalid')
	putil.test.assert_exception(func1, {'par1':1}, RuntimeError, 'Exception 1')
	with pytest.raises(AssertionError):
		putil.test.assert_exception(func1, {'par1':0}, RuntimeError, 'Exception 1')
	putil.test.assert_exception(func1, {'par1':2}, ValueError, r'The number \d+ is invalid')
	with pytest.raises(AssertionError):
		putil.test.assert_exception(func1, {'par1':1}, IOError, 'Exception 5')
	with pytest.raises(AssertionError):
		putil.test.assert_exception(func1, {'par1':2}, ValueError, 'Exception message is wrong')
