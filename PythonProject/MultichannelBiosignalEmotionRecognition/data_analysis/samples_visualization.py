#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_PATH = "./samples/"

def get_sample_data(path=SAMPLE_PATH, people_num=0, trial_num=1):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    data = np.loadtxt(file_path[people_num] + "/trial_" + str(trial_num) + ".csv", delimiter=",", skiprows=0)
    eeg_data = data[:32,128*3:]
    return eeg_data

def plot_raw_eeg(eeg, people, trial):
    num = eeg.shape[0]
    col = 2
    row = num // col if (num % col) == 0 else num // col + 1
    plt.figure("people = "+str(people)+", trial = "+str(trial))
    for i in range(num):
        plt.subplot(row, col, i+1)
        # eeg[i] = (eeg[i] - eeg[i].min()) / (eeg[i].max() - eeg[i].min())
        plt.plot(eeg[i])
        plt.grid()

if __name__ == "__main__":
    for people in range(23, 25):
        eeg = get_sample_data(people_num=people, trial_num=2)
        plot_raw_eeg(eeg, people, trial=1)
        plt.subplots_adjust(wspace=0.1, left=0.03, right=0.99, top=0.95, bottom=0.01)
    plt.show()
