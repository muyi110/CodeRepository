#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from reg_utils import *
import sklearn
import sklearn.datasets
import scipy.io

plt.rcParams['figure.figsize'] = (7.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

train_X, train_Y, test_X, test_Y = load_2D_dataset()
print('-'*50)
print('the shape of train_X: {}'.format(train_X.shape))
print('the shape of train_Y: {}'.format(train_Y.shape))
print('the shape of test_X: {}'.format(test_X.shape))
print('the shape of test_Y: {}'.format(test_Y.shape))
print('-'*50)

def model(X, Y, learning_rate=0.3, num_iterations=30000, print_cost=True, lambd=0, keep_prob=1):
    '''
    Implements a three-layer neural network.
    Arguments:
    X--input data, of shape(input size, number of examples).
    Y--labels, 1 for bule 0 for red of shape(output size, number of examples)
    learning_rate--learning rate of optimization
    num_iterations--number of iterations of optimization
    print_cost--if true, print cost every 10000 iterations
    lambd--regularization hyperparameter, scalar
    keep_prob--probability of keep a neuron active during drop-out, scalar
    Returns:
    parameters--parameters learned by the model
    '''
    grads = {}
    costs = []
    m = X.shape[1]
    layers_dims = [X.shape[0], 20, 3, 1]
    #Initialize parameters dictionary
    parameters = initialize_parameters(layers_dims)
    #loop (gradient descent)
    for i in range(0, num_iterations):
        #Forward propagation
        if keep_prob == 1:
            A3, cache = forward_propagation(X, parameters)
        elif keep_prob < 1:
            A3, cache = forward_propagation(X, parameters, keep_prob)
        # cost function
        if lambd == 0:
            cost = compute_cost(A3, Y)
        else:
            cost = compute_cost_with_regularization(A3, Y, parameters, lambd)
        #Backward propagation
        assert(lambd == 0 or keep_prob == 1)# make sure explore one at a time
        if lambd == 0 and keep_prob == 1:
            grads = backward_propagation(X, Y, cache)
        elif lambd != 0:
            grads = backward_propagation_with_regularization(X, Y, cache, lambd)
        elif keep_prob < 1:
            grads = backward_propagation_with_dropout(X, Y, cache, keep_prob)
        #Update parameters
        parameters = update_parameters(parameters, grads, learning_rate)
        #print cost
        if print_cost and i % 10000 == 0:
            print('Cost after iteration {}: {}'.format(i, cost))
        if print_cost and i % 1000 == 0:
            costs.append(cost)
        #plot the cost
        plt.plot(costs)
        plt.ylabel('cost')
        plt.xlabel('iterations (per 1000 )')
        plt.title('Learning rate = '+str(learning_rate))
        plt.show()
        return parameters
#L2 regularization
def compute_cost_with_regularization(A3, Y, parameters, lambd):
    '''
    Implement the cost function with L2 regularization.
    Arguments:
    A3--post-activation, output of forward propagation
    Y--labels, of shape(output size, number of examples)
    parameters--python dictionary
    Returns:
    cost--value of regularization loss function
    '''
    m = Y.shape[1]
    W1 = parameters['W1']
    W2 = parameters['W2']
    W3 = parameters['W3']
    cross_entropy_cost = compute_cost(A3, Y)
    L2_regularization_cost = (np.sum(np.square(W1)) + np.sum(np.square(W2)) + np.sum(np.square(W3))) * (1./m) * (lambd/2.)
    cost = cross_entropy_cost + L2_regularization_cost
    return cost
def backward_propagation_with_regularization(X, Y, cache, lambd):
    '''
    Implements the backward propagation with L2 regularization
    Arguments:
    X--input dataset, of shape(input size, number of examples)
    Y--labels, of shape(output size, number of examples)
    cache--cache output from forward propagation
    lambd--regularization hyperparameters, scalar
    Returns:
    gradients--A dictionary
    '''
    m = X.shape[1]
    (Z1, A1, W1, b1, Z1, A2, W2, b2, A3, A3, w3, b3) = cache
    dZ3 = 1./m * (A3 - Y)
    dW3 = np.dot(dZ3, A2.T) + (lambd/m) * W3
    db3 = np.sum(dZ3, axis=1, keepdims=True)
    dA2 = np.dot(W3.T, dZ3)
    dZ2 = np.multiply(dA2, np.int64(A2>0))
    dW2 = np.dot(dZ2, A1.T) + (lambd/m) * W2
    db2 = np.sum(dZ2, axis=1, keepdims=True)
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = np.multiply(dA1, int64(A1>0))
    dW1 = np.dot(dZ1, X.T) + (lambd/m) * W1
    db1 = np.sum(dZ1, axis=1, keepdims=True)
    gradients = {'dZ3':dZ3, 'dW3':dW3, 'db3':db3, 'dA2':dA2,
                 'dZ2':dZ2, 'dW2':dW2, 'db2':db2, 'dA1':dA1,
                 'dZ1':dZ1, 'dW1':dW1, 'db1':db1}
    return gradients
# Dropout regularization
def forward_propagation_with_dropout(X, parameters, keep_prob=0.5):
    '''
    Arguments:
    X--input dataset, of shape(input size, number of examples)
    parameters--python dictionary containing Wi,bi(i=1,2,3)
    keep_prob--probability of keeping a neural active during dropout, scalar.
    Returns:
    A3--last activation value
    cache--tuple, information stored for backward propagation
    '''
    np.random.seed(1)
    #retrieve parameters
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']
    
    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
