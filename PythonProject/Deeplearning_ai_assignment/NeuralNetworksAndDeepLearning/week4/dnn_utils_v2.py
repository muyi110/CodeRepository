# -*- coding:UTF-8 -*-
import numpy as np

def sigmoid(Z):
    '''
    Arguments:
    Z--numpy array of any shape
    Returns:
    A--output of sigmoid(z), same shape as Z
    cache--return Z as well, useful during backpropagation
    '''
    A = 1 / (1 + np.exp(-Z))
    cache = Z
    return A, cache
def relu(Z):
    '''
    Arguments:
    Z--output of the linear layer, of any shape
    Returns:
    A--post-activation parameter, of the same shape as Z
    cache--return Z as well
    '''
    A = np.maximum(0, Z)
    assert(A.shape == Z.shape)
    cache = Z
    return A, cache
def relu_backward(dA, cache):
    '''
    Arguments:
    dA--post-activation gradient of any shape
    cache--Z 
    Returns:
    dZ--gradient of the cost with respect to Z
    '''
    Z = cache
    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0 #boolean array as the indices
    assert(dZ.shape == Z.shape)
    return dZ
def sigmoid_backward(dA, cache):
    '''
    Arguments:
    dA--post-activation gradient of any shape
    cache--Z 
    Returns:
    dZ--gradient of the cost with respect to Z
    '''
    Z = cache
    s = 1 / (1 + np.exp(-Z))
    dZ = dA * s * (1-s)
    assert(dZ.shape == Z.shape)
    return dZ
