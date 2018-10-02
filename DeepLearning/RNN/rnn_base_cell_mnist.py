#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import fully_connected

tf.set_random_seed(42)
n_steps = 28
n_inputs = 28 # 输入实例的特征数
n_neurons = 150 # 一个 cell 的神经元个数
n_outputs = 10

learning_rate = 0.001

X = tf.placeholder(tf.float32, shape=[None, n_steps, n_inputs], name="X")
y = tf.placeholder(tf.int32, shape=[None], name="y") # 标签

# basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons)
# # 构建创建 RNN 的节点
# outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32)
# 指定 RNN 权重的初始化方式
with tf.variable_scope("rnn", initializer=tf.contrib.layers.variance_scaling_initializer()):
    basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons)
    # 构建创建 RNN 的节点
    outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32)

logits = tf.layers.dense(states, n_outputs, kernel_initializer=tf.contrib.layers.xavier_initializer())
# logits = fully_connected(states, n_outputs, activation_fn=None)
# 计算代价函数
xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
loss = tf.reduce_mean(xentropy)
# 构建优化器节点
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)
# 构建计算准确率节点
correct = tf.nn.in_top_k(logits, y, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
# 构建全局初始化节点
init = tf.global_variables_initializer()
# 获取数据
mnist = input_data.read_data_sets("/tmp/data/")
X_test = mnist.test.images.reshape((-1, n_steps, n_inputs))
y_test = mnist.test.labels
# 开始执行阶段
n_epochs = 100
batch_size = 150
with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for iteration in range(mnist.train.num_examples // batch_size):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            X_batch = X_batch.reshape((-1, n_steps, n_inputs))
            sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
        acc_train = accuracy.eval(feed_dict={X:X_batch, y:y_batch})
        acc_test = accuracy.eval(feed_dict={X:X_test, y:y_test})
        print(epoch, "Train accuracy: ", acc_train, "\tTest accuracy: ", acc_test)
