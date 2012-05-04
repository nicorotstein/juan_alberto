import networkx as nx
# import matplotlib
# import pydot

class Drawer():

	@classmethod
	def draw_dotgraph(cls, graph, filename):
		nx.draw(graph)
		# nx.write_gexf(graph, 'data/' + filename + '.gexf')
		nx.write_dot(graph, 'data/' + filename + '.dot')
		print "----------> number of nodes in", filename + ':', len(graph)
		
	@classmethod
	def draw_gexfgraph(cls, graph_container, filename):
		gexf_file = open('data/' + filename + '.gexf', 'w')
		graph_container.write(gexf_file)
		
# EOF