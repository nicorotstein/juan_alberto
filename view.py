import networkx as nx
# import matplotlib
# import pydot

class Drawer():

	@classmethod
	def draw_graph(cls, graph, filename):
		nx.draw(graph)
		nx.write_gexf(graph, 'data/' + filename + '.gexf')
		print "----------> number of nodes in", filename + ':', len(graph)
		
# EOF