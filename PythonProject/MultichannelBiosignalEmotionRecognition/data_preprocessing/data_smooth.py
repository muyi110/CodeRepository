#! /usr/bin/env python3
# -*- coding=UTF-8 -*-
################################################################################
# 对数据或特征的平滑处理
# 滑动平均法和线性动态系统（LDA）
################################################################################
import os
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_PATH = "../data_analysis/samples/"

def get_sample_data(path=SAMPLE_PATH, people_num=0, trial_num=1):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    data = np.loadtxt(file_path[people_num] + "/trial_" + str(trial_num) + ".csv", delimiter=",", skiprows=0)
    eeg_data = data[:32,128*3:]
    return eeg_data

