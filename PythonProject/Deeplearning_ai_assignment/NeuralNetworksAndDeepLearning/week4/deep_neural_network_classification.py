#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import time
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
from deep_neural_network_lib import *

plt.rcParams['figure.figsize'] = (5.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
np.random.seed(1)
#load dataset
train_x_orig, train_y, test_x_orig, test_y, classes = load_data()
#Example of a picture
index = 7
plt.imshow(train_x_orig[index])
plt.show()
#show the dataset information
m_train = train_x_orig.shape[0]
m_test = test_x_orig.shape[0]
num_px = train_x_orig.shape[1]
print('number of training examples: {}.'.format(m_train))
print('number of testing examples: {}.'.format(m_test))
print('height/width of each image: {}.'.format(num_px))
print('each image is of size: ({},{},{}).'.format(num_px, num_px, 3))
print('train_x_shape: {}.'.format(train_x_orig.shape))
print('train_y_shape: {}.'.format(train_y.shape))
print('test_x_shape: {}.'.format(test_x_orig.shape))
print('test_y_shape: {}.'.format(test_y.shape))
#Reshape the training and test examples. After this, the dataset is a numpy-array where each column represents a flattened image.
train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0], -1).T
test_x_flatten = test_x_orig.reshape(test_x_orig.shape[0], -1).T
print('-'*50)
print('-'*50)
print('train_x_flatten shape: {}.'.format(train_x_flatten.shape))
print('train_y shape: {}.'.format(train_y.shape))
print('test_x_flatten shape: {}.'.format(test_x_flatten.shape))
print('test_y shape: {}.'.format(test_y.shape))
#Standardize the dataset
train_x = train_x_flatten / 255.
test_x = test_x_flatten / 255.
print('-'*50)
print('-'*50)
# Two layer neural network
n_x = num_px * num_px * 3
n_h = 7
n_y = 1
layers_dims = (n_x, n_h, n_y)
def two_layer_model(X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False):
    '''
    Arguments:
    X--input data, of shape(n_x, number of examples)
    Y--labels(1, number of examples)
    layers_dims--dimensions of the layers(n_x, n_h, n_y)
    num_iterations--number of iterations
    learning_rate--learning rate of gradient descent
    print_cost--if true, print cost every 100 steps
    Returns:
    parameters--a dictionary containing W1 W2 b1 and b2
    '''
    np.random.seed(1)
    grads = {}
    costs = []
    m = X.shape[1]
    (n_x, n_h, n_y) = layers_dims
    parameters = initialize_parameters(n_x, n_h, n_y)
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    for i in range(num_iterations):
        # forward propagation
        A1, cache1 = linear_activation_forward(X, W1, b1, 'relu')
        A2, cache2 = linear_activation_forward(A1, W2, b2, 'sigmoid')
        # compute cost
        cost = compute_cost(A2, Y)
        #initializing backward propagation
        dA2 = -(np.divide(Y, A2) - np.divide(1-Y, 1-A2))
        # backward propagation
        dA1, dW2, db2 = linear_activation_backward(dA2, cache2, 'sigmoid')
        dA0, dW1, db1 = linear_activation_backward(dA1, cache1, 'relu')
        grads['dW1'] = dW1
        grads['db1'] = db1
        grads['dW2'] = dW2
        grads['db2'] = db2
        # update parameters
        parameters = update_parameters(parameters, grads, learning_rate)
        W1 = parameters['W1']
        b1 = parameters['b1']
        W2 = parameters['W2']
        b2 = parameters['b2']
        #print cost
        if print_cost and i % 100 ==0:
            print('Cost after iteration {}: {}'.format(i, cost))
        if i % 100 == 0:
            costs.append(cost)
    #plot the cost
    plt.subplot(121)
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('iterations(per tens)')
    plt.title('learning rate = '+str(learning_rate))
    return parameters
# L-layer model
layers_dims_L = [12288, 20, 7, 5, 1]
def L_layer_model(X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False):
    '''
    Arguments:
    X--input data, of shape(n_x, number of examples)
    Y--labels(1, number of examples)
    layers_dims--dimensions of the layers
    num_iterations--number of iterations
    learning_rate--learning rate of gradient descent
    print_cost--if true, print cost every 100 steps
    Returns:
    parameters--a dictionary containing W1 W2 b1 and b2
    '''
    np.random.seed(1)
    costs = []
    #parameters initialization
    parameters = initialize_parameters_deep(layers_dims_L)
    #loop (gradient descent)
    for i in range(0, num_iterations):
        # forward propagation
        AL, caches = L_model_forward(X, parameters)
        # compute cost
        cost = compute_cost(AL, Y)
        # backward propagation
        grads = L_model_backward(AL, Y, caches)
        # update parameters
        parameters = update_parameters(parameters, grads, learning_rate)
        #print cost
        if print_cost and i%100 == 0:
            print('Cost after iteration %i: %f' % (i, cost))
        if i%100 == 0:
            costs.append(cost)
    plt.subplot(122)
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('iteration (per tens)')
    plt.title('learning rate = '+str(learning_rate))
    return parameters

if __name__ == '__main__':
    print('2 layer neural network\n')
    parameters = two_layer_model(train_x, train_y, layers_dims=(n_x, n_h, n_y), num_iterations=3000, print_cost=True)
    print('-'*50)
    print('train set:\n')
    predictions_train = predict(train_x, train_y, parameters)
    print('-'*50)
    print('test set:\n')
    predictions_test = predict(test_x, test_y, parameters)
    print('-'*50)
    print('-'*50)
    print('4 layer neural network\n')
    parameters = L_layer_model(train_x, train_y, layers_dims_L, num_iterations=2500, print_cost=True)
    print('-'*50)
    print('train set:\n')
    pred_train = predict(train_x, train_y, parameters)
    print('-'*50)
    print('test set:\n')
    pred_test = predict(test_x, test_y, parameters)
    plt.show()
    print_mislabeled_images(classes, test_x, test_y, pred_test)
