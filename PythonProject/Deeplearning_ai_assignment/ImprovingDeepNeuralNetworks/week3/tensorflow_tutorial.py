#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
from tf_utils import *
np.random.seed(1)
def create_placeholders(n_x, n_y):
    '''
    Arguments:
    n_x--scalar, size of an image vector(here 12288)
    n_y--scalar, number of classes(here 6)
    Returns:
    X--placeholder for data input, shape(n_x, None), type 'float'
    Y--placeholder for labels, shape(n_y, None), type 'float'
    '''
    X = tf.placeholder(dtype=tf.float32, shape=(n_x, None), name='X')
    Y = tf.placeholder(dtype=tf.float32, shape=(n_y, None), name='Y')
    return X, Y
def initialize_parameters():
    '''
    Initializes parameters, the shape are:
        W1:[25, 12288]
        b1:[25, 1]
        W2:[12, 25]
        b2:[12, 1]
        W3:[6, 12]
        b3:[6, 1]
    Returns:
    parameters--python dictionary
    '''
    tf.set_random_seed(1)
    W1 = tf.get_variable('W1', [25, 12288], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b1 = tf.get_variable('b1', [25, 1], initializer=tf.zeros_initializer())
    W2 = tf.get_variable('W2', [12, 25], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b2 = tf.get_variable('b2', [12, 1], initializer=tf.zeros_initializer())
    W3 = tf.get_variable('W3', [6, 12], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b3 = tf.get_variable('b3', [6, 1], initializer=tf.zeros_initializer())
    parameters = {'W1':W1, 'b1':b1, 'W2':W2,
                  'b2':b2, 'W3':W3, 'b3':b3}
    return parameters
def forward_propagation(X, parameters):
    '''
    Arguments:
    X--input dataset placeholder, shape(input size, number of examples)
    parameters--dictionary
    Returns:
    Z3--the output of the last linear unit
    '''
    #Retrieve the parameters
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']

    Z1 = tf.add(tf.matmul(W1, X), b1)
    A1 = tf.nn.relu(Z1)
    Z2 = tf.add(tf.matmul(W2, A1), b2)
    A2 = tf.nn.relu(Z2)
    Z3 = tf.add(tf.matmul(W3, A2), b3)
    return Z3
def compute_cost(Z3, Y):
    '''
    Arguments:
    Z3--the output of forward propagation(output fo the last linear layer)
    Y--labels, same shape as Z3
    Returns:
    cost--tensor of the cost function
    '''
    logits = tf.transpose(Z3)
    labels = tf.transpose(Y)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=labels))
   
    return cost
def model(X_train, Y_train, X_test, Y_test, learning_rate=0.0001, num_epochs=1500, minibatch_size=32, print_cost=True):
    '''
    Arguments:
    X_train--training set, shape(12288, number of training examples
    Y_train--training set labels
    X_test--
    Y_test--
    learning_rate--
    num_epochs--numbers of loop
    minibatch_size--
    print_cost--True to print cost every 1000 epochs
    Returns:
    parameters--updated parameters by model
    '''
    ops.reset_default_graph()
    tf.set_random_seed(1)
    seed = 3
    (n_x, m) = X_train.shape
    n_y = Y_train.shape[0]
    costs = []
    X, Y = create_placeholders(n_x, n_y)
    parameters = initialize_parameters()
    #add L2 regularization
    tf.add_to_collection(tf.GraphKeys.WEIGHTS, parameters['W1'])
    tf.add_to_collection(tf.GraphKeys.WEIGHTS, parameters['W2'])
    tf.add_to_collection(tf.GraphKeys.WEIGHTS, parameters['W3'])
    regularization = tf.contrib.layers.l2_regularizer(scale=0.024)
    regularization_term = tf.contrib.layers.apply_regularization(regularizer=regularization)

    Z3 = forward_propagation(X, parameters)
    cost = compute_cost(Z3, Y)
    cost += tf.reduce_mean(regularization_term)

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    #start the session to compute the tensorflow graph
    with tf.Session() as sess:
        #run the initialization
        sess.run(init)
        for epoch in range(num_epochs):
            epoch_cost = 0
            num_minibatches = int(m/minibatch_size)
            seed += 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _, minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y:minibatch_Y})
                epoch_cost += minibatch_cost / num_minibatches
            if print_cost and epoch % 100 == 0:
                print('Cost after epoch %i: %f' % (epoch, epoch_cost))
            if print_cost and epoch % 5 == 0:
                costs.append(epoch_cost)
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title('Learning rate = '+str(learning_rate))
        plt.show()
        parameters = sess.run(parameters)
        print('-'*50)
        print('Parameters have been trained')
        correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))
        accuary = tf.reduce_mean(tf.cast(correct_prediction, 'float'))
        print('Train accuracy:', accuary.eval({X:X_train, Y:Y_train}))
        print('Test accuracy:', accuary.eval({X:X_test, Y:Y_test}))
        return parameters

if __name__ == '__main__':
    X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()
    #Flatten the training and test images
    X_train_flatten = X_train_orig.reshape(X_train_orig.shape[0], -1).T
    X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
    #Normalize image vectors
    X_train = X_train_flatten / 255.
    X_test = X_test_flatten / 255.
    # convert labels to one hot matrices
    Y_train = convert_to_one_hot(Y_train_orig, 6)
    Y_test = convert_to_one_hot(Y_test_orig, 6)
    print('-'*50)
    print("number of training examples = "+str(X_train.shape[1]))
    print("number of test examples = "+str(X_test.shape[1]))
    print('X_train shape: '+str(X_train.shape))
    print('Y_train shape: '+str(Y_train.shape))
    print('X_test shape: '+str(X_test.shape))
    print('Y_test shape: '+str(Y_test.shape))
    print('-'*50)
    parameters = model(X_train, Y_train, X_test, Y_test)
