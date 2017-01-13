from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense

import tensorflow as tf
import time
import sys

t0 = time.time()
g = load_graph(str(sys.argv[1]))
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

t0 = time.time()
cl = closeness(g)
t1 = time.time()
print("closeness calculated in " + str(t1-t0) + " seconds")
cl = [c for c in cl.a]

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

rep = np.asarray([rep for rep in g.vertex_properties["Reputation"]])


X = np.asarray([
    [1 for b in bv],
    pr, bv, ev, kz, auth, hub, id, od
])

for feature in X:
    print(len(feature))
    print(sum(feature==0))
    plt.scatter(feature, rep)
    plt.show()

for feature in X[1:,]:
    print(np.corrcoef(feature,rep))


X = X[filt]
reputation = reputation[filt]
"""
model = Sequential()
model.add(Dense(13, input_dim=1, init='normal', activation='relu'))
model.add(Dense(1, init='normal'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(betweenness[:350], reputation[:350], nb_epoch=1000)
print("result")
print(model.evaluate(betweenness[350:], reputation[350:]))
"""

w = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.transpose(),X)),X.transpose()),reputation)
