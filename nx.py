class DiGraph():
	"""docstring for DiGraph"""
	def __init__(self):
		self._nodes = []
		self._edges = []

	def add_node(self, node, shape='', label='', style='outline', fillcolor='white'):
		if node not in self._nodes:
			self._nodes += [node]

	def remove_node(self, node):
		if node in self._nodes:
			self._nodes.remove(node)
			def not_in_edge((x,y)): return x != node and y != node
			self._edges = filter(not_in_edge, self._edges)

	def add_edge(self, n1, n2, label='', dir='both', color='black'):
		if (n1, n2) not in self._edges:
			self._edges += [(n1, n2)]

	def successors(self, node):
		return [n for (x, n) in self._edges if x == node]

	def predecessors(self, node):
		return [n for (n, x) in self._edges if x == node]

	def nodes(self):
		return self._nodes

	def edges(self):
		return self._edges

	def is_isolate(self, node):
		neighbourhood = [e for (e,x) in self._edges if x == node] + \
						[e for (x,e) in self._edges if x == node]
		return neighbourhood == []
	
	# @classmethod
	# def is_isolate(cls, graph, node):
	# 	return graph.is_isolate(node)

if __name__ == '__main__':
	g = DiGraph()
	g.add_node(1)
	g.add_node(2)
	g.add_node(3)
	g.add_edge(1,2)
	print g.is_isolate(1)
	print g.is_isolate(2)
	print g.is_isolate(3)


# EOF