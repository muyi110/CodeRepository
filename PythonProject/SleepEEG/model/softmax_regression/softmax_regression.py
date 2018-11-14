#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys
sys.path.append("../../") # 将其他模块路径添加到系统搜索路径
import math
import numpy as np
import matplotlib.pyplot as plt
from data_processing import data_processing

PATH = "../../dataset/"
labels_dict = {"0":"awake", "1":"light_sleep", "2":"deep_sleep"}

def to_one_hot(y):
    n_classes = y.max() + 1
    m = len(y)
    Y_one_hot = np.zeros((m, n_classes))
    Y_one_hot[np.arange(m), y] = 1
    return Y_one_hot

def random_mini_batches(X, Y, mini_batch_size = 32, seed = 0):   
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size)
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches

def label_to_string(label_nums):
    assert len(label_nums.shape) == 1
    result = []
    for i in label_nums:
        result.append(labels_dict[str(i)])
    return result

class SoftMax():
    def __init__(self, learning_rate=0.001, batch_size=32, regularization_l2=False, random_seed=42):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.regularization_l2 = regularization_l2
        self.random_seed = random_seed

    def _softmax(self, logits):
        exps = np.exp(logits)
        exp_sum = np.sum(exps, axis=1, keepdims=True)
        return exps / exp_sum

    def fit(self, train_x, train_y, n_epochs=2001):
        n_inputs = train_x.shape[1]
        n_outputs = len(np.unique(np.argmax(train_y, axis=1)))
        epsilon = 1e-7
        theta = np.random.randn(n_inputs, n_outputs) # 学习的参数
        # 开始训练
        seed = 0
        for epoch in range(n_epochs):
            seed += 1
            mini_batches = random_mini_batches(train_x, train_y, mini_batch_size = self.batch_size, seed = seed)
            for mini_batch in mini_batches:
                train_batch_x, train_batch_y = mini_batch
                logits = train_batch_x.dot(theta)
                Y_proba = self._softmax(logits)
                loss = -np.mean(np.sum(train_batch_y * np.log(Y_proba + epsilon), axis=1))
                error = Y_proba - train_batch_y
                gradients = 1 / (train_batch_x.shape[0]) * train_batch_x.T.dot(error)
                theta = theta - self.learning_rate*gradients
            if epoch % 500 == 0:
                logits_train_set = train_x.dot(theta)
                Y_proba_train_set = self._softmax(logits_train_set)
                loss_train_set = -np.mean(np.sum(train_y * np.log(Y_proba_train_set + epsilon), axis=1))
                # 计算准确率
                train_accuracy = np.mean(np.argmax(Y_proba_train_set, axis=1) == np.argmax(train_y, axis=1))
                print(epoch, "\ttrain set loss: ", loss_train_set, "\ttrain accuracy: {}%".format(train_accuracy*100))
        self._theta = theta

    def sorce(self, X, Y):
        logits = X.dot(self._theta)
        y_proba = self._softmax(logits)
        accuracy = np.mean(np.argmax(y_proba, axis=1) == np.argmax(Y, axis=1))
        return accuracy

    def predict(self, X):
        logits = X.dot(self._theta)
        proba = self._softmax(logits)
        label_num = np.argmax(proba, axis=1)
        return label_num


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
    plt.show()
    # one-hot 编码
    Y_train_one_hot = to_one_hot(train_y)
    Y_test_one_hot = to_one_hot(test_y)
    X_train = np.c_[np.ones([len(train_x), 1]), train_x] # 添加偏置
    X_test = np.c_[np.ones([len(test_x), 1]), test_x]

    eta = 0.01
    n_epoches = 20001
    batch_size = 32
    regularization_l2 = False
    softmax = SoftMax(learning_rate=eta, batch_size=batch_size, regularization_l2=regularization_l2)
    softmax.fit(X_train, Y_train_one_hot, n_epochs=n_epoches)
    sorce = softmax.sorce(X_test, Y_test_one_hot)
    print("test accuracy : {}%.".format(sorce * 100))
