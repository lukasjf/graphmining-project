from graph_tool.all import *

"""
g = load_graph("astronomy_answers.graphml")
a= [node for node in g.vertices() if node.out_degree() + node.in_degree() < 3]
g.remove_vertex(a)
bv, be = betweenness(g)"""

g = load_graph("beer.graphml")
print("calculate pagerank")
pr = pagerank(g)
print("calculate betweenness")
bv, be = betweenness(g)
print("calculate closeness")
cl = closeness(g)
print("calculate eigenvector centrality")
ev = eigenvector(g)[1]
print("calculate katz")
kz = katz(g)
print("calculate hits")
ht = hits(g)
