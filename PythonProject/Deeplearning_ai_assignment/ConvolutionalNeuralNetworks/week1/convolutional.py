# -*- coding:UTF-8 -*-
import numpy as np
import h5py
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (5.0, 4.0)
plt.rcParams['image.interpolation'] = 'nearest' 
plt.rcParams['image.cmap'] = 'gray'
np.random.seed(1)

# zero pad
def zero_pad(X, pad):
    '''
    The padding is applied to the height and width of an image
    Arguments:
    X--python numpy array, of shape(m,n_H,n_W,n_c)
    pad--integer, amount of padding around each image on vertical and horizontal dimensions.
    Returns:
    X_pad--padded image of shape(m,n_H+2*pad,n_W+2*pad,n_c)
    '''
    X_pad = np.pad(X, ((0,0),(pad,pad),(pad,pad),(0,0)),'constant',constant_values=0)
    return X_pad
# convolution single step
def conv_single_step(a_slice_prev, W, b):
    '''
    Apply one filter defined by parameters W on a single slice of the output activation.
    Arguments:
    a_slice_prev--slice of input data of shape(f, f, n_c_prev)
    W--weight parameters contained in a window, matrix of shape(f, f, n_c_prev)
    b--bias parameters contained in a window, matrix of shape(1, 1, 1)
    Returns:
    Z--a scalar value, result of convolving the sliding windows(W, b) on a slice x of the input data
    '''
    s = np.multiply(a_slice_prev, W) + b
    Z = np.sum(s)
    return Z
# convolution forward
def conv_forward(A_prev, W, b, hparameters):
    '''
    Implements the forward propagation for convolution function.
    Arguments:
    A_prev--output activations of the previous layer, of shape(m, n_H_prev, n_W_prev, n_c_prev)
    W--weights, numpy array of shape(f, f, n_c_prev, n_c)
    b--biases, numpy array of shape(1, 1, 1, n_c)
    hparameters--python dictionary containing 'stride' and 'pad'
    Returns:
    Z-- convolution output, numpy array of shape(m, n_H, n_W, n_c)
    cache--cache of values needed for the backward
    '''
    (m, n_H_prev, n_W_prev, n_c_prev) = A_prev.shape
    (f, f, n_c_prev, n_c) = W.shape
    stride = hparameters['stride']
    pad = hparameters['pad']
    #compute the dimensions of convolution output
    n_H = 1 + int((n_H_prev - f + 2*pad) / stride)
    n_W = 1 + int((n_W_prev - f + 2*pad) / stride)
    #initialize the output volume Z with zeros
    Z = np.zeros((m, n_H, n_W, n_c))
    #creat A_prev_pad by padding A_prev
    A_prev_pad = zero_pad(A_prev, pad)
    for sample in range(m):
        a_prev_pad = A_prev_pad[sample]
        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_c):
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f
                    a_slice_prev = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
                    Z[sample, h, w, c] = np.sum(np.multiply(a_slice_prev, W[:,:,:,c]) + b[:,:,:,c])
    assert(Z.shap == (m, n_H, n_W, n_c))
    cache = (A_prev, W, b, hparameters)
    return Z, cache
#pool forward
def pool_forward(A_prev, hparameters, mode='max'):
    '''
    Arguments:
    A_prev--input data,numpy array of shape(m, n_H_prev, n_W_prev, n_c_prev)
    hparameters--python dictionary containing 'stride' and 'f'
    mode--the pooling mode you would like to use, string('max' or 'average')
    Returns:
    A--output of pool layer, a numpy array of shape(m, n_H, n_W, n_C)
    cache--cache used in the backward pass of the pooling layer, tuple
    '''
    (m, n_H_prev, n_W_prev, n_c_prev) = A_prev.shape
    f = hparameters['f']
    stride = hparameters['stride']
    #define the dimensions of the output
    n_H = int(1 + (n_H_prev - f) / stride)
    n_W = int(1 + (n_W_prev - f) / stride)
    n_c = n_c_prev
    #initialize the output matrix A
    A = np.zeros((m, n_H, n_W, n_c))
    for i in range(m):
        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_c):
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f
                    a_prev_slice = A_prev[i, vert_start:vert_end, horiz_start:horiz_end, c]
                    if mode == 'max':
                        A[i, h, w, c] = np.max(a_prev_slice)
                    elif mode == 'average':
                        A[i, h, w, c] = np.mean(a_prev_slice)
    cache = (A_prev, hparameters)
    assert(A.shape == (m, n_H, n_W, n_c))
    return A, cache
# 卷积神经网络的反向传播代码实现参见作业部分，这里就不写了
