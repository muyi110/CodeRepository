# -*- coding:UTF-8 -*-
import numbers
import numpy as np
import h5py
import matplotlib.pyplot as plt
from dnn_utils_v2 import *

plt.rcParams['figure.figsize'] = (5.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
np.random.seed(1)
#load data
def load_data():
    train_dataset = h5py.File('./datasets/train_catvnoncat.h5', 'r')
    train_set_x_orig = np.array(train_dataset['train_set_x'][:])
    train_set_y_orig = np.array(train_dataset['train_set_y'][:])
    test_dataset = h5py.File('./datasets/test_catvnoncat.h5', 'r')
    test_set_x_orig = np.array(test_dataset['test_set_x'][:])
    test_set_y_orig = np.array(test_dataset['test_set_y'][:])
    classes = np.array(test_dataset['list_classes'][:])
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes

# initialize parameters
def initialize_parameters(n_x, n_h, n_y):
    '''
    for 2 layer neural network
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
    np.random.seed(1)
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    assert(W1.shape == (n_h, n_x))
    assert(b1.shape == (n_h, 1))
    assert(W2.shape == (n_y, n_h))
    assert(b2.shape == (n_y, 1))
    parameters = {'W1':W1, 'b1':b1, 'W2':W2, 'b2':b2}
    return parameters
def initialize_parameters_deep(layer_dims):
    '''
    Arguments:
    layer_dims--python array(list) containing the dimensions of each layer
    Returns:
    parameters--python dictionary containing W b of each layer
    '''
    np.random.seed(1)
    parameters = {}
    L = len(layer_dims)
    for l in range(1, L):
        parameters['W'+str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) / np.sqrt(layer_dims[l-1])
        parameters['b'+str(l)] = np.zeros((layer_dims[l], 1))
        assert(parameters['W'+str(l)].shape == (layer_dims[l], layer_dims[l-1]))
        assert(parameters['b'+str(l)].shape == (layer_dims[l], 1))
    return parameters
# forward propagation module
def linear_forward(A, W, b):
    '''
    Implement the linear part of a layer's forward propagation
    Arguments:
    A--activations from previous layer, shape(size of previous, number of examples)
    W--weights matrix, shape(size of current layer, size of previous layer)
    b--bias vector, shape(size of current layer, 1)
    Returns:
    Z--the input of activation function
    cache--python tuple containing A, W, b
    '''
    Z = np.dot(W, A) + b
    assert(Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)
    return Z, cache
def linear_activation_forward(A_prev, W, b, activation):
    '''
    Arguments:
    A_pre--activations from previous layer, shape(size of previous, number of examples)
    W--weights matrix, shape(size of current layer, size of previous layer)
    b--bias vector, shape(size of current layer, 1)
    activation--string('sigmoid' or 'relu')
    Returns:
    A--output of the activation function
    cache--python tuple containing 'linear_cache' and 'activation_cache'
    '''
    if activation == 'sigmoid':
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)
    if activation == 'relu':
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    assert(A.shape ==(W.shape[0], A_prev.shape[1]))
    cache = (linear_cache, activation_cache)
    return A, cache
def L_model_forward(X, parameters):
    '''
    Implement forward propagation for L layer
    Arguments:
    X--data, shape(n_x, number of examples)
    parameters--output of initialize_parameters_deep
    Returns:
    AL--last post-activation value
    caches--python list contatining each cache of linear_relu_forward() and the cache of linear_sigmoid_forward()
    '''
    caches = []
    A = X
    L = len(parameters) // 2
    for l in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters['W'+str(l)], parameters['b'+str(l)], 'relu')
        caches.append(cache)
    A_prev = A
    AL, cache = linear_activation_forward(A_prev, parameters['W'+str(L)], parameters['b'+str(L)], 'sigmoid')
    caches.append(cache)
    assert(AL.shape == (1, X.shape[1]))
    return AL, caches
# compute cost
def compute_cost(AL, Y):
    '''
    Arguments:
    AL--probability vector of predictions, shape(1, number of examples)
    Y--labels, shape(1, number of examples)
    Returns:
    cost--cross-entropy cost
    '''
    m = Y.shape[1]
    cost = np.dot(np.log(AL), Y.T) + np.dot(np.log(1-AL), (1-Y).T)
    cost = -cost / m
    cost = cost.ravel()[0]
    assert(isinstance(cost, numbers.Real))
    return cost
# backward propagation module
def linear_backward(dZ, cache):
    '''
    Arguments:
    dZ--gradient of the cost with respect to the linear output(of current layer l)
    cache--tuple of value(A_prev, W, b) from the forward propagation
    Returns:
    dA_prev--gradient of cost with respect to activation(of the previous layer)
    dW--gradient(current layer)
    db--gradient(current layer)
    '''
    A_prev, W, b = cache
    m = A_prev.shape[1]
    dW = np.dot(dZ, A_prev.T) / m
    db = np.sum(dZ, axis=1, keepdims=True) / m
    dA_prev = np.dot(W.T, dZ)
    assert(dA_prev.shape == A_prev.shape)
    assert(dW.shape == W.shape)
    assert(db.shape == b.shape)
    return dA_prev, dW, db
def linear_activation_backward(dA, cache, activation):
    '''
    Arguments:
    dA--post-activation gradient for current layer l
    cache--tuple of value(linear_cache, activation_cache)
    activation--string 'sigmoid' or 'relu'
    Returns:
    dA_prev--gradient(of the previous layer l-1)
    dW--gradient(current layer)
    db--gradient(current layer)
    '''
    linear_cache, activation_cache = cache
    if activation == 'relu':
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif activation == 'sigmoid':
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    return dA_prev, dW, db
def L_model_backward(AL, Y, caches):
    '''
    Arguments:
    AL--probability vector, output of the forward propagation
    Y--labels
    caches--list of caches containing:
            each cache of linear_activation_forward() with 'relu'
            the cache of linear_activation_forward() with 'sigmoid'
    Returns:
    grads--dictionary with gradients dA1,dW1,db1,dA2,dW2,db2,...
    '''
    grads = {}
    L = len(caches)
    m = Y.shape[1]
    Y = Y.reshape(AL.shape)
    dAL = -(np.divide(Y, AL) - np.divide(1-Y, 1-AL))
    current_cache = caches[L-1]
    grads['dA'+str(L)], grads['dW'+str(L)], grads['db'+str(L)] = linear_activation_backward(dAL, current_cache, 'sigmoid')
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads['dA'+str(l+2)], current_cache, 'relu')
        grads['dA'+str(l+1)] = dA_prev_temp
        grads['dW'+str(l+1)] = dW_temp
        grads['db'+str(l+1)] = db_temp
    return grads
# update parameters
def update_parameters(parameters, grads, learning_rate):
    '''
    Arguments:
    parameters--python dictionary
    grads--python dictionary, output of L_model_backward
    learning_rate--hyparameter
    Returns:
    parameters--dictionary
    '''
    L = len(parameters) // 2
    for l in range(L):
        parameters['W'+str(l+1)] = parameters['W'+str(l+1)] - learning_rate * grads['dW'+str(l+1)]
        parameters['b'+str(l+1)] = parameters['b'+str(l+1)] - learning_rate * grads['db'+str(l+1)]
    return parameters
#predict
def predict(X, y, parameters):
    '''
    Arguments:
    X--data set of examples
    y--labels
    parameters--from the trained model
    Returns:
    p--predictions for the giveb dataset X
    '''
    m = X.shape[1]
    n = len(parameters) // 2
    p = np.zeros((1, m))
    probas, caches = L_model_forward(X, parameters)
    for i in range(probas.shape[1]):
        if probas[0, i] > 0.5:
            p[0, i] = 1
        else:
            p[0, i] = 0
    print('Accuracy '+str(np.sum((p==y)/m)))
    return p
def print_mislabeled_images(classes, X, y, p):
    '''
    plots images where predictions and truth were different
    X--dataset
    y--true labels
    p--predictions
    '''
    a = p + y
    mislabeled_indices = np.asarray(np.where(a==1))
    plt.rcParams['figure.figsize'] = (40.0, 40.0)
    num_images = len(mislabeled_indices[0])
    for i in range(num_images):
        index = mislabeled_indices[1][i]
        plt.subplot(2, num_images, i+1)
        plt.imshow(X[:,index].reshape(64,64,3), interpolation='nearest')
        plt.axis('off')
        plt.title('prediction: '+classes[int(p[0,index])].decode('utf-8')+'\nclass: '+classes[y[0,index]].decode('utf-8'))
    plt.show()
