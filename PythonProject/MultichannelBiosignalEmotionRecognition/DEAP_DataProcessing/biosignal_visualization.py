#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import pickle
import matplotlib.pyplot as plt

# 可视化第一个志愿者，第一个实验的生理数据
data = pickle.load(open('./data/s01.dat', 'rb'), encoding='iso-8859-1')
eegData = data['data'][0, 0:32, :]
#EEG
fig = plt.figure(1)
eegData_channel = [fig.add_subplot(32, 1, i+1) for i in range(32)]
for i in range(32):
    eegData_channel[i].plot(eegData[i,:])
    eegData_channel[i].set_xlim(0, 8064)
    eegData_channel[i].set_xticks([])
    eegData_channel[i].set_yticks([])
    eegData_channel[i].set_ylabel(str(i+1),va='center', labelpad=10, rotation=0)
plt.subplots_adjust(left=0.03, right=0.99, top=0.99, bottom=0.01)
#外周生理信号
perData = data['data'][0, 32:, :]
fig2 = plt.figure(2)
perData_channel = [fig2.add_subplot(4, 2, i+1) for i in range(8)]
for i in range(8):
    perData_channel[i].plot(perData[i,:])
    perData_channel[i].set_xlim(0, 8064)
    perData_channel[i].set_xticks([])
    #perData_channel[i].set_yticks([])
perData_channel[0].set_title('hEOG')
perData_channel[1].set_title('vEOG')
perData_channel[2].set_title('zEMG')
perData_channel[3].set_title('tEMG')
perData_channel[4].set_title('GSR')
perData_channel[5].set_title('Respiration')
perData_channel[6].set_title('Plethysmograph')
perData_channel[7].set_title('Temperature')
plt.subplots_adjust(wspace=0.1, left=0.03, right=0.99, top=0.95, bottom=0.01)
plt.show()
