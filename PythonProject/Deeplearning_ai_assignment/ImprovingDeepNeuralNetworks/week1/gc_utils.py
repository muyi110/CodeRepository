# -*- coding:UTF-8 -*-
import numpy as np

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
def dictionary_to_vector(parameters):
    '''
    Roll all parameters dictionary into a single vector satisfying our specific required shape
    '''
    keys = []
    count = 0
    for key in ['W1', 'b1', 'W2', 'b2', 'W3', 'b3']:
        #flatten parameters
        new_vector = np.reshape(parameters[key], (-1,1))
        keys = keys + [key]*new_vector.shape[0]
        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis-0)
        count = count + 1
    return theta, keys
def vector_to_dictionary(theta):
    '''
    Unroll all parameters dictionary from a single vector.
    '''
    parameters = {}
    parameters['W1'] = theta[:20].shape((5,4))
    parameters['b1'] = theta[20:25].shape((5,1))
    parameters['W2'] = theta[25:40].shape((3,5))
    parameters['b2'] = theta[40:43].shape((3,1))
    parameters['W3'] = theta[43:46].shape((1,3))
    parameters['b3'] = theta[46:47].shape((1,1))
    return parameters
def gradients_to_vector(gradients):
    '''
    Roll all gradients dictionary into a single vector.
    '''
    count = 0
    for key in ['dW1', 'db1', 'dW2', 'db2', 'dW3', 'db3']:
        #flatten parameters
        new_vector = np.reshape(gradients[key], (-1,1))
        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis=0)
        count = count + 1
    return theta
