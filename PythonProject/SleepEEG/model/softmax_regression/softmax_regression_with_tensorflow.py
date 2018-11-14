#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys
sys.path.append("../../") # 将其他模块路径添加到系统搜索路径
import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from data_processing import data_processing

PATH = "../../dataset/"
labels_dict = {"0":"awake", "1":"light_sleep", "2":"deep_sleep"}

def random_mini_batches(X, Y, mini_batch_size = 32, seed = 0):   
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:]
    shuffled_Y = Y[permutation]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size)
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches

tf.set_random_seed(42)
np.random.seed(42)

def softmax_regression_model(X, y, initializer=None, seed=42, learning_rate=0.01):
    n_inputs_including_bias = int(X.get_shape()[1])# 获取输入的特征数
    n_outputs = 3 
    with tf.name_scope("softmax_regression"):
        with tf.name_scope("model"):
            if initializer == None:
                initializer = tf.random_uniform([n_inputs_including_bias, n_outputs], -1.0, 1.0, seed = seed)
            theta = tf.Variable(initializer)
            # logits = tf.matmul(X, theta)
            logits = tf.layers.dense(X, n_outputs)
            y_proba = tf.nn.softmax(logits)
        with tf.name_scope("train"):
            xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
            loss = tf.reduce_mean(xentropy, name="loss")
            optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
            training_op = optimizer.minimize(loss)
        with tf.name_scope("init"):
            init = tf.global_variables_initializer()
       
        # 构建准确率节点
        correct = tf.nn.in_top_k(logits, y, 1)
        accurcy = tf.reduce_mean(tf.cast(correct, tf.float32))
        return y_proba, loss, training_op, init, accurcy

def fit(train_x, train_y, training_op, y_proba, accurcy, loss, init, n_epochs=10001, batch_size=32):
    with tf.Session() as sess:
        start_epoch = 0
        sess.run(init)
        seed = 0
        for epoch in range(start_epoch, n_epochs):
            seed += 1
            n_batches = random_mini_batches(train_x, train_y, mini_batch_size = batch_size, seed = seed)
            for batch in n_batches:
                X_batch, y_batch = batch
                sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
            if epoch % 500 == 0:
                loss_val, sorce = sess.run([loss, accurcy], feed_dict={X:train_x, y:train_y})
                print("Epoch: ", epoch, "\tLoss: ", loss_val, "\taccuracy: {:.2f}%".format(sorce*100))

        y_proba_val = accurcy.eval(feed_dict={X:X_test, y:test_y})
        print("test accuracy: {:.2f}%".format(y_proba_val*100))

if __name__ == "__main__":
    train_x, train_y, test_x, test_y = data_processing.getsample(path = PATH, time_interval=10, 
                                                                 train_proportion=0.7, filter_flag=False)
    # sample shape = (number of samples, features)
    train_x = np.array(train_x).mean(axis=2)
    train_y = np.array(train_y)
    test_x = np.array(test_x).mean(axis=2)
    test_y = np.array(test_y)
    assert len(train_x) == len(train_y)
    assert len(test_x) == len(test_y)
    print("train sample shape: ", train_x.shape)
    print("train sample label shape: ", train_y.shape)
    print("test sample shape: ", test_x.shape)
    print("test sample label shape: ", test_y.shape)
    print("awake number: {}  light sleep number: {}  deep sleep number: {}".format(np.sum(train_y==0)+np.sum(test_y==0), np.sum(train_y==1)+np.sum(test_y==1), np.sum(train_y==2)+np.sum(test_y==2)))
    #plt.show()
    # one-hot 编码
    X_train = np.c_[np.ones([len(train_x), 1]), train_x] # 添加偏置
    X_test = np.c_[np.ones([len(test_x), 1]), test_x]
    
    n_epochs = 2001
    batch_size = 32
    n_inputs = X_train.shape[1]
    X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
    y = tf.placeholder(tf.int32, shape=(None), name="y")
    y_proba, loss, training_op, init, accurcy = softmax_regression_model(X, y)
    fit(X_train, train_y, training_op, y_proba, accurcy, loss, init, n_epochs=n_epochs, batch_size=batch_size)
