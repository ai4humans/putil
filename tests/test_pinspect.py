﻿# test_pinspect.py
# Copyright (c) 2013-2015 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=W0212

"""
putil.pintrospect unit tests
"""

import os
import sys
import copy
import mock
import types
import random
import string
import inspect

import putil.test
import putil.pinspect

def test_object_is_module():
	""" Test object_is_module() function """
	test_list = list()
	test_list.append(putil.pinspect.is_object_module(5) == False)
	test_list.append(putil.pinspect.is_object_module(sys.modules['putil.pinspect']) == True)
	assert test_list == [True]*len(test_list)


def test_get_module_name():
	""" Test get_module_name() function """
	test_list = list()
	test_list.append(putil.test.trigger_exception(putil.pinspect.get_module_name, {'module_obj':5}, TypeError, 'Argument `module_obj` is not a module object'))
	mock_module_obj = types.ModuleType('mock_module_obj', 'Mock module')
	test_list.append(putil.test.trigger_exception(putil.pinspect.get_module_name, {'module_obj':mock_module_obj}, RuntimeError, 'Module object `mock_module_obj` could not be found in loaded modules'))
	test_list.append(putil.pinspect.get_module_name(sys.modules['putil.pinspect']) == 'putil.pinspect')
	test_list.append(putil.pinspect.get_module_name(sys.modules['putil']) == 'putil')
	assert test_list == [True]*len(test_list)


def test_get_package_name():
	""" Test get_package_name() function """
	test_list = list()
	sys.modules['no_pkg.module'] = types.ModuleType('no_pkg.module', 'Mock module')
	test_list.append(putil.test.trigger_exception(putil.pinspect.get_package_name, {'module_obj':sys.modules['no_pkg.module']}, RuntimeError, 'Loaded package root could not be found'))
	test_list.append(putil.pinspect.get_package_name(sys.modules['putil.pinspect']) == 'putil')
	assert test_list == [True]*len(test_list)


def test_is_magic_method():
	""" Test is_magic_method() function """
	test_list = list()
	test_list.append(putil.pinspect.is_magic_method('func_name') == False)
	test_list.append(putil.pinspect.is_magic_method('_func_name_') == False)
	test_list.append(putil.pinspect.is_magic_method('__func_name__') == True)
	assert test_list == [True]*len(test_list)


def test_loaded_package_modules():
	""" Test loaded_package_modules() function """
	test_list = list()
	module_name_list = ['check', 'eng', 'misc', 'pinspect', 'test']
	modules_obj_list = set([sys.modules['putil']]+[sys.modules['putil.{0}'.format(module_name)] for module_name in module_name_list])
	test_list.append(set(putil.pinspect.loaded_package_modules(sys.modules['putil'])) == modules_obj_list)
	test_list.append(set(putil.pinspect.loaded_package_modules(sys.modules['putil.pinspect'])) == modules_obj_list)
	assert test_list == [True]*len(test_list)

def test_replace_tabs():
	""" Test _replace_tabs() function """
	test_list = list()
	test_list.append(putil.pinspect._replace_tabs('    def func()') == '    def func()')
	for snum in range(0, 8):
		test_list.append(putil.pinspect._replace_tabs((' '*snum)+'\tdef func()') == (' '*8)+'def func()')
	test_list.append(putil.pinspect._replace_tabs('   \t   def func()') == (' '*8)+'   def func()')
	test_list.append(putil.pinspect._replace_tabs('   \t  \t def func()') == (' '*16)+' def func()')
	test_list.append(putil.pinspect._replace_tabs('\f   \t  \t def func()') == (' '*16)+' def func()')
	assert test_list == [True]*len(test_list)

def test_callables():	# pylint: disable=R0915
	""" Test callables class """
	def mock_get_code_id(obj, file_name=None, offset=0):	#pylint: disable=W0612,W0613
		""" Mock function to trigger exception related to callable not found in database """
		return (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)), random.random())
	test_list = list()
	obj = putil.pinspect.Callables()
	test_list.append(obj.callables_db == dict())
	test_list.append(obj.reverse_callables_db == dict())
	test_list.append(putil.test.trigger_exception(obj.trace, {'obj':None}, TypeError, 'Argument `obj` is not valid'))
	test_list.append(putil.test.trigger_exception(obj.trace, {'obj':'not_an_object'}, TypeError, 'Argument `obj` is not valid'))
	sys.path.append(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'support'))
	import pinspect_support_module_1	#pylint: disable=F0401,W0612
	obj.trace(sys.modules['pinspect_support_module_1'])
	ref_list = list()
	ref_list.append('Modules:')
	ref_list.append('   pinspect_support_module_1')
	ref_list.append('   pinspect_support_module_2')
	ref_list.append('   pinspect_support_module_3')
	ref_list.append('   pinspect_support_module_4')
	ref_list.append('Classes:')
	ref_list.append('   pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators')
	ref_list.append('   pinspect_support_module_1.ClassWithPropertyDefinedViaFunction')
	ref_list.append('   pinspect_support_module_1.ClassWithPropertyDefinedViaLambdaAndEnclosure')
	ref_list.append('   pinspect_support_module_1.class_enclosing_func.ClosureClass')
	ref_list.append('   pinspect_support_module_1.class_enclosing_func.ClosureClass.sub_enclosure_method.SubClosureClass')
	ref_list.append('   pinspect_support_module_1.class_namespace_test_enclosing_func.NamespaceTestClosureClass')
	ref_list.append('   pinspect_support_module_2.SimpleClass')
	ref_list.append('   pinspect_support_module_3.another_class_enclosing_func.FromImportClosureClass')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.__call__: meth (104)')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.__init__: meth (101)')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.encprop: prop')
	ref_list.append('   fget: pinspect_support_module_1.simple_property_generator.fget')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp: prop')
	ref_list.append('   fset: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(setter)')
	ref_list.append('   fdel: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(deleter)')
	ref_list.append('   fget: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(getter)')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(deleter): meth (118)')
	ref_list.append('   fdel of: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(getter): meth (107)')
	ref_list.append('   fget of: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp(setter): meth (112)')
	ref_list.append('   fset of: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.temp')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaFunction.__init__: meth (73)')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._deleter_func: meth (89)')
	ref_list.append('   fdel of: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction.state')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._getter_func: meth (85)')
	ref_list.append('   fget of: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction.state')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._setter_func: meth (76)')
	ref_list.append('   fset of: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction.state')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaFunction.state: prop')
	ref_list.append('   fset: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._setter_func')
	ref_list.append('   fdel: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._deleter_func')
	ref_list.append('   fget: pinspect_support_module_1.ClassWithPropertyDefinedViaFunction._getter_func')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaLambdaAndEnclosure.__init__: meth (52)')
	ref_list.append('pinspect_support_module_1.ClassWithPropertyDefinedViaLambdaAndEnclosure.clsvar: prop')
	ref_list.append('   fset: pinspect_support_module_2.setter_enclosing_func.setter_closure_func')
	ref_list.append('   fget: pinspect_support_module_1.ClassWithPropertyDefinedViaLambdaAndEnclosure.clsvar.fget_lambda')
	ref_list.append('pinspect_support_module_1.class_enclosing_func: func (19)')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.__init__: meth (24)')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.get_obj: meth (28)')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.obj: prop')
	ref_list.append('   fset: pinspect_support_module_1.class_enclosing_func.ClosureClass.set_obj')
	ref_list.append('   fdel: pinspect_support_module_3.deleter')
	ref_list.append('   fget: pinspect_support_module_2.getter_func_for_closure_class')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.set_obj: meth (32)')
	ref_list.append('   fset of: pinspect_support_module_1.class_enclosing_func.ClosureClass.obj')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.sub_enclosure_method: meth (36)')
	ref_list.append('pinspect_support_module_1.class_enclosing_func.ClosureClass.sub_enclosure_method.SubClosureClass.__init__: meth (40)')
	ref_list.append('pinspect_support_module_1.class_namespace_test_enclosing_func: func (129)')
	ref_list.append('pinspect_support_module_1.class_namespace_test_enclosing_func.NamespaceTestClosureClass.__init__: meth (133)')
	ref_list.append('pinspect_support_module_1.class_namespace_test_enclosing_func.NamespaceTestClosureClass.nameprop: prop')
	ref_list.append('   fget: pinspect_support_module_4.another_property_action_enclosing_function.fget')
	ref_list.append('pinspect_support_module_1.dummy_decorator: func (58)')
	ref_list.append('pinspect_support_module_1.module_enclosing_func: func (11)')
	ref_list.append('pinspect_support_module_1.module_enclosing_func.module_closure_func: func (13)')
	ref_list.append('pinspect_support_module_1.simple_property_generator: func (63)')
	ref_list.append('pinspect_support_module_1.simple_property_generator.fget: func (65)')
	ref_list.append('   fget of: pinspect_support_module_1.ClassWithPropertyDefinedViaDecorators.encprop')
	ref_list.append('   fget of: pinspect_support_module_3.another_class_enclosing_func.FromImportClosureClass.encprop')
	ref_list.append('pinspect_support_module_2.SimpleClass.__init__: meth (17)')
	ref_list.append('pinspect_support_module_2.SimpleClass.get_mobj: meth (21)')
	ref_list.append('   fget of: pinspect_support_module_2.SimpleClass.mobj')
	ref_list.append('pinspect_support_module_2.SimpleClass.mobj: prop')
	ref_list.append('   fset: pinspect_support_module_2.SimpleClass.set_mobj')
	ref_list.append('   fget: pinspect_support_module_2.SimpleClass.get_mobj')
	ref_list.append('pinspect_support_module_2.SimpleClass.set_mobj: meth (25)')
	ref_list.append('   fset of: pinspect_support_module_2.SimpleClass.mobj')
	ref_list.append('pinspect_support_module_2.getter_func_for_closure_class: func (32)')
	ref_list.append('   fget of: pinspect_support_module_1.class_enclosing_func.ClosureClass.obj')
	ref_list.append('pinspect_support_module_2.setter_enclosing_func: func (7)')
	ref_list.append('pinspect_support_module_2.setter_enclosing_func.setter_closure_func: func (9)')
	ref_list.append('   fset of: pinspect_support_module_1.ClassWithPropertyDefinedViaLambdaAndEnclosure.clsvar')
	ref_list.append('pinspect_support_module_3.another_class_enclosing_func: func (12)')
	ref_list.append('pinspect_support_module_3.another_class_enclosing_func.FromImportClosureClass.__init__: meth (17)')
	ref_list.append('pinspect_support_module_3.another_class_enclosing_func.FromImportClosureClass.encprop: prop')
	ref_list.append('   fget: pinspect_support_module_1.simple_property_generator.fget')
	ref_list.append('pinspect_support_module_3.another_property_action_enclosing_function: func (25)')
	ref_list.append('pinspect_support_module_3.another_property_action_enclosing_function.fget: func (27)')
	ref_list.append('pinspect_support_module_3.deleter: func (7)')
	ref_list.append('   fdel of: pinspect_support_module_1.class_enclosing_func.ClosureClass.obj')
	ref_list.append('pinspect_support_module_4.another_property_action_enclosing_function: func (7)')
	ref_list.append('pinspect_support_module_4.another_property_action_enclosing_function.fget: func (9)')
	ref_list.append('   fget of: pinspect_support_module_1.class_namespace_test_enclosing_func.NamespaceTestClosureClass.nameprop')
	ref_text = '\n'.join(ref_list)
	if str(obj) != ref_text:
		print str(obj)
		print '---[Differing lines]---'
		actual_list = str(obj).split('\n')
		for actual_line, ref_line in zip(actual_list, ref_list):
			if actual_line != ref_line:
				print 'Actual line...: {0}'.format(actual_line)
				print 'Reference line: {0}'.format(ref_line)
				break
		print '-----------------------'
		if len(actual_list) != len(ref_list):
			print '{0} longer than {1}'.format('Actual' if len(actual_list) > len(ref_list) else 'Reference', 'reference' if len(actual_list) > len(ref_list) else 'actual')
			print_list = actual_list if len(actual_list) > len(ref_list) else ref_list
			print print_list[min([len(actual_list), len(ref_list)]):]
			print '-----------------------'
	test_list.append(str(obj) == ref_text)
	# Test that callables_db and reverse_callables_db are in sync
	congruence_flag = True
	for key, value in obj.callables_db.items():
		if value['code_id']:
			congruence_flag = obj.reverse_callables_db[value['code_id']] == key
			if not congruence_flag:
				break
	test_list.append(congruence_flag)
	# Test string and representation methods
	test_list.append(repr(obj) == "putil.pinspect.Callables([sys.modules['pinspect_support_module_1'], sys.modules['pinspect_support_module_2'], sys.modules['pinspect_support_module_3'], sys.modules['pinspect_support_module_4']])")
	test_list.append(str(putil.pinspect.Callables([sys.modules['pinspect_support_module_2'], sys.modules['pinspect_support_module_1']])) == ref_text)
	test_list.append(repr(putil.pinspect.Callables([sys.modules['pinspect_support_module_2'], sys.modules['pinspect_support_module_1']])) == \
				  "putil.pinspect.Callables([sys.modules['pinspect_support_module_1'], sys.modules['pinspect_support_module_2'], sys.modules['pinspect_support_module_3'], sys.modules['pinspect_support_module_4']])")
	test_list.append(repr(putil.pinspect.Callables()) == "putil.pinspect.Callables()")
	# Test exception raised when callable is not found in database (mainly to cover potential edge cases not considered during development)
	with mock.patch('putil.pinspect._get_code_id', side_effect=mock_get_code_id):
		test_list.append(putil.test.trigger_exception(putil.pinspect.Callables, {'obj':sys.modules['pinspect_support_module_2']}, RuntimeError, r'Attribute `([\w|\W]+)` of property `([\w|\W]+)` not found in callable database'))
	assert test_list == [True]*len(test_list)

def test_copy():
	""" Test __copy__() magic method """
	source_obj = putil.pinspect.Callables()
	import pinspect_support_module_1	#pylint: disable=F0401,W0612
	source_obj.trace(sys.modules['pinspect_support_module_1'])
	dest_obj = copy.copy(source_obj)
	test_list = list()
	test_list.append((source_obj._module_names == dest_obj._module_names) and (id(source_obj._module_names) != id(dest_obj._module_names)))
	test_list.append((source_obj._class_names == dest_obj._class_names) and (id(source_obj._class_names) != id(dest_obj._class_names)))
	test_list.append((source_obj._callables_db == dest_obj._callables_db) and (id(source_obj._callables_db) != id(dest_obj._callables_db)))
	test_list.append((source_obj._reverse_callables_db == dest_obj._reverse_callables_db) and (id(source_obj._reverse_callables_db) != id(dest_obj._reverse_callables_db)))
	assert test_list == [True]*len(test_list)

def test_eq():
	""" Test __eq__() magic method """
	obj1 = putil.pinspect.Callables()
	obj2 = putil.pinspect.Callables()
	obj3 = putil.pinspect.Callables()
	import pinspect_support_module_1	#pylint: disable=F0401,W0612
	import pinspect_support_module_2	#pylint: disable=F0401,W0612
	obj1.trace(sys.modules['pinspect_support_module_1'])
	obj2.trace(sys.modules['pinspect_support_module_2'])
	obj2.trace(sys.modules['pinspect_support_module_1'])
	obj3.trace(sys.modules['putil.test'])
	assert (obj1 == obj2) and (obj1 != obj3)
