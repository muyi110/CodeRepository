#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import math
import sklearn
import sklearn.datasets
from opt_utils import *

plt.rcParams['figure.figsize'] = (7.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

def update_parameters_with_gd(parameters, grads, learning_rate):
    '''
    Arguments:
    parameters--python dictionary containing parameters.
    grads--python dictionary containing gradients
    learning_rate--the learning rate, scalar
    Returns:
    parameters--python dictionary containing updated parameters.
    '''
    L = len(parameters) // 2
    for l in range(L):
        parameters['W'+str(l+1)] -= learning_rate * grads['dW'+str(l+1)]
        parameters['b'+str(l+1)] -= learning_rate * grads['db'+str(l+1)]
    return parameters
def random_mini_batches(X, Y, mini_batch_size=64, seed=0):
    '''
    Creates a list of random minibatches from (X, Y)
    Arguments:
    X--input data, of shape(input size, number of examples)
    Y--labels, of shape(1, number of examples)
    mini_batch_size--size of the mini-batches, integer
    Returns:
    mini-batches--list of synchronous(mini_batch_X, mini_batch_Y)
    '''
    np.random.seed(seed)
    m = X.shape[1]
    mini_batches = []
    # step1: Shuffle X, Y
    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((1, m))
    #step2: Partition
    num_complete_minibatches = math.floor(m/mini_batch_size)
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k*mini_batch_size:(k+1)*mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k*mini_batch_size:(k+1)*mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, num_complete_minibatches*mini_batch_size:] 
        mini_batch_Y = shuffled_Y[:, num_complete_minibatches*mini_batch_size:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    return mini_batches
# initialize velocity for momentum
def initialize_velocity(parameters):
    '''
    Initialize the velocity as a python dictionary, the same as gradients.
    Arguments:
    parameters--python dictionary
    Returns:
    v--python dictionary containing the current velocity
    '''
    L = len(parameters) // 2
    v = {}
    for l in range(L):
        v['dW'+str(l+1)] = np.zeros(parameters['W'+str(l+1)].shape)
        v['db'+str(l+1)] = np.zeros(parameters['b'+str(l+1)].shape)
    return v
def update_parameters_with_momentum(parameters, grads, v, beta, learning_rate):
    '''
    Arguments:
    parameters--python dictionary
    grads--python dictionary containing gradients
    v--python dictionary containing the current velocity
    beta--the momentum hyperparameter, scalar
    learning_rate--the learning rate, scalar
    Returns:
    parameters--python dictionary containing updated parameters
    v--python dictionary containing updated velocity
    '''
    L = len(parameters) // 2
    for l in range(L):
        v['dW'+str(l+1)] = beta * v["dW" + str(l+1)] + (1-beta)*grads['dW'+str(l+1)]
        v['db'+str(l+1)] = beta * v["db" + str(l+1)] + (1-beta)*grads['db'+str(l+1)]
        parameters['W'+str(l+1)] -= learning_rate * v['dW'+str(l+1)] 
        parameters['b'+str(l+1)] -= learning_rate * v['db'+str(l+1)]
    return parameters, v
# Adam optimization
def initialize_adam(parameters):
    '''
    initialize v and s as python dictionary, the same as gradients.
    Arguments:
    parameters--python dictionary
    Returns:
    v--dictionary containing the exponentially weighted average of the gradients.
    s--dictionary containing the exponentially weighted average of the squared gradients.
    '''
    L = len(parameters) // 2
    v = {}
    s = {}
    for l in range(L):
        v['dW'+str(l+1)] = np.zeros(parameters['W'+str(l+1)].shape)
        v['db'+str(l+1)] = np.zeros(parameters['b'+str(l+1)].shape)
        s['dW'+str(l+1)] = np.zeros(parameters['W'+str(l+1)].shape)
        s['db'+str(l+1)] = np.zeros(parameters['b'+str(l+1)].shape)
    return v, s
def update_parameters_with_adam(parameters, grads, v, s, t, learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8):
    '''
    Arguments:
    parameters--python dictionary
    grads--python dictionary
    v--adam variable, dictionary, moving average of the first gradient
    s--adam variable, dictionary, moving average of the squared gradient
    t--count steps
    learning_rate--the learning rate
    beta1--exponential decay hyperparameter for the first moment estimates
    beta2--exponential decay hyperparameter for the second moment estimates
    epsilon--hyperparameter preventing division by zero
    Returns:
    parameters--dictionary, updated parameters
    v--adam variable, dictionary, moving average of the first gradient
    s--adam variable, dictionary, moving average of the squared gradient
    '''
    L = len(parameters) // 2
    v_corrected = {}
    s_corrected = {}
    for l in range(L):
        v['dW'+str(l+1)] = beta1 * v['dW'+str(l+1)] + (1-beta1) * grads['dW'+str(l+1)]
        v['db'+str(l+1)] = beta1 * v['db'+str(l+1)] + (1-beta1) * grads['db'+str(l+1)]
        v_corrected['dW'+str(l+1)] = v['dW'+str(l+1)] / (1-np.power(beta1,t))
        v_corrected['db'+str(l+1)] = v['db'+str(l+1)] / (1-np.power(beta1,t))

        s['dW'+str(l+1)] = beta2 * s['dW'+str(l+1)] + (1-beta2) * np.square(grads['dW'+str(l+1)])
        s['db'+str(l+1)] = beta2 * s['db'+str(l+1)] + (1-beta2) * np.square(grads['db'+str(l+1)])
        s_corrected['dW'+str(l+1)] = s['dW'+str(l+1)] / (1-np.power(beta2,t))
        s_corrected['db'+str(l+1)] = s['db'+str(l+1)] / (1-np.power(beta2,t))

        parameters['W'+str(l+1)] -= learning_rate * v_corrected['dW'+str(l+1)] / (np.sqrt(s_corrected['dW'+str(l+1)])+epsilon)
        parameters['b'+str(l+1)] -= learning_rate * v_corrected['db'+str(l+1)] / (np.sqrt(s_corrected['db'+str(l+1)])+epsilon)
    return parameters, v, s

def model(X, Y, layers_dims, optimizer, learning_rate=0.0007, mini_batch_size=64, beta=0.9, beta1=0.9, beta2=0.999, epsilon=1e-8, num_epochs=10000, print_cost=True):
    '''
    Arguments:
    X--input data
    Y--labels
    layers_dims--list, containing the size of each layer
    optimizer--different optimizer methons
    learning_rate--the learning rate
    mini_batch_size--the size of a mini-batch
    beta--momentum hyperparameter
    beta1--exponential decay hyperparameter for the first moment estimates
    beta2--exponential decay hyperparameter for the second moment estimates
    epsilon--hyperparameter preventing division by zero
    num_epochs--number of epochs
    print_cost--if true, print cost every 1000 epochs
    Returns:
    parameters--updated parameters
    '''
    L = len(layers_dims)
    costs = []
    t = 0
    seed = 10
    #initialize parameters
    parameters = initialize_parameters(layers_dims)
    #initialize the optimizer
    if optimizer == 'gd':
        pass
    elif optimizer == 'momentum':
        v = initialize_velocity(parameters)
    elif optimizer == 'adam':
        v, s = initialize_adam(parameters)
    # loop
    for i in range(num_epochs):
        seed = seed + 1
        minibatches = random_mini_batches(X, Y, mini_batch_size, seed)
        for minibatch in minibatches:
            (minibatch_X, minibatch_Y) = minibatch
            #forward propagation
            a3, caches = forward_propagation(minibatch_X, parameters)
            cost = compute_cost(a3, minibatch_Y)
            #backward propagation
            grads = backward_propagation(minibatch_X, minibatch_Y, caches)
            #update parameters
            if optimizer == 'gd':
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == 'momentum':
                parameters, v = update_parameters_with_momentum(parameters, grads, v, beta, learning_rate)
            elif optimizer == 'adam':
                t = t + 1
                parameters, v, s = update_parameters_with_adam(parameters, grads, v, s, t, learning_rate, beta1, beta2, epsilon)
        if print_cost and i % 1000 == 0:
            print('Cost after epoch %i: %f' % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('epochs (per 100)')
    plt.title('Learning rate = '+str(learning_rate))
    plt.show()
    return parameters

if __name__ == '__main__':
    train_X, train_Y = load_dataset()
    print('-'*50)
    layers_dims = [train_X.shape[0], 5, 2, 1]
    parameters = model(train_X, train_Y, layers_dims, optimizer='gd')
    predictions = predict(train_X, train_Y, parameters)
    plt.title('Model with gradient descent optimization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 2.5])
    axes.set_ylim([-1, 1.5])
    plot_decision_boundary(lambda x:predict_dec(parameters, x.T), train_X, train_Y)
    
    print('-'*50)
    layers_dims = [train_X.shape[0], 5, 2, 1]
    parameters = model(train_X, train_Y, layers_dims, beta=0.9, optimizer='momentum')
    predictions = predict(train_X, train_Y, parameters)
    plt.title('Model with momentum optimization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 2.5])
    axes.set_ylim([-1, 1.5])
    plot_decision_boundary(lambda x:predict_dec(parameters, x.T), train_X, train_Y)

    print('-'*50)
    layers_dims = [train_X.shape[0], 5, 2, 1]
    parameters = model(train_X, train_Y, layers_dims, optimizer='adam')
    predictions = predict(train_X, train_Y, parameters)
    plt.title('Model with adam optimization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 2.5])
    axes.set_ylim([-1, 1.5])
    plot_decision_boundary(lambda x:predict_dec(parameters, x.T), train_X, train_Y)
