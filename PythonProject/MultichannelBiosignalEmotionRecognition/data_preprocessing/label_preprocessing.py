#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
################################################################
# 通过k-means 聚类算法将每个志愿者对应的单独评分（40个实验）进行
# 聚类（4个象限，4个类别）。最后用 one-hot 方法将每个实验对应的
# 标签进行编码。
################################################################
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

SAMPLES_PATH = '../data_analysis/samples/'

def get_samples_labels(path):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    labels = [np.loadtxt(file_path[i]+'/label.csv', delimiter=',', skiprows=0)[:,:2] 
                         for i in range(len(file_path))]
    return labels

def k_means_cluster(input_data, k=4, seed=0):
    labels = input_data
    kmeans = KMeans(n_clusters=k, random_state=seed)
    first_quadrant_number = 0
    second_quadrant_number = 0
    third_quadrant_number = 0
    fourth_quadrant_number = 0
    y_labels = []
    cluster_centers_list = []
    for label in labels:
        cluster_result = kmeans.fit(label)
        cluster_centers_list.append(cluster_result.cluster_centers_)
        #assert(kmeans.cluster_centers_[0][0]-5>0 and kmeans.cluster_centers_[0][1]-5>0)
        #assert(kmeans.cluster_centers_[1][0]-5<0 and kmeans.cluster_centers_[1][1]-5>0)
        #assert(kmeans.cluster_centers_[2][0]-5<0 and kmeans.cluster_centers_[2][1]-5<0)
        #assert(kmeans.cluster_centers_[3][0]-5>0 and kmeans.cluster_centers_[3][1]-5<0)
        first_quadrant_number += len(list(filter(lambda x: x==0, kmeans.labels_)))
        second_quadrant_number += len(list(filter(lambda x: x==1, kmeans.labels_)))
        third_quadrant_number += len(list(filter(lambda x: x==2, kmeans.labels_)))
        fourth_quadrant_number += len(list(filter(lambda x: x==3, kmeans.labels_)))
        y_label = kmeans.labels_.reshape(40,1)
        y_labels.append(y_label)
    total_sample_nunmber = first_quadrant_number + second_quadrant_number + \
                           third_quadrant_number + fourth_quadrant_number
    samples__labels_distributed_number = {'first_quadrant_number':first_quadrant_number,
                                          'second_quadrant_number':second_quadrant_number,
                                          'third_quadrant_number':third_quadrant_number,
                                          'fourth_quadrant_number':fourth_quadrant_number,
                                          'total_sample_number':total_sample_nunmber,
                                          }
    return y_labels, samples__labels_distributed_number, cluster_centers_list

def convert_to_one_hot(Y, class_number):
    labels = Y
    y_label = [np.eye(class_number)[labels[i].reshape(-1)] for i in range(len(labels))] 
    return y_label

def save_y_labels_to_csv(y_labels, path):
    samples_dirs = os.listdir(path) #目录的顺序是随机的
    samples_dirs = sorted(samples_dirs)
    file_path = [os.path.join(path, samples_dirs[i]) for i in range(len(samples_dirs))]
    for i in range(len(file_path)):
        if not os.path.exists(file_path[i] + '/one_hot_label.csv'):
            np.savetxt(file_path[i] + '/one_hot_label.csv', y_labels[i], fmt='%d', delimiter=',')

def label_cluster_visualization(cluster_labels):
    plt.figure(2)
    assert(len(cluster_labels) == 32)
    count = 0
    for cluster_label in cluster_labels:
        x = cluster_label[:,1] #arousal
        y = cluster_label[:,0] #valence
        plt.subplot(4,8,count+1)
        plt.scatter(x, y)
        plt.xlim([0.5, 9.5])
        plt.ylim([0.5, 9.5])
        plt.plot((0.5, 9.5),(5,5), color='black', linewidth=1)
        plt.plot((5, 5),(0.5,9.5), color='black', linewidth=1)
        plt.subplots_adjust(wspace=0.1, left=0.03, right=0.99, top=0.95, bottom=0.01)
        #plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        count += 1
    plt.show()
def label_visualization_for_every_person(labels):
    plt.figure(1)
    count = 0
    for label in labels:
        x = label[:,1]
        y = label[:,0]
        plt.subplot(4,8,count+1)
        plt.scatter(x, y)
        plt.xlim([0.5, 9.5])
        plt.ylim([0.5, 9.5])
        plt.plot((0.5, 9.5),(5,5), color='black', linewidth=1)
        plt.plot((5, 5),(0.5,9.5), color='black', linewidth=1)
        plt.subplots_adjust(wspace=0.1, left=0.03, right=0.99, top=0.95, bottom=0.01)
        #plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        count += 1
    #plt.show()

if __name__ == '__main__':
    labels = get_samples_labels(SAMPLES_PATH)
    label_visualization_for_every_person(labels)
    y_labels, samples_labels_information, cluster_centers_list = k_means_cluster(labels, k=4, seed=0)
    label_cluster_visualization(cluster_centers_list)
    #y_labels = convert_to_one_hot(y_labels, class_number=4)
    #save_y_labels_to_csv(y_labels, SAMPLES_PATH)
    #print('first quadrant: '+str(samples_labels_information['first_quadrant_number']))
    #print('second quadrant: '+str(samples_labels_information['second_quadrant_number']))
    #print('third quadrant: '+str(samples_labels_information['third_quadrant_number']))
    #print('fourth quadrant: '+str(samples_labels_information['fourth_quadrant_number']))
    #print(' total samples: '+str(samples_labels_information['total_sample_number']))
