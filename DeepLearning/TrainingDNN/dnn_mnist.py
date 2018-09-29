#!/usr/bin/env python3
#! -*- coding:UTF-8 -*-
import tensorflow as tf
import numpy as np

def load_data(path="./mnist.npz"):
    f = np.load(path)
    X_train, y_train = f['x_train'], f['y_train']
    X_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (X_train, y_train), (X_test, y_test)
# 获取 mnist 数据 
(X_train, y_train), (X_test, y_test) = load_data()
X_train = X_train.astype(np.float32).reshape(-1, 28*28) / 255.0
X_test = X_test.astype(np.float32).reshape(-1, 28*28) / 255.0
y_train = y_train.astype(np.int32) # 将标签转为 int 类型
y_test = y_test.astype(np.int32)
X_valid, X_train = X_train[:5000], X_train[5000:]
y_valid, y_train = y_train[:5000], y_train[5000:]

def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)

# 创建 He initializer 节点，适用于 ReLU 及其变体激活函数
he_init = tf.contrib.layers.variance_scaling_initializer()
# 模块化编程，利用函数创建 5 层的 DNN 网络
def dnn(inputs, n_hidden_layers=5, n_neurons=100, name=None, activation=tf.nn.elu, initializer=he_init):
    with tf.variable_scope(name, default_name="dnn"):
        for layer in range(n_hidden_layers):
            inputs = tf.layers.dense(inputs, n_neurons, activation=activation, 
                                     kernel_initializer=initializer, name="hidden%d" % (layer+1))
        return inputs
n_inputs = 28*28 # mnist data
n_outputs = 5 # 数字 0-4 
reset_graph()
X = tf.placeholder(tf.float32, shape=(None, n_inputs), name='X')
y = tf.placeholder(tf.int32, shape=(None), name='y') # 标签
# 构建具有 5 个隐藏层的 DNN 并获取最后隐藏层的输出
dnn_outputs = dnn(X) 

# 输出层，tf.layers.dense 默认没有激活函数，输出是线性的
logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init, name="logits")
Y_proba = tf.nn.softmax(logits, name='Y_proba')

learning_rate = 0.01
# 计算交叉熵代价函数
xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
loss = tf.reduce_mean(xentropy, name="loss")
# 创建 Adam 优化器节点
optimizer = tf.train.AdamOptimizer(learning_rate)
training_op = optimizer.minimize(loss, name="training_op")
# 创建获取准确率节点
correct = tf.nn.in_top_k(logits, y, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
# 创建全局变量初始化节点及模型保存节点
init = tf.global_variables_initializer()
saver = tf.train.Saver()
# 划分数据集为训练集，验证集和测试集，其中验证集用于 early stopping
X_train1 = X_train[y_train < 5]
y_train1 = y_train[y_train < 5]
X_valid1 = X_valid[y_valid < 5]
y_valid1 = y_valid[y_valid < 5]
X_test1 = X_test[y_test < 5]
y_test1 = y_test[y_test < 5]
# 下面开始模型的执行阶段
n_epochs = 1000
batch_size = 20
max_checks_without_progress = 20 # 用于早停算法的最大步
checks_without_progress = 0
best_loss = np.infty
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(n_epochs):
        rnd_idx = np.random.permutation(len(X_train1))
        for rnd_indices in np.array_split(rnd_idx, len(X_train1) // batch_size):
            X_batch, y_batch = X_train1[rnd_indices], y_train1[rnd_indices]
            sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
        loss_val, acc_val = sess.run([loss, accuracy], feed_dict={X:X_valid1, y:y_valid1})
        if loss_val < best_loss:
            best_loss = loss_val
            save_path = saver.save(sess, "./trained_model/my_mnist_model_0_to_4.ckpt")
            checks_without_progress = 0
        else:
            checks_without_progress += 1
            if checks_without_progress >= max_checks_without_progress:
                print("Early stopping!")
                break
        print("{}\tValidation loss: {:.6f}\tBest loss: {:.6f}\tAccuracy: {:.2f}%".format(epoch, 
              loss_val, best_loss, acc_val*100))
with tf.Session() as sess:
    saver.restore(sess, "./trained_model/my_mnist_model_0_to_4.ckpt")
    acc_test = accuracy.eval(feed_dict={X:X_test1, y:y_test1})
    print("Final test accuracy: {:.2f}%".format(acc_test * 100))
