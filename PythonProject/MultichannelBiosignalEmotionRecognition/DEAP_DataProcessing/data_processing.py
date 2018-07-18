#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import pickle
import numpy

SAMPLE_PATH = 'samples/'
_samples_dir_name_1 = ['s0'+str(i+1) for i in range(9)]
_samples_dir_name_2 = ['s'+str(i+1) for i in range(9,32)]
samples_dir_name = _samples_dir_name_1 + _samples_dir_name_2

def parse_data_to_samples(sample_path=SAMPLE_PATH):
    for i in range(32):
        if not os.path.isdir(os.path.join(sample_path, samples_dir_name[i])):
            os.makedirs(os.path.join(sample_path, samples_dir_name[i]))

    _raw_data_list_1 = [pickle.load(open('./data/s0'+str(i+1)+'.dat', 'rb'), encoding='iso-8859-1') 
                     for i in range(9)]
    _raw_data_list_2 = [pickle.load(open('./data/s'+str(i+1)+'.dat', 'rb'), encoding='iso-8859-1') 
                     for i in range(9,32)]
    raw_data_list =  _raw_data_list_1 +  _raw_data_list_2
    data_list = [raw_data_list[i]['data'] for i in range(32)]
    label_list = [raw_data_list[i]['labels'] for i in range(32)]
    for i in range(32):
        sample_trial_path = os.path.join(sample_path, samples_dir_name[i])
        numpy.savetxt(sample_trial_path+'/label.csv', label_list[i], delimiter=',')
        for j in range(40):
            numpy.savetxt(sample_trial_path+'/trial_'+str(j+1)+'.csv', data_list[i][j,:,:], delimiter=',')

if __name__ == '__main__':
    parse_data_to_samples()
