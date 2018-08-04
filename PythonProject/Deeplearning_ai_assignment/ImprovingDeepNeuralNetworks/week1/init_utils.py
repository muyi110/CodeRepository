# -*- coding:UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import h5py
import sklearn
import sklearn.datasets

def sigmoid(x):
    '''
    Arguments:
    x--A scalar or numpy array of any size
    Return:
    s--sigmoid(x)
    '''
    s = 1 / (1 + np.exp(-x))
    return s
def relu(x):
    '''
    Arguments:
    x--A scalar or numpy array of any size
    Return:
    s--relu(x)
    '''
    s = np.maximum(0, x)
    return s
def forward_propagation(X, parameters):
    '''
    Arguments:
     X--input dataset, of shape(input size, number of examples)
     Y--labels, of shape(1, number of examples)
     parameters--python dictionary containing W b
                 W_i--weight matrix
                 b_i--bias matrix
                 i = (1, 2, 3)
    Returns:
     loss--the loss function(vanilla logistic loss)
    '''
    # retrieve parameters
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']
    # Linear->relu->linear->relu->linear->sigmoid
    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = relu(Z2)
    Z3 = np.dot(W3, A2) + b3
    A3 = sigmoid(Z3)
    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3)
    return A3, cache
def backward_propagation(X, Y, cache):
    '''
    Arguments:
     X--input dataset, of shape(input size, number of examples)
     Y--labels, of shape(1, number of examples)
     cache--tuple, cache output from forward_propagation()
     Returns:
     gradients--A dictionary with gradients with respect to each parameter, activation and pre-activation variables.
    '''
    m = X.shape[1]
    (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3) = cache
    dZ3 = 1. / m * (A3 - Y)
    dW3 = np.dot(dZ3, A2.T)
    db3 = np.sum(dZ3, axis=1, keepdims=True)
    dA2 = np.dot(W3.T, dZ3)
    dZ2 = np.multiply(dA2, np.int64(A2>0))
    dW2 = np.dot(dZ2, A1.T)
    db2 = np.sum(dZ2, axis=1, keepdims=True)
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = np.multiply(dA1, np.int64(A1>0))
    dW1 = np.dot(dZ1, X.T)
    db1 = np.sum(dZ1, axis=1, keepdims=True)
    gradients = {'dZ3':dZ3, 'dW3':dW3, 'db3':db3,
                 'dA2':dA2, 'dZ2':dZ2, 'dW2':dW2, 'db2':db2,
                 'dA1':dA1, 'dZ1':dZ1, 'dW1':dW1, 'db1':db1
                 }
    return gradients
def update_parameters(parameters, grads, learning_rate):
    '''
    Arguments:
    parameters--python dictionary
    grads--python dictionary
    Returns:
    parameters--python dictionary containing updated parameters.
    '''
    L = len(parameters) // 2
    # update rule for each parameter
    for k in range(L):
        parameters['W'+str(k+1)] -= learning_rate * grads['dW'+str(k+1)]
        parameters['b'+str(k+1)] -= learning_rate * grads['db'+str(k+1)]
    return parameters
def compute_loss(A3, Y):
    '''
    Arguments:
    A3--post-activation, output of forward propagation
    Y--labels, of shape(1, number of examples)
    Returns:
    loss--value of the loss function
    '''
    m = Y.shape[1]
    logprobs = np.multiply(-np.log(A3), Y)+np.multiply(-np.log(1-A3), 1-Y)
    loss = 1. / m * np.nansum(logprobs)
    return loss
def predict(X, y, parameters):
    '''
    Arguments:
    X--dataset you would like to label
    y--labels
    parameters--parameters of trained model
    Returns:
    p--predictions for the given dataset X
    '''
    m = X.shape[1]
    p = np.zeros((1, m), dtype=np.int)
    # forward propagation
    A3, cache = forward_propagation(X, parameters)
    # convert probas to 0/1 predictions
    for i in range(0, A3.shape[1]):
        if A3[0, i] > 0.5:
            p[0, i] = 1
        else:
            p[0, i] = 0
    print('Accuary: '+str(np.mean((p[0,:]==y[0,:]))))
    return p
def predict_dec(parameters, X):
    '''
    Used for plotting decision boundary
    Arguments:
    X--dataset you would like to label
    parameters--parameters of trained model
    Returns:
    predictions--vector of predictions of model
    '''
    A3, cache = forward_propagation(X, parameters)
    predictions = (A3 > 0.5)
    return predictions
def plot_decision_boundary(model, X, y):
    # set min and max values and give it some padding
    x_min, x_max = X[0,:].min()-1, X[0,:].max()+1
    y_min, y_max = X[1,:].min()-1, X[1,:].max()+1
    h = 0.01
    # generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # predict the function value for the whole grid
    Z = model(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[0, :], X[1, :], c=np.squeeze(y), cmap=plt.cm.Spectral)
    plt.show()
def load_dataset():
    np.random.seed(1)
    train_X, train_Y = sklearn.datasets.make_circles(n_samples=300, noise=.05)
    test_X, test_Y = sklearn.datasets.make_circles(n_samples=100, noise=.05)
    # visualize the data
    plt.scatter(train_X[:, 0], train_X[:, 1], c = np.squeeze(train_Y), s=40, cmap=plt.cm.Spectral)
    train_X = train_X.T
    train_Y = train_Y.reshape((1, train_Y.shape[0]))
    test_X = test_X.T
    test_Y = test_Y.reshape((1, test_Y.shape[0]))
    return train_X, train_Y, test_X, test_Y
