#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

DATA_PATH = "../dataset/"

def moving_average_filter(data, windows_length=7):
    data_result = np.zeros(data.shape)
    for elem in range(data_result.shape[0]-windows_length):
        data_result[elem] = (data[elem:windows_length+elem].copy()).mean()
    data_result[-10:] = data[-10:].copy()
    assert (data_result == 0).sum() == 0
    return data_result

def median_filter(data, windows_length=3):
    data_result = signal.medfilt(data, windows_length)
    assert (data_result.shape == data.shape)
    return data_result

def getsample(path=DATA_PATH, time_interval=10, train_proportion=0.7, 
              plot_flag=True, filter_flag=False):
    '''
    有三个类别，分别对应：
        清醒状态--> awake
        浅睡眠状态--> light sleep
        深度睡眠状态--> deep sleep
    '''
    sample_labels = {"awake":0, "light_sleep":1, "deep_sleep":2}
    awake_samples = []
    light_sleep_samples = []
    deep_sleep_samples = []
    awake_labels = []
    light_sleep_labels = []
    deep_sleep_labels = []
    # 获取样本数据的路径
    data_path = os.listdir(path) # 目录顺序是随机的
    data_file_path = [os.path.join(path, data_path[i]) + "/" for i in range(len(data_path))]
    # 8 种波段文件名字对应：delta.txt, theta.txt, lowalpha.txt, highalpha.txt, lowbeta.txt, highbeta.txt, 
    #                       lowgamma.txt, midgamma.txt 
    for file_path in data_file_path: 
        delta = np.loadtxt(file_path + "/delta.txt", skiprows=0, dtype=np.int32)[20:]
        theta = np.loadtxt(file_path + "/theta.txt", skiprows=0, dtype=np.int32)[20:]
        lowalpha = np.loadtxt(file_path + "/lowalpha.txt", skiprows=0, dtype=np.int32)[20:]
        highalpha = np.loadtxt(file_path + "/highalpha.txt", skiprows=0, dtype=np.int32)[20:]
        lowbeta = np.loadtxt(file_path + "/lowbeta.txt", skiprows=0, dtype=np.int32)[20:]
        highbeta = np.loadtxt(file_path + "/highbeta.txt", skiprows=0, dtype=np.int32)[20:]
        if filter_flag:
            # delta = moving_average_filter(delta)
            # theta = moving_average_filter(theta)
            # lowalpha = moving_average_filter(lowalpha)
            # highalpha = moving_average_filter(highalpha)
            # lowbeta = moving_average_filter(lowbeta)
            # highbeta = moving_average_filter(highbeta)
            delta = median_filter(delta)
            theta = median_filter(theta)
            lowalpha = median_filter(lowalpha)
            highalpha = median_filter(highalpha)
            lowbeta = median_filter(lowbeta)
            highbeta = median_filter(highbeta)
        # 求4个波段的能量占比
        sum_energy = delta + theta + lowalpha + highalpha + lowbeta + highbeta
        delta_proportion = delta / sum_energy
        theta_proportion = theta / sum_energy
        alpha_proportion = (lowalpha + highalpha) / sum_energy
        beta_proportion = (lowbeta + highbeta) / sum_energy
        # 获取三个类别对应的样本
        if file_path == (path+"1113_sleep_1/"):
            # 清醒样本
            awake_delta_proportion = delta_proportion[250:450]
            awake_theta_proportion = theta_proportion[250:450]
            awake_alpha_proportion = alpha_proportion[250:450]
            awake_beta_proportion = beta_proportion[250:450]
            for i in range(len(awake_delta_proportion)//time_interval):
                a = awake_delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = awake_theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = awake_alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = awake_beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                awake_samples.append(np.r_[a, b, c, d])
                awake_labels.append(sample_labels["awake"])
            # 浅睡眠样本
            light_delta_proportion = delta_proportion[700:900]
            light_theta_proportion = theta_proportion[700:900]
            light_alpha_proportion = alpha_proportion[700:900]
            light_beta_proportion = beta_proportion[700:900]
            for i in range(len(light_delta_proportion)//time_interval):
                a = light_delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = light_theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = light_alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = light_beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                light_sleep_samples.append(np.r_[a, b, c, d])
                light_sleep_labels.append(sample_labels["light_sleep"])
        if file_path == (path+"1105_sleep/"):
            # 浅睡眠样本
            light_delta_proportion = delta_proportion[:790]
            light_theta_proportion = theta_proportion[:790]
            light_alpha_proportion = alpha_proportion[:790]
            light_beta_proportion = beta_proportion[:790]
            for i in range(len(light_delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                light_sleep_samples.append(np.r_[a, b, c, d])
                light_sleep_labels.append(sample_labels["light_sleep"])
            # 深度睡眠样本
            deep_delta_proportion = delta_proportion[790:]
            deep_theta_proportion = theta_proportion[790:]
            deep_alpha_proportion = alpha_proportion[790:]
            deep_beta_proportion = beta_proportion[790:]
            for i in range(len(deep_delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                deep_sleep_samples.append(np.r_[a, b, c, d])
                deep_sleep_labels.append(sample_labels["deep_sleep"])
        if file_path == (path+"1108_normal/"):
            # 清醒状态样本
            for i in range(len(delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                awake_samples.append(np.r_[a, b, c, d])
                awake_labels.append(sample_labels["awake"])
        if file_path == (path+"1112_sleep/"):
            # 浅睡眠样本
            light_delta_proportion = delta_proportion[640:1220]
            light_theta_proportion = theta_proportion[640:1220]
            light_alpha_proportion = alpha_proportion[640:1220]
            light_beta_proportion = beta_proportion[640:1220]
            for i in range(len(light_delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                light_sleep_samples.append(np.r_[a, b, c, d])
                light_sleep_labels.append(sample_labels["light_sleep"])
            # 深度睡眠样本
            deep_delta_proportion = delta_proportion[550:640]
            deep_theta_proportion = theta_proportion[550:640]
            deep_alpha_proportion = alpha_proportion[550:640]
            deep_beta_proportion = beta_proportion[550:640]
            for i in range(len(deep_delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                deep_sleep_samples.append(np.r_[a, b, c, d])
                deep_sleep_labels.append(sample_labels["deep_sleep"])
        if file_path == (path+"1112_normal/"):
            # 清醒状态样本
            for i in range(len(delta_proportion)//time_interval):
                a = delta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                b = theta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                c = alpha_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                d = beta_proportion[time_interval*i:time_interval*(i+1)].reshape(1,-1)
                awake_samples.append(np.r_[a, b, c, d])
                awake_labels.append(sample_labels["awake"])
        
        samples_x = awake_samples + light_sleep_samples + deep_sleep_samples
        labels_y = awake_labels + light_sleep_labels + deep_sleep_labels
        train_number = int(len(samples_x) * train_proportion)
        test_number = len(samples_x) - train_number
        np.random.seed(42)
        permutation = np.random.permutation(len(samples_x))
        train_x = []
        train_y = []
        test_x = []
        test_y = []
        for i in permutation[:train_number]:
            train_x.append(samples_x[i])
            train_y.append(labels_y[i])
        for i in permutation[-test_number:]:
            test_x.append(samples_x[i])
            test_y.append(labels_y[i])
        
        if plot_flag:
            # 画图
            plt.figure(file_path)
            plt.plot(delta_proportion, label="delta")
            plt.plot(theta_proportion, label="theta")
            plt.plot(alpha_proportion, label="alpha")
            plt.plot(beta_proportion, label="beta")
            plt.legend()
            plt.grid()

    return train_x, train_y, test_x, test_y

if __name__ == "__main__":
    train_x, train_y, test_x, test_y = getsample(filter_flag=True)
    assert len(train_x) == len(train_y)
    assert len(test_x) == len(test_y)
    print("train number: ", len(train_y))
    print("train sample shape: ", train_x[0].shape)
    print(train_y[0])
    print("test number: ", len(test_y))
    print("test sample shape: ", test_x[0].shape)
    print(test_y[0])
    plt.show()
