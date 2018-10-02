#!/usr/bin/env python3
# -*- coding=UTF-8 -*-
import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers import fully_connected
import matplotlib.pyplot as plt

def rest_graph(seed=42):
    tf.set_random_seed(seed)
    np.random.seed(seed)
    tf.reset_default_graph()

rest_graph()
# 开始生成模拟的时间序列
t_min, t_max = 0, 30
resolution = 0.1
# 模拟生成时间序列函数
def time_series(t):
    return t * np.sin(t) / 3 + 2 * np.sin(t*5)
# 产生 batch 数据函数
def next_batch(batch_size, n_steps):
    # np.random.rand(a, b)-->产生 shape 为 (a, b) 的随机数(均匀分布 [0,1))
    t0 = np.random.rand(batch_size, 1) * (t_max - t_min - n_steps * resolution) # 获取实例的起始点
    Ts = t0 + np.arange(0, n_steps + 1) * resolution # TS.shape=(batch_size, n_steps+1)
    ys = time_series(Ts)
    return ys[:,:-1].reshape(-1, n_steps, 1), ys[:,1:].reshape(-1, n_steps, 1)
# 可视化生成的样本数据
# t = np.linspace(t_min, t_max, int((t_max-t_min)/resolution))
# n_steps = 20
# t_instance = np.linspace(12.2, 12.2+resolution*(n_steps+1), n_steps+1)
# plt.figure(figsize=(11,4))
# plt.subplot(121)
# plt.title("A time series (generated)", fontsize=14)
# plt.plot(t, time_series(t), label=r"$t . \sin(t) / 3 + 2 . \sin(5t)$")
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "b-", linewidth=3, label="A training instance")
# plt.legend(loc="lower left", fontsize=14)
# plt.axis([0, 30, -17, 13])
# plt.xlabel("Time")
# plt.ylabel("Value")
# plt.subplot(122)
# plt.title("A training instance", fontsize=14)
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "bo", markersize=10, label="instance")
# plt.plot(t_instance[1:], time_series(t_instance[1:]), "w*", markersize=10, label="target")
# plt.legend(loc="upper left")
# plt.xlabel("Time")
# plt.show()
# 开始构建 RNN 网络
n_steps = 20
n_inputs = 1
n_neurons = 100
n_outputs = 1

learning_rate = 0.001

X = tf.placeholder(tf.float32, shape=[None, n_steps, n_inputs], name="X")
y = tf.placeholder(tf.float32, shape=[None, n_steps, n_outputs], name="y")
# # 利用 OutputProjectionWrapper 包装器（每个时间步的输出都加一个 FC 层)----效率低
# cell = tf.contrib.rnn.OutputProjectionWrapper(cell=tf.contrib.rnn.BasicRNNCell(num_units=n_neurons, 
#                                               activation=tf.nn.relu), output_size=n_outputs)
# # RNN cell 的初始化方式为 he initializer
# with tf.variable_scope("rnn", initializer=tf.contrib.layers.variance_scaling_initializer()):
#     outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
# 高效率版
cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons, activation=tf.nn.relu)
with tf.variable_scope("rnn", initializer=tf.contrib.layers.variance_scaling_initializer()):
    rnn_outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
stacked_rnn_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])
stacked_outputs = fully_connected(stacked_rnn_outputs, n_outputs, activation_fn=None)
outputs = tf.reshape(stacked_outputs, [-1, n_steps, n_outputs])
# 构造 loss 函数节点
loss = tf.reduce_mean(tf.square(outputs-y))
# 构建优化器节点
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)
# 构建全局初始化节点
init = tf.global_variables_initializer()
# 开始执行阶段（训练）
t_instance = np.linspace(12.2, 12.2+resolution*(n_steps+1), n_steps+1) # 测试起始点
n_iterations = 1000
batch_size = 50
with tf.Session() as sess:
    init.run()
    for iteration in range(n_iterations):
        X_batch, y_batch = next_batch(batch_size, n_steps)
        sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
        if iteration % 100 == 0:
            mse = loss.eval(feed_dict={X:X_batch, y:y_batch})
            print(iteration, "\tMSE: ", mse)
    X_new = time_series(np.array(t_instance[:-1].reshape(-1, n_steps, n_inputs)))
    y_pred = sess.run(outputs, feed_dict={X:X_new})
# 预测可视化
plt.title("Testing the model", fontsize=14)
plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "bo", markersize=10, label="instance")
plt.plot(t_instance[1:], time_series(t_instance[1:]), "w*", markersize=10, label="target")
plt.plot(t_instance[1:], y_pred[0,:,0], "r.", markersize=5, label="prediction")
plt.legend(loc="upper left")
plt.xlabel("Time")
plt.show()
