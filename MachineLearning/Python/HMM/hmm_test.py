#!/usr/bin/env python3
# -*- coding=UTF-8 -*-
import numpy as np
from hmm import HMM

states = ("Healthy", "Fever")
observations = ("normal", "cold", "dizzy")
start_probability = {"Healthy": 0.6, "Fever": 0.4}
transition_probability = {
        "Healthy": {"Healthy": 0.7, "Fever": 0.3},
        "Fever": {"Healthy": 0.4, "Fever": 0.6},
        }
emission_probability = {
        "Healthy": {"normal": 0.5, "cold": 0.4, "dizzy": 0.1}, 
        "Fever": {"normal": 0.1, "cold": 0.3, "dizzy": 0.6}, 
        }

def generate_index_map(labels):
    index_label = {}
    label_index = {}
    i = 0
    for l in labels:
        index_label[i] = l
        label_index[l] = i
        i += 1
    return label_index, index_label

def convert_observations_to_index(observations, label_index):
    observations_list = []
    for o in observations:
        observations_list.append(label_index[o])
    return observations_list

def convert_map_to_vector(map_object, label_index):
    v = np.empty(len(map_object), dtype=np.float32) # 返回一个一维数组
    for e in map_object: # 这里的 e 是一个 key 值
        v[label_index[e]] = map_object[e]
    return v

def convert_map_to_matrix(map_object, label_index1, label_index2):
    m = np.empty((len(map_object), len(label_index2)), dtype=np.float32)
    for line in map_object:
        for col in map_object[line]:
            m[label_index1[line]][label_index2[col]] = map_object[line][col]
    return m

if __name__ == "__main__":
    states_label_index, states_index_label = generate_index_map(states)
    observations_label_index, observations_index_label = generate_index_map(observations)
    A = convert_map_to_matrix(transition_probability, states_label_index, states_label_index)
    B = convert_map_to_matrix(emission_probability, states_label_index, observations_label_index)
    observations_index = convert_observations_to_index(observations, observations_label_index)
    pi = convert_map_to_vector(start_probability, states_label_index)
    # 下面测试 viterbi 算法
    h = HMM(A, B, pi)
    V, prev = h.viterbi(observations_index)
    label = ""
    for i in observations_index:
        label += "".join("%10s" % observations_index_label[i])
    print(" "*7 + label)
    for s in range(0, 2):
        print("%7s: " % states_index_label[s] + " ".join("%10s" % ("%f" % v) for v in V[s]))
    print("\nThe most possible states and probability are:")
    p, ss = h.state_path(observations_index)
    for s in ss:
        print(states_index_label[s])
    print("%5f" % p)
    # 下面测试 Baum-Welch 算法
    print("---------Baum-Welch---------")
    observations_data = np.array([1, 0, 0, 1, 0, 1, 0, 2, 1, 2])
    states_data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    guess = HMM(np.array([[0.5,0.5],[0.5,0.5]]), np.array([[0.3,0.3,0.3],[0.3,0.3,0.3]]), np.array([0.5,0.5]))
    newA, newB, newpi = guess.baum_welch(observations_data)
    states_out = guess.state_path(observations_data)[1]
    p = 0.0
    for s in states_data:
        if next(states_out) == s:
            p += 1
    print(p / len(states_data))
    print("new A:\n", newA)
    print("new B:\n", newB)
    print("new pi:\n", newpi)
