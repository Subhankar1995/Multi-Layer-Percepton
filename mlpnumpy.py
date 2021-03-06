# -*- coding: utf-8 -*-
"""MLPnumpy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GU6Aw9iAy4tuDz5zIxH0AgxKhDoBw_iw
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST data/", one_hot=True)
X_train = np.vstack([img.reshape((1,784,1)) for img in mnist.train.images])
y_train = mnist.train.labels
y_train = np.reshape(y_train,(55000,10,1))
X_test = np.vstack([img.reshape(1,784,1) for img in mnist.test.images])
y_test = mnist.test.labels
y_test = np.reshape(y_test,(10000,10,1))
del mnist

class MLP():
    
    def __init__(self,size):
        self.size = size
        self.length = len(size)
    
    def default_weight_initializer(self):
        biases = [np.random.randn(y, 1) for y in self.size[1:]]
        weights = [np.random.randn(y, x)
                        for x, y in zip(self.size[:-1], self.size[1:])]
        return biases,weights
    
    def relu(self,z):
        return np.maximum(0,z)
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    
    def backprop(self,x,y,biases,weights):
        #feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(biases,weights):
            z = np.dot(w, activation)+b
            #print(z.shape)#,w.shape,b.shape)
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        #weights = weights]
        #backpropagation
        deltalayers,deltaweights,deltabiases=[],[],[]
        deltay = (activations[-1]-y)*activations[-1]*(1-activations[-1])
        #deltay = np.reshape(deltay,(deltay.shape[0],1))
        #print(deltay.shape)
        for l in range(1,self.length):
            deltaweight = np.dot(deltay,activations[-l-1].transpose())
            deltaweights.append(deltaweight)
            deltabiase = deltay
            deltabiases.append(deltabiase)
            deltalayer = np.dot(weights[-l].transpose(),deltay)
            deltalayers.append(deltalayer)
            deltay = deltalayer
        #w=self.weights"""
        return activations[-1],deltaweights,deltabiases
    
    def error(self,y,yhat):
        return np.sum(np.square(y-yhat))
    
    def traning(self,X_train,y_train,epoch,batch_size,lr,biases,weights):
        l = len(X_train)
        loss = []
        for i in range(epoch):
            minibatches = [zip(X_train[k:k+batch_size,:],y_train[k:k+batch_size,:]) for k in range(0,l,batch_size)]
            err = []
            u = 1
            for mini in minibatches:
                #print("minibatch no : {}".format(u))
                for x,y in mini:
                    temperror = []
                    yhat,deltaweights,deltabiases = model.backprop(x,y,biases,weights)
                    temperror.append(self.error(y,yhat))
                    deltaweights,deltabiases = np.array(deltaweights),np.array(deltabiases)
                    deltaweights += deltaweights
                    deltabiases += deltabiases
                deltaweights = np.array([i for i in list(reversed(deltaweights))])
                deltabiases = np.array([i for i in list(reversed(deltabiases))])
                err.append(np.sum(temperror)/batch_size)
                weights-=lr*(deltaweights/batch_size)
                biases-=lr*(deltabiases/batch_size)
                u+=1
            n = (np.sum(err)/550)
            print("epoch {} complete current loss : {}".format(i,n))
            loss.append(n)
        self.modelweight = weights
        self.modelbiases = biases
        return loss
    
    def testing(self,X_test,y_test):
        self.testlen = len(X_test)
        yout = []
        for x in X_test:
            
            activation = x
            activations = [x] # list to store all the activations, layer by layer
            zs = [] # list to store all the z vectors, layer by layer
            for b, w in zip(self.modelbiases,self.modelweight):
                z = np.dot(w, activation)+b
                zs.append(z)
                activation = self.sigmoid(z)
                activations.append(activation)
            yout.append(activations[-1])
        yhat = np.reshape(yout,(y_test.shape))
        accu = self.accurecy(yhat,y_test)
        print("Test accurecy : {}".format(accu))
        
    def accurecy(self,yhat,ytest):
        summ=0 
        for i in range(yhat.shape[0]):
            if (np.argmax(yhat[i])) == (np.argmax(ytest[i])):
                summ+=1
        return (summ/self.testlen)

model = MLP([784,128,10])
biases,weights = model.default_weight_initializer()

los = model.traning(X_train,y_train,50,100,0.01,biases,weights)
plt.plot(los)

model.testing(X_test,y_test)