#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_PATH = 'samples/'

def get_samples_labels(path):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    labels = (np.loadtxt(file_path[i]+'/label.csv', delimiter=',', skiprows=0) for i in range(len(file_path)))
    valence_list = []
    arousal_list = []
    for label in labels:
        valence_list += list(label[:, 0]-5) #-5:中心化
        arousal_list += list(label[:, 1]-5) #-5:中心化

    return valence_list, arousal_list

def labels_plot(x, y):
    arousal = x
    valence = y
    plt.scatter(arousal, valence)
    plt.xlim([-4.5, 4.5])
    plt.ylim([-4.5, 4.5])
    plt.plot((-4.5, 4.5),(0,0), color='black', linewidth=2)
    plt.plot((0, 0),(-4.5,4.5), color='black', linewidth=2)
    plt.ylabel('valence')
    plt.xlabel('arousal')
    plt.title('32 people each for 40 trails, total 1280 sample')
    plt.show()

def samples_distributed(valence, arousal):
    first_quadrant = 0 #记录每个像限样本数
    second_quadrant = 0
    third_quadrant = 0
    forth_quadrant = 0
    for i in range(len(valence)): 
        if valence[i] > 0 and arousal[i] > 0:
            first_quadrant += 1
        elif valence[i] >= 0 and arousal[i] <= 0:
            second_quadrant += 1
        elif valence[i] < 0 and arousal[i] <= 0:
            third_quadrant += 1
        elif valence[i] <= 0 and arousal[i] > 0:
            forth_quadrant += 1
    total_samples = first_quadrant + second_quadrant + third_quadrant + forth_quadrant
    return first_quadrant, second_quadrant, third_quadrant, forth_quadrant, total_samples
    
if __name__ == '__main__':
    valence, arousal = get_samples_labels(SAMPLE_PATH)
    sample_nums_tuple = samples_distributed(valence, arousal)
    print('The number of samples in the first quadrant is: '+str(sample_nums_tuple[0]))
    print('The number of samples in the second quadrant is: '+str(sample_nums_tuple[1]))
    print('The number of samples in the third quadrant is: '+str(sample_nums_tuple[2]))
    print('The number of samples in the forth quadrant is: '+str(sample_nums_tuple[3]))
    print('The number of total samples is: '+str(sample_nums_tuple[4]))
    labels_plot(arousal, valence)

