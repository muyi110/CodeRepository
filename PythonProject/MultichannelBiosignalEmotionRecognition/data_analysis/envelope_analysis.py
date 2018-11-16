#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import PyEMD

SAMPLE_PATH = "./samples/"

def get_sample_data(path=SAMPLE_PATH, people_num=0, trial_num=1):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    data = np.loadtxt(file_path[people_num] + "/trial_" + str(trial_num) + ".csv", delimiter=",", skiprows=0)
    eeg_data = data[:32,128*3:]
    return eeg_data

def data_filter(eeg):
    b_theta, a_theta = signal.butter(4, [0.0625, 0.109375], "bandpass") # 4-7Hz
    b_alpha, a_alpha = signal.butter(4, [0.125, 0.203125], "bandpass")  # 8-13Hz
    b_beta, a_beta = signal.butter(4, [0.21875, 0.46875], "bandpass")   # 14-30Hz
    b_gamma, a_gamma = signal.butter(4, 0.484375, "highpass")           # >=31Hz

    theta = signal.filtfilt(b_theta, a_theta, eeg).reshape(-1)
    alpha = signal.filtfilt(b_alpha, a_alpha, eeg).reshape(-1)
    beta = signal.filtfilt(b_beta, a_beta, eeg).reshape(-1)
    gamma = signal.filtfilt(b_gamma, a_gamma, eeg).reshape(-1)
    assert (len(theta) == len(beta))
    
    return (theta, alpha, beta, gamma)

def plot(data, figure_num=1, max_spline=None, min_spline=None):
    num = data.shape[0]
    plt.figure(figure_num)
    for i in range(1, num + 1):
        plt.subplot(num, 1, i)
        plt.plot(data[i-1])
        if max_spline is not None :
            plt.plot(max_spline[i-1])
        if min_spline is not None:
            plt.plot(min_spline[i-1])
        plt.grid()
    plt.show()

def get_envelope(signal, T):
    # emd = PyEMD.EMD()
    emd = PyEMD.EMD(extrema_detection="parabol")
    splines = emd.extract_max_min_spline(T, signal)
    max_spline = splines[0]
    min_spline = splines[1]
    
    return max_spline, min_spline 

def fft(datas):
    fft_result = []
    for data in datas:
        fft_result.append(np.fft.fft(data))

    return fft_result    

if __name__ == "__main__":
    eeg_data = get_sample_data(people_num=0, trial_num=2)
    max_spline, min_spline = get_envelope(eeg_data[0], np.arange(len(eeg_data[0])))
    plot(eeg_data[0].reshape(1,-1), figure_num=1, max_spline=max_spline.reshape(1, -1), min_spline=None)

    theta, alpha, beta, gamma = data_filter(eeg_data[0])
    filt_eeg_data = np.r_[theta.reshape(1, -1), alpha.reshape(1, -1), beta.reshape(1, -1), gamma.reshape(1, -1)]
    max_spline_theta, min_spline_theta = get_envelope(theta, np.arange(len(theta)))
    max_spline_alpha, min_spline_alpha = get_envelope(alpha, np.arange(len(alpha)))
    max_spline_beta, min_spline_beta = get_envelope(beta, np.arange(len(beta)))
    max_spline_gamma, min_spline_gamma = get_envelope(gamma, np.arange(len(gamma)))
    filt_eeg_data_max_spline = np.r_[max_spline_theta.reshape(1, -1), max_spline_alpha.reshape(1, -1), max_spline_beta.reshape(1, -1), max_spline_gamma.reshape(1, -1)]
    filt_eeg_data_min_spline = np.r_[min_spline_theta.reshape(1, -1), min_spline_alpha.reshape(1, -1), min_spline_beta.reshape(1, -1), min_spline_gamma.reshape(1, -1)]
    plot(filt_eeg_data, figure_num=2, max_spline = filt_eeg_data_max_spline, min_spline=filt_eeg_data_min_spline)

    signal_list = []
    signal_list.append(max_spline)
    signal_list.append(min_spline)

    raw_eeg_spline_fft = fft(signal_list)  # 一个 list
    filt_eeg_max_spline_fft = fft(filt_eeg_data_max_spline)
    filt_eeg_min_spline_fft = fft(filt_eeg_data_min_spline)

    raw_eeg_spline_fft_x = np.linspace(0, 64, len(raw_eeg_spline_fft[0])//2 - 1)
    filt_eeg_spline_fft_x = np.linspace(0, 64, len(filt_eeg_min_spline_fft[0])//2 - 1)

    plt.figure(3)
    plt.subplot(3,2,1)
    plt.plot(raw_eeg_spline_fft_x, np.abs(raw_eeg_spline_fft[0][1:len(raw_eeg_spline_fft[0])//2]), label="raw top")
    plt.plot(raw_eeg_spline_fft_x, np.abs(raw_eeg_spline_fft[1][1:len(raw_eeg_spline_fft[1])//2]), label="raw bottom")
    plt.grid()
    plt.xlim(0, 20)
    plt.legend()

    plt.subplot(3,2,3)
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_max_spline_fft[0][1:len(filt_eeg_max_spline_fft[0])//2]), label="theta top")
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_min_spline_fft[0][1:len(filt_eeg_min_spline_fft[0])//2]), label="theta bottom")
    plt.grid()
    plt.xlim(0, 5)
    plt.legend()
    
    plt.subplot(3,2,4)
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_max_spline_fft[1][1:len(filt_eeg_max_spline_fft[1])//2]), label="alpha top")
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_min_spline_fft[1][1:len(filt_eeg_min_spline_fft[1])//2]), label="alpha bottom")
    plt.grid()
    plt.xlim(0, 5)
    plt.legend()
    
    plt.subplot(3,2,5)
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_max_spline_fft[2][1:len(filt_eeg_max_spline_fft[2])//2]), label="beta top")
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_min_spline_fft[2][1:len(filt_eeg_min_spline_fft[2])//2]), label="beta bottom")
    plt.grid()
    plt.xlim(0, 10)
    plt.legend()
    
    plt.subplot(3,2,6)
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_max_spline_fft[3][1:len(filt_eeg_max_spline_fft[3])//2]), label="gamma top")
    plt.plot(filt_eeg_spline_fft_x, np.abs(filt_eeg_min_spline_fft[3][1:len(filt_eeg_min_spline_fft[3])//2]), label="gamma bottom")
    plt.grid()
    plt.legend()
    plt.xlim(0, 20)
    plt.show()
