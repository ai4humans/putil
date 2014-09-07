# -*- coding: utf-8 -*-
# pylint: disable=W0212,C0111
# tree.py
# Copyright (c) 2014 Pablo Acosta-Serafini
# See LICENSE for details


import putil.check

###
# Node name custom pseudo-type
###
class NodeName(object):	#pylint: disable=R0903
	""" Hierarchical node name data type class """
	def includes(self, test_obj):	#pylint: disable=R0201,W0613
		"""	Test that an object belongs to the pseudo-type """
		return False if (not isinstance(test_obj, str)) or (isinstance(test_obj, str) and (' ' in test_obj)) else all([element.strip() != '' for element in test_obj.strip().split('.')])

	def istype(self, test_obj):	#pylint: disable=R0201
		"""	Checks to see if object is of the same class type """
		return isinstance(test_obj, str)

	def exception(self, param_name):	#pylint: disable=R0201,W0613
		"""	Returns a suitable exception message """
		exp_dict = dict()
		exp_dict['type'] = ValueError
		exp_dict['msg'] = 'Argument `{0}` is not a valid node name'.format(param_name)
		return exp_dict
putil.check.register_new_type(NodeName, 'Hierarchical node name')


class Tree(object):	#pylint: disable=R0903
	"""
	Provides basic data tree functionality

	:rtype: :py:class:`putil.tree.Tree()` object
	"""
	def __init__(self):	#pylint: disable=R0913
		self._db = dict()
		self._root = None
		self._vertical = unichr(0x2502)
		self._vertical_and_right = unichr(0x251C)
		self._up_and_right = unichr(0x2514)
		#{'name':{'parent':None, 'children':None, 'data':data}}

	def __str__(self):
		u"""
		String with the tree structure pretty printed as a character-based tree structure. Only node names are shown, nodes with data are marked with an asterisk (*). For example:

			>>> import putil.tree
			>>> tobj = putil.tree.Tree()
			>>> tobj.add([
			...		{'name':'root.branch1', 'data':5},
			...		{'name':'root.branch2', 'data':None},
			...		{'name':'root.branch1.leaf1', 'data':None},
			...		{'name':'root.branch1.leaf2', 'data':'Hello world!'}
			... ])
			>>> print str(tobj)
			root
			├branch1 (*)
			│├leaf1
			│└leaf2 (*)
			└branch2

		:rtype: Unicode string
		"""
		return self._prt(name=self.root_name, lparent=-1, sep='', pre1='', pre2='').encode('utf-8')

	def _collapse_node(self, name):
		""" Collapse a single node """
		while True:
			node = self._db[name]
			if (len(node['children']) == 1) and (not node['data']):
				child_name = node['children'][0]
				self._db[child_name]['parent'] = node['parent']
				self._db[self._db[name]['parent']]['children'].remove(name)
				self._db[self._db[name]['parent']]['children'] = sorted(self._db[self._db[name]['parent']]['children']+[child_name])
				del self._db[name]
				name = child_name
			else:
				break
		node = self._db[name]
		for name in node['children'][:]:
			self._collapse_node(name)

	def _get_nodes(self):	#pylint: disable=C0111
		return None if not self._db else sorted(self._db.keys())

	def _get_root_node(self):	#pylint: disable=C0111
		return None if not self.root_name else self.get_node(self.root_name)

	def _get_root_name(self):	#pylint: disable=C0111
		return self._root

	def _node_in_tree(self, name):	#pylint: disable=C0111
		if name not in self._db:
			raise RuntimeError('Node {0} not in tree'.format(name))

	def _prt(self, name, lparent, sep, pre1, pre2):	#pylint: disable=C0111,R0913,R0914
		# Characters from http://www.unicode.org/charts/PDF/U2500.pdf
		node_name = name[lparent+1:]
		#node_name = name.split('.')[-1]
		children = self._db[name]['children']
		ncmu = len(children)-1
		plist1 = ncmu*[self._vertical_and_right]+[self._up_and_right]
		plist2 = ncmu*[self._vertical]+[' ']
		slist = (ncmu+1)*[sep+pre2]
		dmark = ' (*)' if self._db[name]['data'] else ''
		return '\n'.join([u'{0}{1}{2}{3}'.format(sep, pre1, node_name, dmark)]+[self._prt(child, len(name), sep=schar, pre1=p1, pre2=p2) for child, p1, p2, schar in zip(children, plist1, plist2, slist)])

	def _rnode(self, root, name, hierarchy):	#pylint: disable=C0111,R0913,R0914
		suffix = name[len(root):]
		new_suffix = suffix.replace('.'+hierarchy, '').replace('..', '.')
		new_name = root+new_suffix
		if new_name != name:
			if not self.in_tree(new_name):
				self._db[new_name] = self._db[name].copy()
				self._db[self._db[name]['parent']]['children'] = sorted(list(set([child for child in self._db[self._db[name]['parent']]['children'] if child != name]+[new_name])))
			else:
				if self._db[name]['data']:
					raise RuntimeError('Hierarchy {0} cannot be deleted'.format(hierarchy))
				if self._db[name]['parent'] == new_name:
					self._db[self._db[name]['parent']]['children'] = sorted(list(set([child for child in self._db[self._db[name]['parent']]['children'] if child != name])))
				new_children = sorted(self._db[new_name]['children']+self._db[name]['children'])
				if len(new_children) != len(set(new_children)):
					raise RuntimeError('Inconsitency when deleting hierarchy')
				self._db[new_name]['children'] = new_children
			for child in self.get_children(name):
				self._db[child]['parent'] = new_name
			del self._db[name]
		for child in self.get_children(new_name):
			self._rnode(root, child, hierarchy)

	def _set_root_name(self, name):	#pylint: disable=C0111
		self._root = name

	def _split_node_name(self, name):	#pylint: disable=C0111,R0201
		return [element.strip() for element in name.strip().split('.')]

	@putil.check.check_argument(putil.check.PolymorphicType([{'name':NodeName(), 'data':putil.check.Any()}, putil.check.ArbitraryLengthList({'name':NodeName(), 'data':putil.check.Any()})]))
	def add(self, nodes):
		"""
		Add nodes to tree

		:param	nodes: Node(s) to add. Each dictionary must contain these exactly two entries, **name** (*string*) node name, and **data** (*any* or None) node data. If there are several list elements that refer to the same \
		node the resulting node data is a list with all the data of the elements that have the same node name in addition to any existing data if the node is already present in the tree list element(s) that refer to an existing node.
		:type	nodes: dictionary or list of dictionaries
		:raises:
		 * TypeError (Argument `nodes` is of the wrong type)

		 * ValueError (Illegal node name *[node_name]*)
		"""
		nodes = nodes if isinstance(nodes, list) else [nodes]
		if not self.root_name:
			self._set_root_name(nodes[0]['name'].split('.')[0].strip())
			self._db[self.root_name] = {'parent':'', 'children':list(), 'data':list()}
		for node_dict in nodes:
			name = node_dict['name']
			data = node_dict['data']
			if not self.in_tree(name):
				hierarchy = self._split_node_name(name)
				if hierarchy[0] != self.root_name:
					raise ValueError('Illegal node name: {0}'.format(name))
				for num in range(len(hierarchy)):
					child = '.'.join(hierarchy[:num+1])
					if not self.in_tree(child):
						parent = '.'.join(self._split_node_name(child)[:-1])
						self._db[child] = {'parent':parent, 'children':list(), 'data':list()}
						self._db[parent]['children'] = list(sorted(set(self._db[parent]['children']+[child])))
			data = data if isinstance(data, list) and (len(data) > 0) else (list() if isinstance(data, list) else [data])
			self._db[name]['data'] = self._db[name]['data']+data

	@putil.check.check_argument(NodeName())
	def collapse(self, name):
		""" Compress nodes that have no data """
		self._node_in_tree(name)
		for child in self._db[name]['children'][:]:
			self._collapse_node(child)

	def _get_subtree(self, name):
		if self.is_leaf(name):
			return [name]
		children = self.get_children(name)
		ret = [name]
		for child in children:
			ret += self._get_subtree(child)
		return ret

	@putil.check.check_argument(putil.check.PolymorphicType([NodeName(), putil.check.ArbitraryLengthList(NodeName())]))
	def delete(self, nodes):
		"""
		Delete nodes (and their sub-trees) from tree

		:param	nodes: Node(s) to delete
		:type	nodes: string or list of strings
		:raises:
		 * TypeError (Argument `nodes` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[node_name]* not in tree)
		"""
		nodes = nodes if isinstance(nodes, list) else [nodes]
		for node in nodes:
			self._node_in_tree(node)
			parent = self.get_node(node)['parent']
			# Delete link to parent (if not root node)
			del_list = self._get_subtree(node)
			if parent:
				self._db[parent]['children'] = [child for child in self._db[parent]['children'] if child != node]
			# Delete children (sub-tree)
			for child in del_list:
				del self._db[child]
			if not len(self._db):
				self._root = None

	@putil.check.check_argument(NodeName())
	def get_node(self, name):	#pylint: disable=C0111
		"""
		Get tree node in the form of a dictionary with three keys:
		 * *parent* (*string*) Parent node name, *''* if not is root

		 * *children* (*list*) Node names, empty list if node is a leaf

		 * *data* (*list*) Node data, empty list if node contains no data

		:param	name: Node name
		:type	name: string
		:rtype: dictionary
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return self._db[name]

	@putil.check.check_argument(NodeName())
	def get_node_parent(self, name):	#pylint: disable=C0111
		"""
		Retrieves parent structure of a node. See :py:meth:`putil.tree.Tree.get_node()` for details about returned dictionary.

		:param	name: Child node name
		:type	name: string
		:rtype: dictionary
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return self._db[self._db[name]['parent']] if not self.is_root(name) else {}

	@putil.check.check_argument(NodeName())
	def get_children(self, name):	#pylint: disable=C0111
		"""
		Retrieves children of a node

		:param	name: Node name
		:type	name: string
		:rtype	data: listg of strings
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return sorted(self._db[name]['children'])

	@putil.check.check_argument(NodeName())
	def get_data(self, name):	#pylint: disable=C0111
		"""
		Get node data

		:param	name: Node name
		:type	name: string
		:type	data: any type or list of any type
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return self._db[name]['data']

	@putil.check.check_argument(NodeName())
	def in_tree(self, name):
		"""
		Search tree for a paticular node

		:param	name: Node name to search for
		:type	name: string
		:rtype	data: boolean
		:raises: TypeError (Argument `name` is of the wrong type)
		"""
		return name in self._db

	@putil.check.check_argument(NodeName())
	def is_root(self, name):	#pylint: disable=C0111
		"""
		Root node flag, *True* if node is the root node (node with no ancestors), *False* otherwise

		:param	name: Node name
		:type	name: string
		:rtype: boolean
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return not self._db[name]['parent']

	@putil.check.check_argument(NodeName())
	def is_leaf(self, name):	#pylint: disable=C0111
		"""
		Leaf node flag, *True* if node is a leaf node (node with no children), *False* otherwise

		:param	name: Node name
		:type	name: string
		:rtype: boolean
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		return not self._db[name]['children']

	@putil.check.check_argument(NodeName())
	def make_root(self, name):	#pylint: disable=C0111
		"""
		Makes a sub-node the root node of tree

		:param	name: Node name
		:type	name: string
		:rtype: boolean
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `name` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		dlist = [key for key in self.nodes if key.find(name) != 0]
		for key in dlist:
			del self._db[key]
		self._db[name]['parent'] = ''
		self._root = name

		return not self._db[name]['children']

	@putil.check.check_argument(NodeName())
	def print_node(self, name):	#pylint: disable=C0111
		"""
		Prints node information

		:param	name: Node name
		:type	name: string
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `nodes` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		node = self.get_node(name)
		children = [self._split_node_name(child)[-1] for child in node['children']] if node['children'] else node['children']
		data = node['data'][0] if node['data'] and (len(node['data']) == 1) else node['data']
		return 'Name: {0}\nParent: {1}\nChildren: {2}\nData: {3}'.format(name, node['parent'] if node['parent'] else None, ', '.join(children) if children else None, data if data else None)


	@putil.check.check_arguments({'name':NodeName(), 'hierarchy':NodeName()})
	def remove_hierarchy(self, name, hierarchy):	#pylint: disable=C0111
		"""
		Get node data

		:param	name:		Root node of sub-tree to remove hierarchy from
		:type	name:		string
		:param	hierarchy:	Hierarchy to remove from node names in sub-tree
		:type	hierarhcy:	string
		:raises:
		 * TypeError (Argument `name` is of the wrong type)

		 * ValueError (Argument `name` is not a valid node name)

		 * TypeError (Argument `hierarchy` is of the wrong type)

		 * ValueError (Argument `hierarchy` is not a valid node name)

		 * RuntimeError (Node *[name]* not in tree)
		"""
		self._node_in_tree(name)
		# REMOVE print 'Entry function children {0}'.format(self.get_children(name))
		for child in self.get_children(name):
			# REMOVE print 'Entry function child {0}'.format(child)
			self._rnode(name, child, hierarchy)

	@putil.check.check_argument(NodeName())
	def remove_prefix(self, prefix):
		index = self.root_name.find(prefix)
		if index != 0:
			raise ValueError('Illegal prefix')
		cstart = len(prefix)+1
		ndb = dict()
		for key in self._db.keys():
			new_key = key[cstart:]
			self._db[key]['parent'] = self._db[key]['parent'] if not self._db[key]['parent'] else self._db[key]['parent'][cstart:]
			self._db[key]['children'] = sorted([child[cstart:] for child in self._db[key]['children']])
			ndb[new_key] = self._db[key].copy()
			del self._db[key]
		self._db = ndb
		self._set_root_name(self.root_name[cstart:])

	# Managed attributes
	nodes = property(_get_nodes, None, None, doc='Tree nodes')
	"""
	Name of all tree nodes, *None* if an empty tree

	:rtype: list or None
	"""	#pylint: disable=W0105

	root_node = property(_get_root_node, None, None, doc='Tree root node')
	"""
	Tree root node or *None* if :py:class:`putil.tree.Tree()` object has no nodes. See :py:meth:`putil.tree.Tree.get_node()` for details about returned dictionary.

	:rtype: dictionary or None
	"""	#pylint: disable=W0105

	root_name = property(_get_root_name, None, None, doc='Tree root node name')
	"""
	Tree root node name, *None* if :py:class:`putil.tree.Tree()` object has no nodes.

	:rtype: string or None
	"""	#pylint: disable=W0105

@putil.check.check_arguments({'tree':Tree, 'name':NodeName()})
def search_for_node(tree, name):
	"""
	Searches tree node and its children for a particular node name, which can be specified hierarchically. Returns *None* if node name not found.

	:param	tree:	Tree to search
	:type	tree:	:py:class:`putil.tree.Tree()` object
	:param	name:	Node name to search for (case sensitive). Levels of hierarchy are denoted by '.', for example 'root.branch1.leaf2'.
	:type	name:	string
	:rtype:	same as :py:meth:`putil.tree.Tree.get_node()` or *None*
	:raises:
	 * TypeError (Argument `tree` is of the wrong type)

	 * TypeError (Argument `name` is of the wrong type)
	"""
	return None if not tree.in_tree(name) else tree.get_node(name)

@putil.check.check_argument(putil.check.PolymorphicType([{'node':NodeName(), 'data':putil.check.Any()}, putil.check.ArbitraryLengthList({'node':NodeName(), 'data':putil.check.Any()})]))
def build_trees(nodes):
	"""
	Build tree objects

	:param	nodes:	Tree information. Each dictionary must contain only two keys, *name*, with a (hierarchical) node name, and *data*, with the node data. Multiple entries for a given node name may exist, \
	and the resulting node data will be a list whose elements are the values of the *data* key of all dictionaries in **tree_info** that share the same node name
	:type	nodes:	dictionary or list of dictionaries.
	:rtype:	:py:class:`putil.tree.TreeNode()` object or list of :py:class:`putil.tree.TreeNode()` objects if there are multiple root nodes
	:raises:
	 * TypeError (Argument `tree_info` is of the wrong type)

	 * Same as :py:attr:`putil.tree.TreeNode.name`
	"""
	roots = list()
	nodes = nodes if isinstance(nodes, list) else [nodes]
	for node in nodes:
		root_name = [element.strip() for element in node['name'].strip().split('.')][0]
		# Find or create tree to add nodes and data to
		for tobj in roots:
			if tobj.root_name == root_name:
				break
		else:
			tobj = Tree()
			roots.append(tobj)
		tobj.add(node)
	return roots
