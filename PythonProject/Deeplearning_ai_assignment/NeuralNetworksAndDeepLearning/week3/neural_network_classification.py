#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import numbers
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.datasets
import sklearn.linear_model
from planar_utils import *

np.random.seed(1)

X, Y = load_planar_dataset()
m = X.shape[1]
print('-'*50)
print('The shape of X is: '+str(X.shape))
print('The shape of Y is: '+str(Y.shape))
print('I have m = {} training examples!'.format(m))
print('-'*50)
#Train the logistic regression classifier
clf = sklearn.linear_model.LogisticRegressionCV()
clf.fit(X.T, Y.T.ravel())
LR_predictions = clf.predict(X.T)
print('-'*50)
print('Accuracy of logistic regression: %d' % float((np.dot(Y, LR_predictions) + np.dot(1-Y, 1-LR_predictions))/float(Y.size)*100) + '%')
print('-'*50)
# Neural Network Model
# layer_sizes
def layer_sizes(X, Y):
    '''
    Arguments:
    X--input dataset of shape(input size, number of examples)
    Y--labels of shape(output size, number of examples)
    Returns:
    n_x--the size of the input layer
    n_y--the size of the hidden layer
    n_y--the size of the output layer
    '''
    n_x = X.shape[0]
    n_h = 4
    n_y = Y.shape[0]
    return n_x, n_h, n_y
# initialize_parameters
def initialize_parameters(n_x, n_h, n_y):
    '''
    Argument:
    n_x--size of the input layer
    n_h--size of the hidden layer
    n_y--size of the output layer
    Returns:
    params--python dictionary containing parameters:
            w1--weight matrix of shape(n_h, n_x)
            b1--bias vector of shape(n_h, 1)
            w2--weight matrix of shape(n_y, n_h)
            b2--bias vector of shape(n_y, 1)
    '''
    np.random.seed(2)
    w1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    w2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    assert(w1.shape == (n_h, n_x))
    assert(b1.shape == (n_h, 1))
    assert(w2.shape == (n_y, n_h))
    assert(b2.shape == (n_y, 1))
    parameters = {'w1':w1, 'b1':b1, 'w2':w2, 'b2':b2}
    return parameters
# The Loop
#forward propagation
def forward_propagation(X, parameters):
    '''
    Argument:
    X--input data of size(n_x, m)
    parameters--python dictionary containing parameters
    Returns:
    A2--the sigmoid output of the second activation
    cache--a dictionary containing Z1, A1, Z2, A2
    '''
    w1 = parameters['w1']
    b1 = parameters['b1']
    w2 = parameters['w2']
    b2 = parameters['b2']
    Z1 = np.dot(w1, X) + b1 
    A1 = np.tanh(Z1)
    Z2 = np.dot(w2, A1) + b2
    A2 = sigmoid(Z2)
    assert(A2.shape == (1, X.shape[1]))
    cache = {'Z1':Z1, 'A1':A1, 'Z2':Z2, 'A2':A2}
    return A2, cache
# compute cost
def compute_cost(A2, Y, parameters):
    '''
    Computes the cross-entropy cost give in equation
    Arguments:
    A2--The sigmoid output of the second activation, shape(1,number of examples)
    Y--labels, shape(1, number of examples)
    parameters--python dictionary
    Returns:
    cost--cross-entropy cost
    '''
    m = Y.shape[1] #number of example
    logprobs = np.dot(np.log(A2), Y.T) + np.dot(np.log(1-A2),(1-Y).T) 
    cost = -logprobs / m
    cost = cost.ravel()
    cost = cost[0]
    assert(isinstance(cost, numbers.Real))
    return cost
#backward propagation
def backward_propagation(parameters, cache, X, Y):
    '''
    Arguments:
    parameters--python dictionary
    cache--a dictionary containing Z1 A1 Z2 A2
    X--input data of shape(n_x, number of examples)
    Y--labels of shape(1, number of examples)
    Returns:
    grads--python dictionary containing gradients
    '''
    m = X.shape[1]
    w1 = parameters['w1']
    w2 = parameters['w2']
    A1 = cache['A1']
    A2 = cache['A2']
    dZ2 = A2 - Y
    dw2 = np.dot(dZ2, A1.T) / m
    db2 = np.sum(dZ2, axis=1, keepdims=True) / m
    dZ1 = np.dot(w2.T, dZ2) * (1 - np.power(A1, 2))
    dw1 = np.dot(dZ1, X.T) / m
    db1 = np.sum(dZ1, axis=1, keepdims=True) / m
    grads = {'dw1':dw1, 'db1':db1, 'dw2':dw2, 'db2':db2}
    return grads
#update parameters
def update_parameters(parameters, grads, learning_rate=1.2):
    '''
    Arguments:
    parameters--python dictionary
    grads--python dictionary
    learning_rate--hyparameters
    Returns:
    parameters--python dictionary containing updated parameters
    '''
    w1 = parameters['w1']
    b1 = parameters['b1']
    w2 = parameters['w2']
    b2 = parameters['b2']
    dw1 = grads['dw1']
    db1 = grads['db1']
    dw2 = grads['dw2']
    db2 = grads['db2']
    w1 -= learning_rate * dw1
    b1 -= learning_rate * db1
    w2 -= learning_rate * dw2
    b2 -= learning_rate * db2
    parameters = {'w1':w1, 'b1':b1, 'w2':w2, 'b2':b2}
    return parameters
#neural network model
def nn_model(X, Y, n_h, num_iterations=10000, print_cost=False):
    '''
    Arguments:
    X--dataset of shape(2, number of examples)
    Y--labels of shape(1, number of examples)
    n_h--size of the hidden layer
    num_iterations--number of iterations in gradient descent
    print_cost--if True, print cost every 1000 steps
    Return:
    parameters--parameters of model, used to predict
    '''
    np.random.seed(3)
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[2]
    parameters = initialize_parameters(n_x, n_h, n_y)
    w1 = parameters['w1']
    b1 = parameters['b1']
    w2 = parameters['w2']
    b2 = parameters['b2']
    #loop
    for i in range(0, num_iterations):
        A2, cache = forward_propagation(X, parameters)
        cost = compute_cost(A2, Y, parameters)
        grads = backward_propagation(parameters, cache, X, Y)
        parameters = update_parameters(parameters, grads)
        if print_cost and i % 1000 == 0:
            print('Cost after iteration {}: {}'.format(i, cost))
    return parameters
# predict
def predict(parameters, X):
    '''
    Arguments:
    parameters--python dictionary
    X--input data of shape(n_x, m)
    Returns:
    predictions--vector of predictions of model(red:0, bule:1)
    '''
    A2, cache = forward_propagation(X, parameters)
    predictions = A2 > 0.5
    return predictions

if __name__ == '__main__':
    fig = plt.figure()
    subplot_1 = fig.add_subplot(221)
    subplot_1.scatter(X[0, :], X[1, :], c=np.squeeze(Y), s=40, cmap=plt.cm.Spectral)
    subplot_1.set_title('Original data scatter')
    subplot_2 = fig.add_subplot(222)
    plot_decision_boundary(lambda x: clf.predict(x), X, Y, sub_plot=subplot_2)
    subplot_2.set_title('Logistic Regression')
    #build a neural network
    parameters = nn_model(X, Y, n_h=4, num_iterations=10000, print_cost=True)
    subplot_3 = fig.add_subplot(223)
    plot_decision_boundary(lambda x: predict(parameters,x.T), X, Y, sub_plot=subplot_3)
    subplot_3.set_title('Decision Boundary for hidden layer size '+str(4))
    predictions = predict(parameters, X)
    print('-'*50)
    print ('Accuracy of neural network with 4 hidden units: %d' % float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')

    parameters = nn_model(X, Y, n_h=5, num_iterations=10000, print_cost=True)
    subplot_4 = fig.add_subplot(224)
    plot_decision_boundary(lambda x: predict(parameters,x.T), X, Y, sub_plot=subplot_4)
    subplot_4.set_title('Decision Boundary for hidden layer size '+str(5))
    predictions = predict(parameters, X)
    print('-'*50)
    print ('Accuracy of neural network with 5 hidden units: %d' % float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')
    plt.show()
