#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from pandas.tools.plotting import andrews_curves
from pandas.plotting import andrews_curves
import pandas as pd
import data_processing

PATH = "../dataset/"
def global_visual(X, label):
    '''
    全局可视化，最高适合 5 维度数据（x, y, z, size, color)
    X shape = (number of samples, features)
    label shape = (number of samples)---->label
    这里的 lable 用颜色代替
    '''
    x = X[:,0]  # delta
    y = X[:,1]  # theta
    z = X[:,3]  # beta
    size = X[:,2]*500 # alpha
    # 开始颜色映射 (0-->red, 1-->blue, 2-->yellow)
    # 0: awake; 1: light sleep; 2: deep sleep
    x_awake = x[label==0]
    x_light = x[label==1]
    x_deep = x[label==2]
    y_awake = y[label==0]
    y_light = y[label==1]
    y_deep = y[label==2]
    z_awake = z[label==0]
    z_light = z[label==1]
    z_deep = z[label==2]
    size_awake = size[label==0]
    size_light = size[label==1]
    size_deep = size[label==2]
    fig = plt.figure(1)
    ax = Axes3D(fig)
    ax.scatter(x_awake, y_awake, z_awake, s=size_awake, c="r", marker="*", alpha=0.9, label="awake")
    ax.scatter(x_light, y_light, z_light, s=size_light, c="b", marker="*", alpha=0.9, label="light sleep")
    ax.scatter(x_deep, y_deep, z_deep, s=size_deep, c="y", marker="*", alpha=0.9, label="deep sleep")
    ax.set_xlabel("delta")
    ax.set_ylabel("theat")
    ax.set_zlabel("beta")
    ax.legend()

def visual_2D(X, label):
    """
    两两特征组合可视化
    """
    X_awake = X[label==0]
    X_light = X[label==1]
    X_deep = X[label==2]
    features_name = {"0":"delta", "1":"theta", "2":"alpha", "3":"beta"}
    m = X.shape[1] * (X.shape[1]-1) // 2 # 两两特征组合的个数
    cols = 2 
    rows = m // cols + 1
    number = 1
    plt.figure(2)
    for i in range(0, X.shape[1]):
        for j in range(i+1, X.shape[1]):
            plt.subplot(rows, cols, number)
            plt.scatter(X_awake[:, i], X_awake[:, j], c="r", label="awake")
            plt.scatter(X_light[:, i], X_light[:, j], c="b", label="light")
            plt.scatter(X_deep[:, i], X_deep[:, j], c="y", label="deep")
            plt.grid()
            plt.legend()
            plt.xlabel(features_name[str(i)])
            plt.ylabel(features_name[str(j)])
            number += 1

def andrews_plot(X, label):
    plt.figure(3)
    label = label.reshape(-1, 1)
    data = np.c_[label, X]
    data = pd.DataFrame(data)
    print(data.head(20))
    andrews_curves(data, 0)

if __name__ == "__main__":
    train_x, train_y, test_x, test_y = data_processing.getsample(path = PATH, time_interval=10, 
                                                                 train_proportion=0.7, plot_flag=False)
    # sample shape = (number of samples, features)
    train_x = np.array(train_x).mean(axis=2)
    train_y = np.array(train_y)
    test_x = np.array(test_x).mean(axis=2)
    test_y = np.array(test_y)
    X = np.r_[train_x, test_x]
    y = np.c_[train_y.reshape(1,-1), test_y.reshape(1,-1)].reshape(-1)
    assert X.shape[0] == y.shape[0]
    print("number of samples is: ", X.shape[0])

    global_visual(X, y)
    visual_2D(X, y)
    plt.tight_layout()
    andrews_plot(X, y)
    plt.show()
