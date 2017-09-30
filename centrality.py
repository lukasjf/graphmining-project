from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt

import math
import time
import sys
import pickle

class Dataset(object):
    def __init__(self, X, rep):
        self.X = X
        self.rep = rep

with open("centr/centr_"+sys.argv[1], "wb") as f:
	t0 = time.time()
	g = load_graph("datasets/" + str(sys.argv[1]) + ".graphml")
	t1 = time.time()
	print("graph loaded successfully in " + str(t1-t0) + " seconds")

	t0 = time.time()
	pr = pagerank(g)
	t1 = time.time()
	print("pagerank calculated in " + str(t1-t0) + " seconds")
	pr = [p for p in pr.a]

	t0 = time.time()
	bv, be = betweenness(g)
	t1 = time.time()
	print("betweenness calculated in " + str(t1-t0) + " seconds")
	bv = [b for b in bv.a]

	"""t0 = time.time()
	cl = closeness(g)
	t1 = time.time()
	print("closeness calculated in " + str(t1-t0) + " seconds")
	cl = [c for c in cl.a]"""

	t0 = time.time()
	ev = eigenvector(g)[1]
	t1 = time.time()
	print("eigenvector centrality calculated in " + str(t1-t0) + " seconds")
	ev = [e for e in ev.a]

	t0 = time.time()
	kz = katz(g)
	t1 = time.time()
	print("katz calculated in " + str(t1-t0) + " seconds")
	kz = [k for k in kz.a]

	t0 = time.time()
	ht = hits(g)
	t1 = time.time()
	print("hits calculated in " + str(t1-t0) + " seconds")
	auth = [h for h in ht[1].a]
	hub = [h for h in ht[2].a]

	t0 = time.time()
	id = [v.in_degree() for v in g.vertices()]
	t1 = time.time()
	print("in degree calculated in " + str(t1-t0) + " seconds")

	t0 = time.time()
	od = [v.out_degree() for v in g.vertices()]
	t1 = time.time()
	print("out degree calculated in " + str(t1-t0) + " seconds")

	rep = [rep for rep in g.vertex_properties["Reputation"]]
	rep = (rep - np.amin(rep))/(np.amax(rep) - np.amin(rep))
	X = [[1 for b in bv], pr, bv, ev, kz, auth, hub, id, od]
	data = Dataset(X,rep)
	pickle.dump(data,f,0)
