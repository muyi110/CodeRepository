#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import math
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops

def load_data(path='./mnist.npz'):
    f = np.load(path)
    X_train, y_train = f['x_train'], f['y_train']
    X_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (X_train, y_train), (X_test, y_test)
# one-hot encoding
def convert_to_one_hot(Y, class_number):
    y_label = np.eye(class_number)[Y.reshape(-1)]
    return y_label

np.random.seed(1)
def initialize_parameters():
    tf.set_random_seed(1)
    W1 = tf.get_variable(name='W1', dtype=tf.float32, shape=[3,3,1,32], 
                         initializer=tf.contrib.layers.xavier_initializer(seed=0))
    W2 = tf.get_variable(name='W2', dtype=tf.float32, shape=[3,3,32,32], 
                         initializer=tf.contrib.layers.xavier_initializer(seed=0))
    W3 = tf.get_variable(name='W3', dtype=tf.float32, shape=[3,3,32,64], 
                         initializer=tf.contrib.layers.xavier_initializer(seed=0))
    W4 = tf.get_variable(name='W4', dtype=tf.float32, shape=[3,3,64,64], 
                         initializer=tf.contrib.layers.xavier_initializer(seed=0))
    b1 = tf.Variable(tf.zeros([32]), name='b1')
    b2 = tf.Variable(tf.zeros([32]), name='b2')
    b3 = tf.Variable(tf.zeros([64]), name='b3')
    b4 = tf.Variable(tf.zeros([64]), name='b4')
    parameters = {'W1':W1, 'W2':W2, 'W3':W3, 'W4':W4, 'b1':b1, 'b2':b2, 'b3':b3, 'b4':b4}
    return parameters

def forward_propagation(X, parameters):
    W1 = parameters['W1']
    W2 = parameters['W2']
    W3 = parameters['W3']
    W4 = parameters['W4']
    b1 = parameters['b1']
    b2 = parameters['b2']
    b3 = parameters['b3']
    b4 = parameters['b4']
    Z1 = tf.nn.conv2d(input=X, filter=W1, strides=(1,1,1,1), padding='SAME')
    BN1 = tf.layers.batch_normalization(inputs=Z1)
    A1 = tf.nn.relu(BN1+b1)
    Z2 = tf.nn.conv2d(input=A1, filter=W2, strides=(1,1,1,1), padding='SAME')
    BN2 = tf.layers.batch_normalization(inputs=Z2)
    A2 = tf.nn.relu(BN2+b2)
    P1 = tf.nn.max_pool(value=A2, ksize=(1,2,2,1), strides=(1,2,2,1), padding='VALID')
    
    Z3 = tf.nn.conv2d(input=P1, filter=W3, strides=(1,1,1,1), padding='SAME')
    BN3 = tf.layers.batch_normalization(inputs=Z3)
    A3 = tf.nn.relu(BN3+b3)
    Z4 = tf.nn.conv2d(input=A3, filter=W4, strides=(1,1,1,1), padding='SAME')
    BN4 = tf.layers.batch_normalization(inputs=Z4)
    A4 = tf.nn.relu(BN4+b4)
    P2 = tf.nn.max_pool(value=A4, ksize=(1,2,2,1), strides=(1,2,2,1), padding='VALID')
    
    P2 = tf.contrib.layers.flatten(inputs=P2)
    fc1 = tf.layers.dense(P2, 512, activation=None, name='fc1')
    fc1_BN = tf.layers.batch_normalization(inputs=fc1)
    fc1_output = tf.nn.relu(fc1_BN)
    fc1_dropout = tf.layers.dropout(fc1_output, 0.2)
    fc2 = tf.layers.dense(fc1_dropout, 10, activation=tf.nn.softmax, name='fc2')
    return fc2

def compute_cost(fc2, Y):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=fc2, labels=Y))
    return cost

def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
    """
    Creates a list of random minibatches from (X, Y)
    
    Arguments:
    X -- input data, of shape (input size, number of examples) (m, Hi, Wi, Ci)
    Y -- true "label" vector, of shape (1, number of examples) (m, n_y)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.
    
    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:,:,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:,:,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches

def model(X_train, Y_train, X_test, Y_test, learning_rate=0.0001, num_epochs=60, minibatch_size=64, print_cost=True):
    ops.reset_default_graph()
    tf.set_random_seed(1)
    seed = 3
    m = X_train.shape[0]
    X = tf.placeholder(name='X', shape=(None, 28, 28, 1), dtype=tf.float32)
    Y = tf.placeholder(name='Y', shape=(None, 10), dtype=tf.float32)
    parameters = initialize_parameters()
    fc2 = forward_propagation(X, parameters)
    cost = compute_cost(fc2, Y)
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
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
            if print_cost:
                print('Cost after epoch%i cost: %f' % (epoch, minibatch_cost))
        predict_op = tf.argmax(fc2, 1)
        correct_prediction = tf.equal(predict_op, tf.argmax(Y, 1))
        accurary = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print('-'*50)
        train_acc = 0
        test_acc = 0
        #一次加载一部分数据，全部加载，电脑内存太小，会卡死
        for i in range(600):
            train_acc += accurary.eval(feed_dict={X:X_train[i*100:(i+1)*100, :, :, :], Y:Y_train[i*100:(i+1)*100, :]})
        for i in range(100):
            test_acc += accurary.eval(feed_dict={X:X_test[i*100:(i+1)*100,:,:,:], Y:Y_test[i*100:(i+1)*100, :]})
        print("train accurary: ", train_acc / (600))
        print("test accurary: ", test_acc/ (100))
if __name__ == "__main__":
    (X_train, y_train), (X_test, y_test) = load_data()
    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    Y_train = convert_to_one_hot(y_train, 10)
    Y_test = convert_to_one_hot(y_test, 10)
    print("Y_train shape: ", Y_train.shape)
    print("Y_test shape: ", Y_test.shape)
    model(X_train, Y_train, X_test, Y_test)
