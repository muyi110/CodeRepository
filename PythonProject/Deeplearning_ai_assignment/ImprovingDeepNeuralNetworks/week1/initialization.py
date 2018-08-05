#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.datasets
from init_utils import *

plt.rcParams['figure.figsize'] = (7.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

train_X, train_Y, test_X, test_Y = load_dataset()
print('-'*50)
print('the shape of train_X: {}'.format(train_X.shape))
print('the shape of train_Y: {}'.format(train_Y.shape))
print('the shape of test_X: {}'.format(test_X.shape))
print('the shape of test_Y: {}'.format(test_Y.shape))
print('-'*50)

def model(X, Y, learning_rate=0.01, num_iterations=15000, print_cost=True, initialization='he'):
    '''
    Implements a three-layer neural network.
    Arguments:
    X--input data, of shape(2, number of examples)
    Y--labels, of shape(1, number of examples)
    learning_rate--learning rate for gradient descent
    num_iterations--number of iterations to run gradient descent
    print_cost--if true, print cost every 1000 iterations
    initialization--flag to choose which initialization to use
    Returns:
    parameters--parameters learnt by the model
    '''
    grads = {}
    costs = []
    m = X.shape[1]
    layers_dims = [X.shape[0], 10, 5, 1]
    #Initialize parameters dictionary
    if initialization == 'zeros':
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == 'random':
        parameters = initialize_parameters_random(layers_dims)
    elif initialization == 'he':
        parameters = initialize_parameters_he(layers_dims)
    # loop(gradient descent)
    for i in range(num_iterations):
        # forward propagation
        A3, cache = forward_propagation(X, parameters)
        #loss
        cost = compute_loss(A3, Y)
        #backward propagation
        grads = backward_propagation(X, Y, cache)
        #update parameters
        parameters = update_parameters(parameters, grads, learning_rate)
        #print cost
        if print_cost and i % 1000 == 0:
            print('Cost after iteration {}: {}'.format(i, cost))
            costs.append(cost)
    # plot the loss
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('iterations (per 1000)')
    plt.title('Learning rate = '+str(learning_rate))
    plt.show()
    return parameters
def initialize_parameters_zeros(layers_dims):
    '''
    Arguments:
    layers_dims--python array(list) containing the size of each layer.
    Returns:
    parameters--python dictionary containing parameters.
    '''
    parameters = {}
    L = len(layers_dims)
    for l in range(1, L):
        parameters['W'+str(l)] = np.zeros((layers_dims[l],layers_dims[l-1]))
        parameters['b'+str(l)] = np.zeros((layers_dims[l], 1))
    return parameters
def initialize_parameters_random(layers_dims):
    '''
    Arguments:
    layers_dims--python array(list) containing the size of each layer.
    Returns:
    parameters--python dictionary containing parameters.
    '''
    np.random.seed(3)
    parameters = {}
    L = len(layers_dims)
    for l in range(1, L):
        parameters['W'+str(l)] = np.random.randn(layers_dims[l], layers_dims[l-1]) * 10
        parameters['b'+str(l)] = np.zeros((layers_dims[l], 1))
    return parameters
def initialize_parameters_he(layers_dims):
    '''
    Arguments:
    layers_dims--python array(list) containing the size of each layer.
    Returns:
    parameters--python dictionary containing parameters.
    '''
    np.random.seed(3)
    parameters = {}
    L = len(layers_dims)
    for l in range(1, L):
        parameters['W'+str(l)] = np.random.randn(layers_dims[l], layers_dims[l-1]) * np.sqrt(2./ layers_dims[l-1])
        parameters['b'+str(l)] = np.zeros((layers_dims[l], 1))
    return parameters

if __name__ == '__main__':
    parameters = model(train_X, train_Y, initialization='zeros')
    print('-'*50)
    print('On the train set(zeros initialization):')
    predictions_train = predict(train_X, train_Y, parameters)
    print('On the test set(zeros initialization):')
    predictions_test = predict(test_X, test_Y, parameters)
    plt.title('Model with Zeros initialization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 1.5])
    axes.set_ylim([-1.5, 1.5])
    plot_decision_boundary(lambda x: predict_dec(parameters, x.T), train_X, train_Y)

    parameters = model(train_X, train_Y, initialization='random')
    print('-'*50)
    print('On the train set(random initialization):')
    predictions_train = predict(train_X, train_Y, parameters)
    print('On the test set(random initialization):')
    predictions_test = predict(test_X, test_Y, parameters)
    plt.title('Model with random initialization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 1.5])
    axes.set_ylim([-1.5, 1.5])
    plot_decision_boundary(lambda x: predict_dec(parameters, x.T), train_X, train_Y)

    parameters = model(train_X, train_Y, initialization='he')
    print('-'*50)
    print('On the train set(he initialization):')
    predictions_train = predict(train_X, train_Y, parameters)
    print('On the test set(he initialization):')
    predictions_test = predict(test_X, test_Y, parameters)
    plt.title('Model with he initialization')
    axes = plt.gca()
    axes.set_xlim([-1.5, 1.5])
    axes.set_ylim([-1.5, 1.5])
    plot_decision_boundary(lambda x: predict_dec(parameters, x.T), train_X, train_Y)
