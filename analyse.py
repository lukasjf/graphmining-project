from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense

import tensorflow as tf

g = load_graph("datasets/beer_answers.graphml")
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

betweenness = np.asarray([be for be in bv.a])
betweenness = np.asarray([v.out_degree() for v in g.vertices()])
reputation = np.asarray([rep for rep in g.vertex_properties["Reputation"]])
#reputation = reputation / max(reputation)

X = np.asarray([[be for be in bv.a],
	[v.out_degree() for v in g.vertices()],
	[v.in_degree() for v in g.vertices()],
	[p for p in pr.a],
	#[c for c in cl.a],
	[e for e in ev.a],
	[k for k in kz.a],
	[h for h in ht[1].a],
	[h for h in ht[2].a]
]).transpose()

plt.scatter(betweenness,reputation)
#plt.show()
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
w = tf.cast(tf.Variable(tf.zeros([8,1])),tf.float64)
b = tf.cast(tf.Variable(tf.zeros([1])), tf.float64)
mod = tf.matmul(X,w) + b
loss = tf.reduce_mean(tf.square(reputation-mod))
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)
for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(w), sess.run(b))
prediction = sess.run(mod, betweenness.all())
print(prediction)
