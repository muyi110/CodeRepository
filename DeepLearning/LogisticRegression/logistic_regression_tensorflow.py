#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

import os
from datetime import datetime
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import precision_score, recall_score

def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(42)

m = 1000
X_moons, y_moons = make_moons(m, noise=0.1, random_state=42)

# 可视化数据集
#plt.plot(X_moons[y_moons == 1, 0], X_moons[y_moons == 1, 1], "go", label="Positive")
#plt.plot(X_moons[y_moons == 0, 0], X_moons[y_moons == 0, 1], "r^", label="Negative")
#plt.legend()
#plt.show()
# 对每个实例添加额外的 bias (x_0 = 1) 
X_moons_with_bias = np.c_[np.ones((m, 1)), X_moons]
y_moons_column_vector = y_moons.reshape(-1,1)
# 将数据集划分为训练集和测试集
test_ratio = 0.2
test_size = int(m * test_ratio)
X_train = X_moons_with_bias[:-test_size]
X_test = X_moons_with_bias[-test_size:]
y_train = y_moons_column_vector[:-test_size]
y_test = y_moons_column_vector[-test_size:]
# 获取 mini-batch 数据（此方法具有随机性，可能不能覆盖全部的数据集）
def random_batch(X_train, y_train, batch_size):
    rnd_indices = np.random.randint(0, len(X_train), batch_size)
    X_batch = X_train[rnd_indices]
    y_batch = y_train[rnd_indices]
    return X_batch, y_batch

reset_graph()
n_inputs = 2
X = tf.placeholder(tf.float32, shape=(None, n_inputs+1), name="X")
y = tf.placeholder(tf.float32, shape=(None, 1), name="y")
theta = tf.Variable(tf.random_uniform([n_inputs+1, 1], -1.0, 1.0, seed=42), name="theta")# 参数
logits = tf.matmul(X, theta, name="logits")
y_proba = 1 / (1 + tf.exp(-logits))
#y_proba = tf.sigmoid(logits)
epsilon = 1e-7 # 当计算 log 时避免溢出
loss = -tf.reduce_mean(y * tf.log(y_proba + epsilon) + (1 - y) * tf.log(1 - y_proba + epsilon))
#loss = tf.losses.log_loss(y, y_proba)
learning_rate = 0.01
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)
init = tf.global_variables_initializer()

# 开始执行阶段
n_epochs = 1000
batch_size = 50
n_batches = int(np.ceil(m / batch_size)) # np.ceil() 向上取整，例如 np.ceil(2.1) = 3.0
with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for batch_index in range(n_batches):
            X_batch, y_batch = random_batch(X_train, y_train, batch_size)
            sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
        loss_val = loss.eval(feed_dict={X:X_test, y:y_test})
        if epoch % 100 == 0:
            print("Epoch: ", epoch, "\tLoss: ", loss_val)
    y_proba_val = y_proba.eval(feed_dict={X:X_test, y:y_test})
    y_pred = (y_proba_val >= 0.5)
    print("precision score: ", precision_score(y_test, y_pred))
    print("recall score: ", recall_score(y_test, y_pred))

# 下面开始实现结果更好的方法
# 添加4个特征
X_train_enhanced = np.c_[X_train, np.square(X_train[:,1]), 
                         np.square(X_train[:, 2]), X_train[:,1] ** 3, 
                         X_train[:,2] ** 3]
X_test_enhanced = np.c_[X_test, np.square(X_test[:,1]), 
                         np.square(X_test[:, 2]), X_test[:,1] ** 3, 
                         X_test[:,2] ** 3]
reset_graph()
def logistic_regression(X, y, initializer=None, seed=42, learning_rate=0.01):
    n_inputs_including_bias = int(X.get_shape()[1])# 获取输入的特征数
    with tf.name_scope("logistic_regression"):
        with tf.name_scope("model"):
            if initializer == None:
                initializer = tf.random_uniform([n_inputs_including_bias, 1], -1.0, 1.0, seed = seed)
            theta = tf.Variable(initializer, name = "theta")
            logits = tf.matmul(X, theta, name="logits")
            y_proba = tf.sigmoid(logits)
        with tf.name_scope("train"):
            loss = tf.losses.log_loss(y, y_proba, scope="loss")
            optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
            training_op = optimizer.minimize(loss)
            loss_summary = tf.summary.scalar("log_loss", loss)
        with tf.name_scope("init"):
            init = tf.global_variables_initializer()
        with tf.name_scope("save"):
            saver = tf.train.Saver()
        return y_proba, loss, training_op, loss_summary, init, saver

def log_dir(prefix=""):
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    root_logdir = "tf_logs"
    if prefix:
        prefix += "-"
    name = prefix + "run-"+now
    return "{}/{}/".format(root_logdir, name)

n_inputs = 2 + 4
X = tf.placeholder(tf.float32, shape=(None, n_inputs+1), name="X")
y = tf.placeholder(tf.float32, shape=(None, 1), name="y")
logdir = log_dir("logreg")
y_proba, loss, training_op, loss_summary, init, saver = logistic_regression(X, y)
file_writer = tf.summary.FileWriter(logdir, tf.get_default_graph())

n_epochs = 10001
batch_size = 50
n_batches = int(np.ceil(m / batch_size))
checkpoint_path = "./temp/my_logreg_model.ckpt"
checkpoint_epoch_path = checkpoint_path + ".epoch"
final_model_path = "./my_logreg_model"
with tf.Session() as sess:
    if os.path.isfile(checkpoint_epoch_path):
        with open(checkpoint_epoch_path, "rb") as f:
            start_epoch = int(f.read())
        print("Training was interrupted. Continuing at epoch", start_epoch)
        saver.restore(sess, checkpoint_path)
    else:
        start_epoch = 0
        sess.run(init)
    for epoch in range(start_epoch, n_epochs):
        for batch_index in range(n_batches):
            X_batch, y_batch = random_batch(X_train_enhanced, y_train, batch_size)
            sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
        loss_val, summary_str = sess.run([loss, loss_summary], feed_dict={X:X_test_enhanced, y:y_test})
        file_writer.add_summary(summary_str, epoch)
        if epoch % 500 == 0:
            print("Epoch: ", epoch, "\tLoss: ", loss_val)
            saver.save(sess, checkpoint_path)
            with open(checkpoint_epoch_path, "wb") as f:
                f.write(b"%d" % (epoch + 1))
    saver.save(sess, final_model_path)
    y_proba_val = y_proba.eval(feed_dict={X:X_test_enhanced, y:y_test})
    os.remove(checkpoint_epoch_path)
    y_pred = (y_proba_val >= 0.5)
    print("precision score: ", precision_score(y_test, y_pred))
    print("recall score: ", recall_score(y_test, y_pred))
