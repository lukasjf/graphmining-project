from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense

import tensorflow as tf
import math
import time
import sys

np.random.seed(1234)

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

feature_names = ["bias", "pagerank", "betweenness", "eigenvector", "katz", "hits-authority", "hits-hub", "in_degree", "out_degree"] 

indices = np.random.permutation(X.shape[1])
train = indices[:len(indices)//10*7]
test = indices[len(indices)//10*7:]

for index, feature in enumerate(X[1:,]):
    if ('verbose' in sys.argv):
        print(len(feature))
        print(sum(feature==0))
    plt.scatter(feature, rep)
    plt.xlim(0)
    plt.xlabel(feature_names[index+1])
    plt.ylim(0)
    plt.ylabel('reputation')
    plt.savefig(sys.argv[1].replace('datasets/','').replace('.graphml','') + feature_names[index+1] + '.pdf')

    print(np.corrcoef(feature,rep)[0,1])

    data = np.asarray([X[0,],feature]).transpose()
    training = data[train,]
    testing = data[test,]
    weight = np.matmul(np.matmul(np.linalg.inv(np.matmul(training.transpose(),training)),training.transpose()),rep[train])
    prediction = np.matmul(testing,weight)
    mse = np.dot(prediction-rep[test], prediction-rep[test]) / len(prediction)
    mrd = sum((prediction-rep[test])/rep[test]) / len(prediction)
    print("SE for " + feature_names[index+1] + " is: " + str(mse))
    #print("RD for " + feature_names[index+1] + " is: " + str(mrd))
    plt.plot(feature, feature*weight[1] + weight[0],'-')
    plt.savefig(sys.argv[1].replace('datasets/','').replace('.graphml','') + feature_names[index+1] + '_fitted.pdf')
    plt.clf()
    

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
X = X.transpose()
w = np.matmul(np.matmul(np.linalg.inv(np.matmul(X[train,].transpose(),X[train,])),X[train,].transpose()),rep[train])
prediction = np.matmul(X[test,],w)
mse = np.dot(prediction-rep[test], prediction-rep[test]) / len(prediction)
print("MSE for mv linear regression " + str(mse))
rd = sum(np.absolute(prediction-rep[test])) 
rd = rd/ np.mean(rep[test]) / len(prediction)
print("RD for mv linear regression " + str(rd))
print("mean " + str(np.mean(rep[test])))
