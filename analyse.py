from graph_tool.all import *

"""
g = load_graph("astronomy_answers.graphml")
a= [node for node in g.vertices() if node.out_degree() + node.in_degree() < 3]
g.remove_vertex(a)
bv, be = betweenness(g)"""

g = load_graph("beer.graphml")
print(1)
a= [node for node in g.vertices() if node.out_degree() + node.in_degree() < 3]
print(2)
bv, be = betweenness(g)
