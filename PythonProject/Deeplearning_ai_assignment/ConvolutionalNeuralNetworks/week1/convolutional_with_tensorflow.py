#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import math
import numpy as np
print('numpy version is: '+str(np.__version__))
import h5py
import matplotlib.pyplot as plt
import matplotlib as mpl
print('matplotlib version is: '+str(mpl.__version__))
import scipy
from scipy import ndimage
import tensorflow as tf
print('tensorflow version is: '+str(tf.__version__))
from tensorflow.python.framework import ops
from cnn_utils import *

np.random.seed(1)
#create placeholders
def create_placeholders(n_H0, n_W0, n_c0, n_y):
    '''
    Arguments:
    n_H0--scalar, height of an input image
    n_W0--scalar, width of an input image
    n_c0--scalar, number of channels of input
    n_y--scalar, number of classes
    Returns:
    X--placeholder for data input, of shape(None, n_H0, n_W0, n_c0) dtype "float"
    Y--placeholder for input labels, of shape(None, n_y) dtype "float"
    '''
    X = tf.placeholder(name='X', shape=(None, n_H0, n_W0, n_c0), dtype=tf.float32)
    Y = tf.placeholder(name='Y', shape=(None, n_y), dtype=tf.float32)
    return X, Y
#initialize parameters
def initialize_parameters():
    '''
    initialize weight parameters to bulid a neural network with tensorflow, shape are:
        W1:[4, 4, 3, 8]
        W2:[2, 2, 8, 16]
    Arguments:None
    Returns:
    parameters--python dictionary of tensors containing W1, W2
    '''
    tf.set_random_seed(1)
    W1 = tf.get_variable(name='W1', dtype=tf.float32, shape=(4, 4, 3, 8), initializer=tf.contrib.layers.xavier_initializer(seed=0))
    W2 = tf.get_variable(name='W2', dtype=tf.float32, shape=(2, 2, 8, 16), initializer=tf.contrib.layers.xavier_initializer(seed=0))
    b1 = tf.Variable(tf.zeros([8]), name='b1')
    b2 = tf.Variable(tf.zeros([16]), name='b2')
    parameters = {'W1':W1, 'W2':W2, 'b2':b2, 'b1':b1}
    return parameters
#forward propagation
def forward_propagation(X, parameters):
    '''
    conv2d->relu->maxpool->conv2d->relu->maxpool->flatten->fc
    Arguments:
    X--input dataset placeholder, of shape(input size, number of examples)
    parameters--python dictionary containing W1, W2
    Returns:
    Z3--the output of the last linear unit
    '''
    W1 = parameters['W1']
    W2 = parameters['W2']
    #conv2d: stride of 1, padding 'same'
    Z1 = tf.nn.conv2d(input=X, filter=W1, strides=(1, 1, 1, 1), padding='SAME')
    A1 = tf.nn.relu(Z1+b1)
    P1 = tf.nn.max_pool(value=A1, ksize=(1, 8, 8, 1), strides=(1, 8, 8, 1), padding='SAME')
    Z2 = tf.nn.conv2d(input=P1, filter=W2, strides=(1, 1, 1, 1), padding='SAME')
    A2 = tf.nn.relu(Z2+b2)
    P2 = tf.nn.max_pool(value=A2, ksize=(1, 4, 4, 1), strides=(1, 4, 4, 1), padding='SAME')
    P2 = tf.contrib.layers.flatten(inputs=P2)
    Z3 = tf.contrib.layers.fully_connected(P2, 6, activation_fn=None)
    return Z3
#compute cost
def compute_cost(Z3, Y):
    '''
    Arguments:
    Z3--output of forward propagation
    Y--labels placeholders
    Returns:
    cost--tensor of cost function
    '''
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=Z3, labels=Y))
    return cost
# model
def model(X_train, Y_train, X_test, Y_test, learning_rate=0.009, num_epochs=200, minibatch_size=64, print_cost=True):
    '''
    X_train--training set, of shape(None, 64, 64, 3)
    Y_train--training set, of shape(None, n_y=6)
    X_test--test set, of shape(None, 64, 64, 3)
    Y_test--test set, of shape(None, n_y=6)
    learning_rate--learning rate of the optimization loop
    num_epochs--number of epochs of loop
    minibatch_size--size of minibatch
    print_cost--True to print cost every 100 epochs
    Returns:
    train_accuracy--real number, accurary on train set
    test_accurary--real number, accurary in test set
    parameters--parameters learned by model
    '''
    ops.reset_default_graph()
    tf.set_random_seed(1)
    seed = 3
    (m, n_H0, n_W0, n_c0) = X_train.shape
    n_y = Y_train.shape[1]
    costs = []
    #placeholders
    X, Y = create_placeholders(n_H0, n_W0, n_c0, n_y)
    #initializer
    parameters = initialize_parameters()
    #forward propagation
    Z3 = forward_propagation(X, parameters)
    #cost
    cost = compute_cost(Z3, Y)
    optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    #start the session
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(num_epochs):
            minibatch_cost = 0
            num_minibatches = int(m / minibatch_size)
            seed += 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _, temp_cost = sess.run([optimizer, cost], feed_dict={X:minibatch_X, Y:minibatch_Y})
                minibatch_cost += temp_cost / num_minibatches
            if print_cost == True and epoch % 5 == 0:
                print('Cost after epoch %i: %f' % (epoch, minibatch_cost))
            if print_cost == True and epoch % 1 == 0:
                costs.append(minibatch_cost)
        #plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('interations')
        plt.title('Learning rate = '+str(learning_rate))
        plt.show()
        # calculate the correct predictions
        predict_op = tf.argmax(Z3, 1)
        correct_prediction = tf.equal(predict_op, tf.argmax(Y, 1))
        accurary = tf.reduce_mean(tf.cast(correct_prediction, 'float'))
        print('-'*50)
        print(accurary)
        train_accurary = accurary.eval({X:X_train, Y:Y_train})
        test_accurary = accurary.eval({X:X_test, Y:Y_test})
        print('Train accurary: ',train_accurary)
        print('Test accurary: ', test_accurary)
        return train_accurary, test_accurary, parameters

if __name__ == '__main__':
    X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()
    X_train = X_train_orig / 255
    X_test = X_test_orig / 255
    Y_train = convert_to_one_hot(Y_train_orig, 6).T
    Y_test = convert_to_one_hot(Y_test_orig, 6).T
    print('-'*50)
    print('number of training examples = '+str(X_train.shape[0]))
    print('number of test examples = '+str(X_test.shape[0]))
    print('X_train shape: '+str(X_train.shape))
    print('Y_train shape: '+str(Y_train.shape))
    print('X_test shape: '+str(X_test.shape))
    print('Y_test shape: '+str(Y_test.shape))
    print('-'*50)
    conv_layers = {}
    _, _, parameters = model(X_train, Y_train, X_test, Y_test)
