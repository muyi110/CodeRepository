#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys
sys.path.append("../../") # 将其他模块路径添加到系统搜索路径
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from data_processing import data_processing

PATH = "../../dataset/"
labels_dict = {"0":"awake", "1":"light_sleep", "2":"deep_sleep"}

def label_to_string(label_nums):
    assert len(label_nums.shape) == 1
    result = []
    for i in label_nums:
        result.append(labels_dict[str(i)])
    return result

if __name__ == "__main__":
    train_x, train_y, test_x, test_y = data_processing.getsample(path = PATH, time_interval=10, plot_flag=False, 
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
    # 训练模型
    softmax_reg = LogisticRegression(multi_class = "multinomial", 
                                     solver="lbfgs", C=1000)
    softmax_reg.fit(train_x, train_y)
    score_train = softmax_reg.score(train_x, train_y)
    score = softmax_reg.score(test_x, test_y)
    print("train accuracy: {}%.".format(score_train*100))
    print("test accuracy: {}%.".format(score*100))
    print(label_to_string(softmax_reg.predict(np.array([[0.2,0.2,0.2,0.3]]))))
    print("test predict: \n", softmax_reg.predict(test_x))
    print("test true label: \n", test_y)
    print(test_x[(test_y != softmax_reg.predict(test_x))])
