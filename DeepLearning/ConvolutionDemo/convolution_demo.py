#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
############################################################################
# 模块功能：读两张图片（一张中国寺庙和一朵花），创建两个7*7滤波器（一个检测
#           垂直边缘，一个检测水平边缘），使用卷积层和池化层应用这两个滤波器
#           ，最后画出特征图。
# 参考：handson-ml book P361
############################################################################
import numpy as np
from sklearn.datasets import load_sample_images
import matplotlib.pyplot as plt
import tensorflow as tf
# Load sample images
dataset = np.array(load_sample_images().images, dtype=np.float32)
batch_size, height, width, channels = dataset.shape
# Create 2 filters
filters_test = np.zeros(shape=(7,7,channels,2), dtype=np.float32)
filters_test[:,3,:,0] = 1 # vertical line
filters_test[3,:,:,1] = 1 # horizontal line
# Create a graph with input X plus a convolutional layer applying the 2 filters
X = tf.placeholder(tf.float32, shape=(None, height, width, channels))
convolution = tf.nn.conv2d(X, filters_test, strides=[1,2,3,1], padding="SAME")
max_pool = tf.nn.max_pool(X, ksize=[1,2,2,1], strides=[1,2,2,1], padding="VALID")

with tf.Session() as sess:
    output = sess.run(convolution, feed_dict={X:dataset})
    output_max_pool = sess.run(max_pool, feed_dict={X:dataset})

print("dataset shape: ", dataset.shape)
print("output shape: ", output.shape)
print("output_max_pool shape", output_max_pool.shape)
dataset[0,:,:,:] /= 255
plt.subplot(331).imshow(dataset[0, :, :, :])
plt.subplot(332).imshow(output[0, :, :, 1])
plt.subplot(333).imshow(output[0, :, :, 0])
dataset[1,:,:,:] /= 255
plt.subplot(334).imshow(dataset[1, :, :, :])
plt.subplot(335).imshow(output[1, :, :, 1])
plt.subplot(336).imshow(output[1, :, :, 0])
plt.subplot(337).imshow(output_max_pool[1].astype(np.uint8))
plt.subplot(338).imshow(output_max_pool[0].astype(np.uint8))
plt.show()
