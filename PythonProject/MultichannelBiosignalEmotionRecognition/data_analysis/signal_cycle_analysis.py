#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
from envelope_analysis import data_filter, get_envelope

SAMPLE_PATH = "./samples/"

def get_sample_data(path=SAMPLE_PATH, people_num=0, trial_num=1):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    data = np.loadtxt(file_path[people_num] + "/trial_" + str(trial_num) + ".csv", delimiter=",", skiprows=0)
    eeg_data = data[:32,128*3:]
    return eeg_data

def _corrcoef(X, Y):
    corr = np.corrcoef(X, Y)
    return(corr[0,1])

def _eeg_corrcoef(data, time_length=1):
    corr_list = []
    for sigle_channel_eeg in data:
        X = sigle_channel_eeg[:128*time_length]
        Y = sigle_channel_eeg[128*time_length:128*time_length*2]
        corr = _corrcoef(X, Y)
        corr_list.append(corr)
    assert len(corr_list) == 32
    return np.array(corr_list).reshape(1, -1)

def eeg_corrcoef_diff_times(data):
    # 分别计算 1-30s 时间间隔的 32 通道相关系数
    result = _eeg_corrcoef(data, time_length=1)
    for time in range(2, 31):
        result = np.r_[result, _eeg_corrcoef(data, time)]
    return result

def autocorr(X):
    n = len(X)
    var = X.var()
    X = X-X.mean()
    result = np.correlate(X, X, mode="full")
    return result[result.size//2:]/(n*var)

def auto_function_plot(data):
    x = np.linspace(0, len(data)//128, len(data))
    y = data
    plt.plot(x, y)
    plt.grid()

if __name__ == "__main__":
    eeg = get_sample_data(people_num=6, trial_num=1)
    np.set_printoptions(precision=3, suppress=True)
    # print("shape: \n", eeg_corrcoef_diff_times(eeg).shape)
    # print("corr: \n", eeg_corrcoef_diff_times(eeg))
    data = autocorr(eeg[0][128*10:128*20])
    auto_function_plot(data)
    # x = eeg[0][:128*10]
    # envelope_max, _ = get_envelope(x, np.arange(len(x)))
    # data = autocorr(envelope_max)
    # auto_function_plot(data)
    plt.show()
