#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import numpy as np
import tensorflow as tf
import time
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from tcn import TCN

# 构建 TCN 模型类，为了兼容 scikit-learning 的 RandomizedSearchCV 类，后续可能实现超参数搜索
class TCNClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, num_channels, 
                 sequence_length, 
                 kernel_size, 
                 dropout, 
                 batch_size=16, 
                 in_channels=1, 
                 random_state=None, 
                 learning_rate=0.001, 
                 optimizer_class=tf.train.AdamOptimizer):
        self.num_channels = num_channels
        self.sequence_length = sequence_length
        self.kernel_size = kernel_size
        self.dropout = dropout
        self.batch_size = batch_size
        self.random_state = random_state
        self.in_channels = in_channels
        self.learning_rate = learning_rate
        self.optimizer_class = optimizer_class
        self._session = None
    def _TCN(self, inputs, n_outputs):
        '''构建 TCN 模型'''
        outputs = TCN(inputs, n_outputs, self.num_channels, 
                      self.sequence_length, self.kernel_size, self.dropout)
        return outputs
    def _bulid_graph(self, n_outputs):
        '''构建计算图'''
        if self.random_state is not None:
            tf.set_random_seed(self.random_state)
            np.random.seed(self.random_state)
        inputs = tf.placeholder(tf.float32, 
                                shape=(self.batch_size, self.sequence_length, self.in_channels), name="inputs")
        labels = tf.placeholder(tf.int32, shape=(None), name="labels")
        #self._training = tf.placeholder_with_default(True, shape=(), name="training")
        tcn_outputs = self._TCN(inputs, n_outputs)
        predictions = tf.softmax(tcn_outputs, name="predictions")
        # 计算交叉熵
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=tcn_outputs)
        loss = tf.reduce_mean(xentropy, name="loss")
        # 构建优化器节点
        optimizer = self.optimizer_class(learning_rate=self.learning_rate)
        training_op = optimizer.minimize(loss)
        # 构建计算准确率节点
        correct = tf.nn.in_top_k(tcn_outputs, labels, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
        # 构建全局初始化节点和模型保存节点
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

        self._X, self._y = inputs, labels
        self._predictions, self._loss = predictions, loss
        self._training_op, self._accuracy = training_op, accuracy
        self._init, self._saver = init, saver
    def close_session(self):
        if self._session:
            self._session.close()
    def _get_model_params(self):
        '''获取所有变量值，用于 early stopping ,faster than saving to disk'''
        with self._graph.as_default():
            gvars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)# 获取一个 list 包含所有的变量
        return {gvar.op.name: value for gvar, value in zip(gvars, self._session.run(gvars))}
    def _restore_model_params(self, model_params):
        gvar_names = list(model_params.keys())
        # 获取被给名字的操作(op)
        assign_ops = {gvar_name: self._graph.get_operation_by_name(gvar_name + "/Assign") for gvar_name in gvar_names}
        # inputs 是tf.Operation 的属性. The list of Tensor objects representing the data inputs of this op
        init_values = {gvar_name: assign_op.inputs[1] for gvar_name, assign_op in assign_ops.items()}
        # 由于 key 是 tensor ，所以 value 会替换为 key 对应的 tensor. 具体参考官网 tf.Session.run
        feed_dict = {init_values[gvar_name]: model_params[gvar_name] for gvar_name in gvar_names}
        self._session.run(assign_ops, feed_dict=feed_dict)
    def fit(self, X, y, n_epochs, X_valid=None, y_valid=None):
        '''Fit the model to the training set. If X_valid and y_valid are provided, use early stopping'''
        self.close_session()
        self.classes_ = np.unique(y)
        n_outputs = len(self.classes_) # 获取输出的类别数
        self._graph = tf.Graph()
        with self._graph.as_default():
            self._bulid_graph(n_outputs) # 构建计算模型
        # 下面几个变量用于 early stopping
        max_check_without_progress = 20
        checks_without_progress = 0
        best_loss = np.infty
        best_params = None
        # 开始训练阶段
        self._session = tf.Session(graph=self._graph)
        with self._session.as_default() as sess:
            sess.run(self._init)
            for epoch in range(n_epochs):
                pass
                # 下面用于 early stopping
                if V_valid is not None and y_valid is not None:
                    loss_val, acc_val = sess.run([self._loss, self._accuracy], 
                                                 feed_dict={self._X:X_valid, self._y:y_valid})
                    if loss_val < best_loss:
                        best_loss = loss_val
                        best_params = self._get_model_params()
                        checks_without_progress = 0
                    else:
                        checks_without_progress += 1
                    print("{}\tValidation loss: {.6f}\tBest loss: {:.6f}\tAccuracy: {:.2f}%".format(epoch, 
                          loss_val, best_loss, acc_val*100))
                    if checks_without_progress >= max_check_without_progress:
                        print("Early stopping!")
                else:
                    loss_train, acc_train = sess.run([self._loss, self._accuracy], 
                                                     feed_dict={self._X:X_batch, self._y:y_batch})
                    print("{}\tLast training batch loss: {:.6f}\tAccuracy: {:.2f}%".format(epoch, 
                          loss_train, acc_train*100))
            if best_params:
                self._restore_model_params(best_params)
            return self
    def predict_proba(self, X):
        if not self._session:
            raise NotFittedError("This %s instance is not fitted yet" % self.__class__.__name__)
        with self._session.as_default() as sess:
            return self._predictions.eval(feed_dict={self._X: X})
    def predict(self, X):
        class_indices = np.argmax(self.predict_proba(X), axis=1)
        return np.array([[self.classes_[class_index]] for class_index in class_indices], np.int32)
    def save(self, path):
        self._saver.save(self._session, path)
