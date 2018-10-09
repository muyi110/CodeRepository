#!/usr/bin/env python3
# -*- coding=UTF-8 -*-
import time
import tensorflow as tf
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from data import read_data, index_generator

# 构建 RNN 模型类，为了兼容 scikit-learning 的 RandomizedSearchCV 类，后续可能实现超参数搜索
class RNNClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, 
                 n_steps = 15,
                 n_inputs = 128, # 可以理解为输入的特征数
                 n_neurons = 120,# 每个 cell 包含的神经元个数
                 n_outputs = 4, # 4 分类
                 learning_rate = 0.001,
                 random_state = None, 
                 batch_size = 64,
                 dropout = 0.0,
                 optimizer_class = tf.train.AdamOptimizer):
        self.n_steps = n_steps
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        self.n_outputs = n_outputs
        self.learning_rate = learning_rate
        self.random_state = random_state
        self.batch_size = batch_size
        self.dropout = dropout
        self.optimizer_class = optimizer_class
        self._session = None
    def _rnn(self, inputs, multi_layer=False):
        lstm_cells_1 = tf.contrib.rnn.BasicLSTMCell(num_units=self.n_neurons) # 构建 LSTM cell
        if multi_layer:
            #lstm_cells_1 = tf.contrib.rnn.DropoutWrapper(lstm_cells_1, input_keep_prob=1-self.dropout)
            lstm_cells_2 = tf.contrib.rnn.BasicLSTMCell(num_units=100) # 构建第二层 LSTM cell
            #lstm_cells_2 = tf.contrib.rnn.DropoutWrapper(lstm_cells_2, input_keep_prob=1-self.dropout)
            lstm_cells_3 = tf.contrib.rnn.BasicLSTMCell(num_units=40) # 构建第三层 LSTM cell
            #lstm_cells_3 = tf.contrib.rnn.DropoutWrapper(lstm_cells_3, input_keep_prob=1-self.dropout)
            multi_cell_cell = tf.contrib.rnn.MultiRNNCell([lstm_cells_1, lstm_cells_2, lstm_cells_3])
        else:
            multi_cell_cell = lstm_cells_1
        outputs, states = tf.nn.dynamic_rnn(multi_cell_cell, inputs, dtype=tf.float32)
        return states
    def _bulid_graph(self, multi_cell_cell):
        if self.random_state is not None:
            tf.set_random_seed(self.random_state)
            np.random.seed(self.random_state)
        X = tf.placeholder(tf.float32, [None, self.n_steps, self.n_inputs])
        y = tf.placeholder(tf.int32, [None])
        is_training = tf.placeholder(tf.bool, shape=(), name="is_training")
        rnn_outputs = self._rnn(X, multi_cell_cell) # 获取 RNN 网络最后的输出状态
        if multi_cell_cell:
            top_layer_h_state = rnn_outputs[-1][1]  # 获取顶层的 RNN 输出状态(短期状态)
        else:
            top_layer_h_state = rnn_outputs[1]
        # 对 RNN 的输出应用 dropout
        top_layer_h_state = tf.contrib.layers.dropout(top_layer_h_state, 1-self.dropout, is_training=is_training)
        logits_mid = tf.layers.dense(top_layer_h_state, 20, 
                                 kernel_initializer=tf.contrib.layers.variance_scaling_initializer(), 
                                 activation=tf.nn.relu,
                                 name="logits_mid") # 全连接层默认是没有激活函数的
        out = tf.contrib.layers.dropout(logits_mid, 1-self.dropout, is_training=is_training) # 添加dropout层
        logits = tf.layers.dense(out, self.n_outputs, 
                                 kernel_initializer=tf.contrib.layers.variance_scaling_initializer(), 
                                 name="logits") # 全连接层默认是没有激活函数的
        Y_proba = tf.nn.softmax(logits, name="Y_proba")
        # 计算交叉熵
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
        loss = tf.reduce_mean(xentropy, name="loss")
        # 构建优化器节点
        optimizer = self.optimizer_class(learning_rate=self.learning_rate)
        training_op = optimizer.minimize(loss)
        # 构建计算准确率节点
        correct = tf.nn.in_top_k(logits, y, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
        # 构建全局初始化节点和模型保存节点
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

        self._X, self._y = X, y
        self._Y_proba, self._loss = Y_proba, loss
        self._training_op, self._accuracy = training_op, accuracy
        self._init, self._saver = init, saver
        self._is_training = is_training
    def close_session(self):
        if self._session:
            self._session.close()
    def fit(self, X, y, n_epochs=100, X_test=None, y_test=None, multi_cell_cell=False):
        self.close_session()
        
        self.classes_ = np.unique(y)
        self.class_to_index_ = {label: index for index, label in enumerate(self.classes_)}
        y = np.array([self.class_to_index_[label] for label in y], dtype=np.int32)
        self.y_test_classes_ = np.unique(y_test)
        self.y_test_class_to_index_ = {label: index for index, label in enumerate(self.y_test_classes_)}
        y_test = np.array([self.y_test_class_to_index_[label] for label in y_test], dtype=np.int32)

        self._graph = tf.Graph()
        with self._graph.as_default():
            self._bulid_graph(multi_cell_cell) # 构建模型
        # 开始训练阶段
        seed = 0
        self._session = tf.Session(graph=self._graph)
        with self._session.as_default() as sess:
            sess.run(self._init)
            for epoch in range(n_epochs):
                seed += 1
                start_time = time.time()
                for X_batch_index, y_batch_index in index_generator(len(y), self.batch_size, seed=seed):
                    X_batch = X[X_batch_index]
                    y_batch = y[y_batch_index]
                    sess.run(self._training_op, feed_dict={self._X: X_batch, self._y: y_batch, self._is_training:True})
                total_loss = 0 
                total_acc = 0
                if epoch % 10 == 0:
                    for i in range(len(y) // 8):
                        X_batch = X[i*8:(i+1)*8,:,:]
                        y_batch = y[i*8:(i+1)*8]
                        loss_train, acc_train = sess.run([self._loss, self._accuracy], 
                                                        feed_dict={self._X:X_batch, self._y:y_batch, self._is_training:False})
                        total_loss += loss_train
                        total_acc += acc_train
                        end_time = time.time()
                    print("{}\ttraining loss: {:.6f}\t|  training accuracy: {:.2f}% | time: {:.2f}s".format(epoch, 
                          total_loss/(len(y)//8), (total_acc / (len(y)//8))*100, end_time-start_time))
                if X_test is not None and y_test is not None and epoch % 20 == 0:
                    loss_test, acc_test = sess.run([self._loss, self._accuracy], 
                                                    feed_dict={self._X:X_test, self._y:y_test, self._is_training:False})
                    print("Test accuracy: {:.4f}%\t Test loss: {:.6f}".format(acc_test*100, loss_test))
            return self
    def predict_proba(self, X):
        if not self._session:
            raise NotFittedError("This %s instance is not fitted yet" % self.__class__.__name__)
        with self._session.as_default() as sess:
            return self._predictions.eval(feed_dict={self._X: X})
    def predict(self, X):
        class_indices = np.argmax(self.predict_proba(X), axis=1)
        return np.array([self.classes_[class_index] for class_index in class_indices], np.int32).reshape(-1)
    def save(self, path):
        self._saver.save(self._session, path)

if __name__ == "__main__":
    # 获取生理信号数据(训练集)
    # datas, labels = read_data(train=True, test=False, raw_data=False, seed=42)
    datas = np.load("./data_set/datas_train.npy")
    labels = np.load("./data_set/label_train.npy")
    print("train set number: ", len(labels))
    print(datas[0])
    # 数据处理，目前只用到 32 通道的 EEG 信号
    datas_eeg = np.array(datas) # datas_result 的 shape=(880, features, seq_length)
    datas_eeg = datas_eeg.transpose((0,2,1)) # 将 datas_result 的形状变为 shape=(880, seq_length, features)
    #datas_eeg = datas_eeg.reshape(datas_eeg.shape[0], -1, 1)
    labels = np.array(labels).reshape(-1)
    # datas = datas.clear() # 清空列表， 释放内存
    del datas
    print(datas_eeg.shape)

    # 获取生理信号数据（测试集）
    # datas_test, labels_test = read_data(train=False, test=True, raw_data=False, seed=42)
    datas_test = np.load("./data_set/datas_test.npy")
    labels_test = np.load("./data_set/label_test.npy")
    print("test set number: ", len(labels_test))
    print(datas_test[0])
    datas_test_eeg = np.array(datas_test) # shape=(400, features, seq_length)
    datas_test_eeg = datas_test_eeg.transpose((0,2,1)) # 将 shape 转为 shape=(400, seq_length, features)
    #datas_test_eeg = datas_test_eeg.reshape(datas_test_eeg.shape[0], -1, 1)
    y_test = np.array(labels_test).reshape(-1)
    #datas_test.clear()
    del datas_test
    print(datas_test_eeg.shape)
    rnn = RNNClassifier(random_state=30, learning_rate=1e-3, dropout=0.35)
    rnn.fit(X=datas_eeg, y=labels, n_epochs=500, X_test=datas_test_eeg, y_test=y_test, multi_cell_cell=False)
    rnn_1 = RNNClassifier(random_state=30, learning_rate=1e-3, dropout=0.5)
    rnn_1.fit(X=datas_eeg, y=labels, n_epochs=500, X_test=datas_test_eeg, y_test=y_test, multi_cell_cell=False)
    rnn_2 = RNNClassifier(random_state=30, learning_rate=1e-3, dropout=0.5)
    rnn_2.fit(X=datas_eeg, y=labels, n_epochs=500, X_test=datas_test_eeg, y_test=y_test, multi_cell_cell=True)
    rnn_3 = RNNClassifier(random_state=30, learning_rate=1e-3, dropout=0.6)
    rnn_3.fit(X=datas_eeg, y=labels, n_epochs=500, X_test=datas_test_eeg, y_test=y_test, multi_cell_cell=True)
