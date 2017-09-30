from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

import tensorflow as tf
import math
import time
import sys
import pickle

np.random.seed(784)

class Dataset(object):
    def __init__(self, X, rep):
        self.X = X
        self.rep = rep

data = pickle.load(open("centr/centr_"+sys.argv[1], "rb"))
X = np.asarray(data.X)
rep = np.asarray(data.rep)

mask = ~np.any(np.isnan(X),axis=0)
X = X.transpose()[mask].transpose()
rep = rep[mask]


feature_names = ["bias", "pagerank", "betweenness", "eigenvector", "katz", "hits-authority", "hits-hub", "in_degree", "out_degree"] 

indices = np.random.permutation(X.shape[1])
train = indices[:len(indices)//4*3:]
test = indices[len(indices)//4*3:]

corrs = []
r2s = []
tts = []

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

    #print(np.corrcoef(feature,rep)[0,1])
    corrs += [round(np.corrcoef(feature,rep)[0,1],4)]
    data = np.asarray([X[0,],feature]).transpose()
    training = data[train,]
    testing = data[test,]
    t0 = time.time()
    weight = np.matmul(np.matmul(np.linalg.pinv(np.matmul(training.transpose(),training)),training.transpose()),rep[train])
    t1 = time.time()
    prediction = np.matmul(testing,weight)
    rss = sum(np.square(prediction-rep[test]))
    tss = sum(np.square(rep[test] - np.mean(rep[test])))
    r2 = (tss-rss)/tss
    r2s += [round(r2,4)]
    tts += [round(t1-t0,3)]
    #print("R2 metric for " + feature_names[index+1] + " is: " + str(r2) + "training time: " + str(t1-t0) + " seconds")
    plt.plot(feature, feature*weight[1] + weight[0],'-')
    plt.savefig(sys.argv[1].replace('datasets/','').replace('.graphml','') + feature_names[index+1] + '_fitted.pdf')
    plt.clf()
    
print("Correlations: " + ' & '.join(map(str,corrs)))
print("R2 errors : " + ' & '.join(map(str,r2s)))
print("Training Times " + ' & '.join(map(str,tts)))



X = X.transpose()
t0 = time.time()
w = np.matmul(np.matmul(np.linalg.pinv(np.matmul(X[train,].transpose(),X[train,])),X[train,].transpose()),rep[train])
t1 = time.time()
prediction = np.matmul(X[test,],w)
rss = sum(np.square(prediction-rep[test]))
tss = sum(np.square(rep[test] - np.mean(rep[test])))
r2 = (tss-rss)/tss
print("R2 metric for mv linear regression " + str(r2)+ "training time: " + str(t1-t0) + " seconds")


model = Sequential()
model.add(Dense(50, input_dim=9, init='normal', activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(50, init='normal', activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(1, init='normal'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='adam')
t0 = time.time()
cb = ModelCheckpoint("0model.hdf5", monitor="val_loss", verbose = 0, save_best_only=True)
model.fit(X[train,], rep[train,],validation_split=0.33, nb_epoch=1500, verbose=0, callbacks=[cb])
model = load_model("0model.hdf5")
t1 = time.time()
prediction = model.predict(X[test,]).flatten()
rss_nn = sum(np.square(prediction-rep[test]))
tss_nn = sum(np.square(rep[test] - np.mean(rep[test])))
r2_nn = (tss_nn-rss_nn)/tss_nn
print("R2 for neural network is: " + str(r2_nn) + " training time: " + str(t1-t0) + " seconds")

mv = []
nn = []
def compare(dataset,mv,nn):
    data = pickle.load(open("centr/centr_" + dataset,"rb"))
    X = np.asarray(data.X)
    rep = np.asarray(data.rep)

    mask = ~np.any(np.isnan(X),axis=0)
    X = X.transpose()[mask]
    rep = rep[mask]

    prediction = np.matmul(X,w)
    rss = sum(np.square(prediction-rep))
    tss = sum(np.square(rep - np.mean(rep)))
    r2 = (tss-rss)/tss
    print("R2 metric for mv linear regression for " + dataset + " is: " + str(r2))
    mv += [round(r2,4)] if r2 > 0 else ["X"]

    prediction = model.predict(X).flatten()
    rss_nn = sum(np.square(prediction-rep))
    tss_nn = sum(np.square(rep - np.mean(rep)))
    r2_nn = (tss_nn-rss_nn)/tss_nn
    print("R2 for NN for " + dataset + " is: " + str(r2_nn))
    nn += [round(r2_nn,4)] if r2_nn > 0 else ["X"]

compare("beer",mv,nn)
compare("codegolf",mv,nn)
compare("cs",mv,nn)
compare("academia",mv,nn)
compare("scifi",mv,nn)
compare("android",mv,nn)
compare("tex",mv,nn)
compare("serverfault",mv,nn)
print(' & '.join(map(str,mv)))
print(' & '.join(map(str,nn)))
