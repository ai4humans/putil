﻿# exh.py
# Copyright (c) 2014 Pablo Acosta-Serafini
# See LICENSE for details

"""
Exception handling classes, methods, functions and constants
"""

import sys
import inspect

import putil.check
import putil.tree

class ExHandle(object):
	""" Exception handling class """
	def __init__(self, cls, func_name=None, ex_list=None):
		self._cls = cls
		self._trace_on = False
		self._trace_list, self._tobj, self._extable = None, None, None
		self._ex_list = list()
		if ((func_name is None) and (ex_list is not None)) or ((func_name is not None) and (ex_list is None)):
			raise RuntimeError('Arguments `func_name` and `ex_list` have to be either both defined or both undefined')
		if (func_name is not None) and (ex_list is not None):
			for obj in ex_list:
				obj['func'] = func_name
				obj['checked'] = False
			self._ex_list = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in ex_list)] # Remove duplicates

	def __str__(self):
		ret = ['Name....: {0}\nFunction: {1}\nType....: {2}\nMessage.: {3}\nChecked.: {4}'.format(ex['name'], ex['function'], self._ex_type_str(ex['type']), ex['msg'], ex['checked']) for ex in self._ex_list]
		return '\n\n'.join(ret)

	def _ex_type_str(self, extype):	#pylint: disable-msg=R0201
		""" Returns a string corresponding to the exception type """
		return str(extype)[str(extype).rfind('.')+1:str(extype).rfind("'")]

	def _format_msg(self, msg, edata):	#pylint: disable=R0201
		""" Substitute parameters in exception message """
		edata = edata if isinstance(edata, list) else [edata]
		for field in edata:
			if 'field' not in field:
				raise ValueError('Key `field` not in field definition')
			if 'value' not in field:
				raise ValueError('Key `value` not in field definition')
			if '*[{0}]*'.format(field['field']) not in msg:
				raise RuntimeError('Field {0} not in exception message'.format(field['field']))
			msg = msg.replace('*[{0}]*'.format(field['field']), field['value'])
		return msg

	def _tree_data(self):	#pylint: disable-msg=R0201
		""" Returns a list of dictionaries suitable to be used with putil.tree module """
		return [{'name':ex['function'], 'data':'{0} ({1})'.format(self._ex_type_str(ex['type']), ex['msg'])} for ex in self._ex_list]

	def ex_add(self, name, extype, exmsg):	#pylint: disable=R0913,R0914
		""" Add exception to database """
		func_name = self.get_func_name()
		self._ex_list.append({'name':self.get_ex_name(name), 'function':func_name, 'type':extype, 'msg':exmsg, 'checked':False})
		self._ex_list = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in self._ex_list)] # Remove duplicates

	def get_exception_by_name(self, name):
		""" Find exception object """
		exname = self.get_ex_name(name)
		for obj in self._ex_list:
			if obj['name'] == exname:
				return obj
		raise ValueError('Exception name {0} not found'.format(name))

	def get_ex_name(self, name):
		""" Returns hierarchical function name """
		func_name = self.get_func_name()
		return '{0}{1}{2}'.format(func_name, '.' if func_name is not None else '', name)

	def get_func_name(self):	#pylint: disable=R0201
		""" Get calling function name """
		# Stack frame is a tuple with the following items:
		# 0: the frame object
		# 1: the filename
		# 2: the line number of the current line
		# 3: the function name
		# 4: a list of lines of context from the source code
		# 5: the index of the current line within that list.
		frame_list = inspect.stack()
		func_name = ''
		fobj_found = False
		for frame_obj, file_name, _, fname, fcontext, findex in frame_list:
			if (('wrapper' in fname) and ('check.py' in file_name)) or ('exh.py' in file_name) or ('check.py' in file_name) or ((fcontext is None) and (findex is None) and fobj_found):
				pass
			elif fname != '<module>':
				func_name = get_func_calling_hierarchy(frame_obj)+('' if not func_name else '.')+func_name
				fobj_found = True
		return func_name

	def build_ex_tree(self):	#pylint: disable=R0912,R0914
		""" Builds exception tree """
		tree_data = self._tree_data()
		if not tree_data:
			raise RuntimeError('No trace information')
		self._tobj = putil.tree.Tree()
		# Build tree
		print 'Building tree'
		self._tobj.add(tree_data)
		# Collapse tree
		print 'Collapsing tree'
		self._tobj.collapse(self._tobj.root_name)
		node = self._tobj.root_name
		for node in self._tobj.nodes:
			if self._cls in node:
				break
		# Remove class hierarchy
		print 'Removing hierarchy {0}'.format(node)
		self._tobj.remove_hierarchy(node, self._cls)
		# Make class root node
		print 'Making {0} root'.format(node)
		self._tobj.make_root(node)
		index = node.find(self._cls)
		if index != 0:
			prefix = node[:index-1]
			print 'Removing prefix {0}'.format(prefix)
			self._tobj.remove_prefix(prefix)
		# Detect cross-usage
		print 'Detecting cross-usage'
		children = self._tobj.get_children(self._tobj.root_name)
		for child1 in children:
			grandchildren = self._tobj.get_children(child1)
			for grandchild in grandchildren:
				for child2 in children:
					if child1 != child2:
						name_grandchild = grandchild[len(child1)+1:]
						name_child = child2[len(self._cls)+1:]
						if name_child == name_grandchild:
							self._tobj.delete(grandchild)
							self._tobj.add({'name':child1, 'data':'Same as :py:{0}:`{1}`'.format('attr' if child2.split('.')[-1][:5] == '_set_' else 'meth', child2.replace('_set_', ''))})
							break
		# Condense exceptions to class methods nodes
		self._extable = dict()
		for child in children:
			exdesc_list = list()
			for name in self._tobj._get_subtree(child):	#pylint: disable=W0212
				exdesc_list += self._tobj.get_data(name)
			self._extable[child.replace(self._cls+'.', '').split('.')[0].strip().replace('_set_', '')] = exdesc_list
		# Sort exceptions with 'Same as [...]' at the end, and both 'sections' sorted alphabetically
		for key in self._extable:
			data = self._extable[key]
			bex = [exname for exname in data if 'Same as' not in exname]
			sex = [exname for exname in data if 'Same as' in exname]
			self._extable[key] = sorted(list(set(bex)))+sorted(list(set(sex)))
		# Recursively expand 'Same as [...] entries
		expanded_table = dict()
		for key in self._extable:
			expanded_table[key] = self._expand_same_ex_list(self._extable[key], start=True)
		# Remove exceptions that could be in 'Same as [...]' entry
		for key in self._extable:
			self._extable[key] = [member for member in self._extable[key] if member not in expanded_table[key]]

	def _expand_same_ex_list(self, data, start=False):
		""" Create exception list where the 'Same as [...]' entries have been replaced for the exceptions in the method/attribute they point to """
		ret = [ex_member for ex_member in data if ex_member.find('Same as') == -1] if not start else list()
		sex_members = [ex_member.split('.')[-1][:-1] for ex_member in data if ex_member.find('Same as') != -1]
		for member in sex_members:
			ret += self._extable[member]
		if sex_members:
			self._expand_same_ex_list(ret)
		return ret


	def print_ex_tree(self):
		""" Prints exception tree """
		print str(self._tobj)

	def print_ex_table(self):
		""" Prints exception table """
		if not self._extable:
			raise RuntimeError('No exception table data')
		print
		for child in sorted(self._extable.keys()):
			print 'Member: {0}'.format(child)
			for exname in self._extable[child]:
				print ' * {0}\n'.format(exname)
			print

	def _ptable(self, name):	#pylint: disable=C0111
		data = self._tobj.get_data(name)
		ret = 'Node: {0}\n{1}\n\n'.format(name, '\n'.join(sorted(data))) if data else ''
		for child in self._tobj.get_children(name):
			ret += self._ptable(child)
		return ret

	def raise_exception(self, name, **kargs):
		""" Raise exception by name """
		if (len(kargs) == 1) and ('edata' not in kargs):
			raise RuntimeError('Illegal keyword argument passed to raise_exception')
		if len(kargs) > 1:
			raise RuntimeError('Illegal keyword argument{0} passed to raise_exception'.format('s' if len(kargs)-(1 if 'edata' in kargs else 0) > 1 else ''))
		obj = self.get_exception_by_name(name)
		if len(kargs):
			raise obj['type'](self._format_msg(obj['msg'], kargs['edata']))
		else:
			raise obj['type'](obj['msg'])

	def raise_exception_if(self, name, condition, **kargs):
		""" Raise exception by name if condition is true """
		if (len(kargs) == 1) and ('edata' not in kargs):
			raise RuntimeError('Illegal keyword argument passed to raise_exception')
		if len(kargs) > 1:
			raise RuntimeError('Illegal keyword argument{0} passed to raise_exception'.format('s' if len(kargs)-(1 if 'edata' in kargs else 0) > 1 else ''))
		if condition:
			self.raise_exception(name, **kargs)
		self.get_exception_by_name(name)['checked'] = True


def get_func_calling_hierarchy2(func):
	""" Get class name of decorated function """
	# Stack frame is a tuple with the following items:
	# 0: the frame object
	# 1: the filename
	# 2: the line number of the current line
	# 3: the function name
	# 4: a list of lines of context from the source code
	# 5: the index of the current line within that list.
	funcname = func.__name__
	for fobj, _, _, fname, _, _ in inspect.stack():
		if fname == func.__name__:
			if 'self' in fobj.f_locals:
				modname = fobj.f_locals['self'].__module__
				clsname = fobj.f_locals['self'].__class__.__name__
				return '{0}.{1}.{2}'.format(modname, clsname, funcname)
			else:
				modname = sys.modules[func.__module__].__name__
				return '{0}.{1}'.format(modname, funcname)
	raise RuntimeError('Function {0} could not be found in stack'.format(func.__name__))

def get_func_calling_hierarchy(frame_obj):
	""" Get class name of decorated function """
	# Most of this code from pycallgraph/tracer.py of the Python Call Graph project (https://github.com/gak/pycallgraph/#python-call-graph)
	ret = list()
	code = frame_obj.f_code
	# Work out the module name
	module = inspect.getmodule(code)
	if module:
		module_name = module.__name__
		ret.append(module_name)
	else:
		if 'self' in frame_obj.f_locals:
			module_name = frame_obj.f_locals['self'].__module__
			ret.append(module_name)
		else:
			module_name = ''
	# Work out the class name
	try:
		class_name = frame_obj.f_locals['self'].__class__.__name__
		ret.append(class_name)
	except (KeyError, AttributeError):
		class_name = ''
	# Work out the current function or method
	func_name = code.co_name
	if func_name == '?':
		func_name = '__main__'
	ret.append(func_name)
	return '.'.join(ret)

