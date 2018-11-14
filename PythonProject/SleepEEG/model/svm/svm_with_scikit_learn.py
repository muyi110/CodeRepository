#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys
sys.path.append("../../") # 将其他模块路径添加到系统搜索路径
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score
from data_processing import data_processing

PATH = "../../dataset/"
labels_dict = {"0":"awake", "1":"light_sleep", "2":"deep_sleep"}

class Linear_SVM():
    def __init__(self, c=1.0):
        self.c = c
        self.scaler = StandardScaler()

    def _data_scaler(self, X):
        X_scaled = self.scaler.fit_transform(X.astype(np.float32))
        return X_scaled

    def fit(self, X, y, random_state=42):
        # X_scaled = self._data_scaler(X)
        lin_clf = LinearSVC(C = self.c, random_state=random_state)
        lin_clf.fit(X, y)
        # lin_clf.fit(X_scaled, y)

        self._lin_clf = lin_clf
    def score(self, X, y):
        # X_scaled = self._data_scaler(X)
        y_pred = self._lin_clf.predict(X)
        # y_pred = self._lin_clf.predict(X_scaled)
        return accuracy_score(y, y_pred)

class SVM():
    def __init__(self, gamma="auto", decision_function_shape="ovr", c=1.0,  kernel="rbf"):
        self.c = c
        self.scaler = StandardScaler()
        self.decision_function_shape = decision_function_shape
        self.kernel = kernel
        self.gamma = gamma

    def _data_scaler(self, X):
        X_scaled = self.scaler.fit_transform(X.astype(np.float32))
        return X_scaled

    def fit(self, X, y, random_state=42):
        # X_scaled = self._data_scaler(X)
        svm_clf = SVC(decision_function_shape=self.decision_function_shape, gamma=self.gamma, 
                      C=self.c, kernel=self.kernel, random_state=random_state)
        svm_clf.fit(X, y)
        # svm_clf.fit(X_scaled, y)

        self._svm_clf = svm_clf
    def score(self, X, y):
        # X_scaled = self._data_scaler(X)
        y_pred = self._svm_clf.predict(X)
        # y_pred = self._svm_clf.predict(X_scaled)
        return accuracy_score(y, y_pred)



if __name__ == "__main__":
    train_x, train_y, test_x, test_y = data_processing.getsample(path = PATH, time_interval=10, train_proportion=0.7, filter_flag=False, plot_flag=False)
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
    print("-"*50)
    plt.show()

    # 构造线性 SVM
    linear_svm = Linear_SVM(c=1)
    linear_svm.fit(train_x, train_y)
    print("linear svm---train accaracy: {:.2f}%.".format(linear_svm.score(train_x, train_y)*100))
    print("linear svm---test accaracy: {:.2f}%.".format(linear_svm.score(test_x, test_y)*100))
    print("-"*50)
    # 构造 SVM 核函数是 RBF
    svm = SVM(c=1, decision_function_shape="ovr", kernel="rbf", gamma=100)
    svm.fit(train_x, train_y)
    print("svm with kernel---train accaracy: {:.2f}%.".format(svm.score(train_x, train_y)*100))
    print("svm with kernel---test accaracy: {:.2f}%.".format(svm.score(test_x, test_y)*100))
    print("-"*50)
