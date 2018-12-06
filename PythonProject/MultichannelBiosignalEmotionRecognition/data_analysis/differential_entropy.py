#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

SAMPLE_PATH = "./samples/"

def get_sample_data(path=SAMPLE_PATH, people_num=0, trial_num=1):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    data = np.loadtxt(file_path[people_num] + "/trial_" + str(trial_num) + ".csv", delimiter=",", skiprows=0)
    eeg_data = data[:32,128*3:]
    return eeg_data

def data_filter(X):
    b_theta, a_theta = signal.butter(6, [0.0625, 0.109375], "bandpass")
    b_alpha, a_alpha = signal.butter(6, [0.125, 0.203125], "bandpass")
    b_beta, a_beta = signal.butter(6, [0.21875, 0.46875], "bandpass")
    b_gamma, a_gamma = signal.butter(6, 0.484375, "highpass")

    theta = signal.filtfilt(b_theta, a_theta, X).reshape(-1)
    alpha = signal.filtfilt(b_alpha, a_alpha, X).reshape(-1)
    beta = signal.filtfilt(b_beta, a_beta, X).reshape(-1)
    gamma = signal.filtfilt(b_gamma, a_gamma, X).reshape(-1)

    return (theta, alpha, beta, gamma)

if __name__ == "__main__":
    eeg = get_sample_data(people_num=0, trial_num=1)[0][128*3:]
    eeg = (eeg - eeg.min()) / (eeg.max() - eeg.min())
    theta, alpha, beta, gamma = data_filter(eeg)
    print(theta[128*1:128*10].var())
    print(alpha[128*1:128*10].var())
    print(beta[128*1:128*10].var())
    print(gamma[128*1:128*10].var())
    plt.figure("eeg")
    plt.plot(eeg)
    plt.grid()
    plt.figure("subband")
    plt.subplot(4,1,1)
    plt.plot(theta)
    plt.grid()
    plt.subplot(4,1,2)
    plt.plot(alpha)
    plt.grid()
    plt.subplot(4,1,3)
    plt.plot(beta)
    plt.grid()
    plt.subplot(4,1,4)
    plt.plot(gamma)
    plt.grid()
    plt.show()
