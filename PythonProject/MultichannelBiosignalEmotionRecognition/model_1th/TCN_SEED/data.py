# -*- coding:UTF-8 -*-
import os
import re
import math
import numpy as np
import scipy.io as scio
import scipy.signal as signal
from features import differential_entropy

SAMPLES_PATH = "/media/ylq/024EF3F44EF3DE7B/SEED_DataSet/Preprocessed_EEG"
def get_samples_data(path, windows=4, overlapping=3):
    '''
      windows: 划分的时间窗口长度
      overlapping: 时间窗口的重叠长度
    '''
    samples_dirs = os.listdir(path) # 目录的顺序是随机的, 每一个元素是字符串
    # 移除 目录中的 label.mat 和 readme.txt
    samples_dirs.remove("label.mat")
    samples_dirs.remove("readme.txt")
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    datas = [] 
    labels = []
    label_ = scio.loadmat(path+"/label.mat")["label"]
    for people in range(1): # 15个人，每个人参加 3 次实验
        data = scio.loadmat(file_path[people]) # 得到一个字典
        # 删除无关信息，保留 15 个 trial 的 eeg 信号 
        del data["__version__"]
        del data["__header__"]
        del data["__globals__"]
        for key in data:
            data_eeg = data[key][:, :-1] # shape = (62, data)
            number = re.findall("\d+", key)[0] # number 是 str
            number = int(number)
            # 获取对应的 trial 的 label
            label = label_[0][number - 1]
            step = windows - overlapping # 每次移动的步长
            iterator_num = int((data_eeg.shape[1]/200 - windows) / step  + 1) # 划分时间片段总个数
            for iterator in range(iterator_num):
                data_slice = data_eeg[:,200*(iterator*step):200*(iterator*step+windows)]
                datas.append(data_slice)
                labels.append(label)
    print("Get sample data success!")
    print("Total sample number is: ", len(labels))
    print("label -1: {}  label 0: {}  label 1: {}.".format(np.sum(np.array(labels)==-1), 
                                                                  np.sum(np.array(labels)==0), 
                                                                  np.sum(np.array(labels)==1))) 
    return (datas, labels)

def index_generator(num_examples, batch_size, seed=0):
    '''此函数用于生成 batch 的索引'''
    np.random.seed(seed)
    permutation = list(np.random.permutation(num_examples))
    num_complete_minibatches = math.floor(num_examples/batch_size)
    for k in range(0, num_complete_minibatches):
        X_batch_index = permutation[k*batch_size:(k+1)*batch_size]
        y_batch_index = permutation[k*batch_size:(k+1)*batch_size]
        yield (X_batch_index, y_batch_index)
    if num_examples % batch_size != 0:
        X_batch_index = permutation[num_complete_minibatches*batch_size:num_examples]
        y_batch_index = permutation[num_complete_minibatches*batch_size:num_examples]
        yield (X_batch_index, y_batch_index)

def read_data(path=SAMPLES_PATH, windows=4, overlapping=3):
    datas, labels = get_samples_data(path, windows, overlapping)
    data_result = []
    for data in datas:
        data_list = []
        for window in range(windows):
            features_list = []
            for i in range(62):
                X = data[i, 200*window:200*(window+1)]
                X = X * signal.get_window('hann', 200)
                fft = np.fft.rfft(X, 256)
                features_list.append(differential_entropy(fft, 1, 3))
                features_list.append(differential_entropy(fft, 4, 7))
                features_list.append(differential_entropy(fft, 8, 13))
                features_list.append(differential_entropy(fft, 14, 30))
                features_list.append(differential_entropy(fft, 31, 50))
            data_list.append((np.array(features_list).reshape(-1, 1)))
        data_result.append(np.c_[tuple(data_list)])
    return (data_result, labels)
