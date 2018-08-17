#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import numpy as np
import tensorflow as tf
from keras import layers
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from resnets_utils import *
from keras.initializers import glorot_uniform
import scipy.misc
from matplotlib.pyplot import imshow
import keras.backend as K
K.set_image_data_format('channels_last')
K.set_learning_phase(1)

# the identity block for ResNet
def identity_block(X, f, filters, stage, block):
    '''
    Arguments:
    X--input tensor of shape(m, n_H_prev, n_W_prev, n_c_prev)
    f--integer, specifying the shape of the middle CONV windows for the main path
    filters--list of integers, defining the number of filters in the CONV layers of the main path
    stage--integer, used to name the layers, depending on their position in the network
    block--string/character, used to name the layers, depending on their position in the network
    Returns:
    X--output of the identity block, tensor of shape(n_H, n_W, n_c)
    '''
    #defining name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    #Retrieve filters
    F1, F2, F3 = filters
    X_shortcut = X
    #first component of main path
    X = Conv2D(filters=F1, kernel_size=(1,1), strides=(1,1), padding="valid", name=conv_name_base+'2a', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2a')(X)
    X = Activation('relu')(X)
    #second component of main path
    X = Conv2D(filters=F2, kernel_size=(f,f), strides=(1,1), padding='same', name=conv_name_base+'2b', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2b')(X)
    X = Activation('relu')(X)
    #third component of main path
    X = Conv2D(filters=F3, kernel_size=(1,1), strides=(1,1), padding='valid', name=conv_name_base+'2c', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2c')(X)
    X = layers.add([X, X_shortcut])
    X = Activation('relu')(X)
    return X
#convolutional block (in the case that the input and output dimensions don't match up)
def convolutional_block(X, f, filters, stage, block, s=2):
    '''
    X--input tensor of shape(m, n_H_prev, n_W_prev, n_c_prev)
    f--integer, specifying the shape of the middle CONV windows for the main path
    filters--list of integers, defining the number of filters in the CONV layers of the main path
    stage--integer, used to name the layers, depending on their position in the network
    block--string/character, used to name the layers, depending on their position in the network
    s--integer, specifying the stride to be used
    Returns:
    X--output of the identity block, tensor of shape(n_H, n_W, n_c)
    '''
    #defining name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    #Retrieve filters
    F1, F2, F3 = filters
    X_shortcut = X
    #first component of main path
    X = Conv2D(filters=F1, kernel_size=(1,1), strides=(s,s), padding="valid", name=conv_name_base+'2a', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2a')(X)
    X = Activation('relu')(X)
    #second component of main path
    X = Conv2D(filters=F2, kernel_size=(f,f), strides=(1,1), padding='same', name=conv_name_base+'2b', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2b')(X)
    X = Activation('relu')(X)
    #third component of main path
    X = Conv2D(filters=F3, kernel_size=(1,1), strides=(1,1), padding='valid', name=conv_name_base+'2c', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base+'2c')(X)
    X_shortcut = Conv2D(filters=F3, kernel_size=(1,1), strides=(s,s), name=conv_name_base+'1', padding='valid', kernel_initializer=glorot_uniform(seed=0))(X_shortcut)
    X_shortcut = BatchNormalization(axis=3, name=bn_name_base+'1')(X_shortcut)
    X = layers.add([X, X_shortcut])
    X = Activation('relu')(X)
    return X
# ResNet model(50 layers)
def ResNet50(input_shape=(64, 64, 3), classes=6):
    '''
    Implementation of the popular ResNet50 the following architecture:
        CONV2D -> BATCHNORM -> RELU -> MAXPOOL -> CONVBLOCK -> IDBLOCK*2 -> CONVBLOCK -> IDBLOCK*3-> CONVBLOCK -> 
        IDBLOCK*5 -> CONVBLOCK -> IDBLOCK*2 -> AVGPOOL -> TOPLAYER
    Arguments:
    input_shape--shape of the images of the dataset
    classes--integer, number of classes
    Returns:
    model--a Model() instance in Keras
    '''
    #define the input as a tensor with shape input_shape
    X_input = Input(input_shape)
    #Zero-padding
    X = ZeroPadding2D((3,3))(X_input)
    #stage 1
    X = Conv2D(filters=64, kernel_size=(7,7), strides=(2,2), name='conv1', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name='bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D(pool_size=(3,3), strides=(2,2))(X)
    #stage 2
    X = convolutional_block(X, f=3, filters=[64, 64, 256], stage=2, block='a', s=1)
    X = identity_block(X, f=3, filters=[64, 64, 256], stage=2, block='b')
    X = identity_block(X, f=3, filters=[64, 64, 256], stage=2, block='c')
    #stage 3
    X = convolutional_block(X, f=3, filters=[128,128,512], stage=3, block='a', s=2)
    X = identity_block(X, f=3, filters=[128,128,512], stage=3, block='b')
    X = identity_block(X, f=3, filters=[128,128,512], stage=3, block='c')
    X = identity_block(X, f=3, filters=[128,128,512], stage=3, block='d')
    #stage 4
    X = convolutional_block(X, f=3, filters=[256,256,1024], stage=4, block='a', s=2)
    X = identity_block(X, f=3, filters=[256,256,1024], stage=4, block='b')
    X = identity_block(X, f=3, filters=[256,256,1024], stage=4, block='c')
    X = identity_block(X, f=3, filters=[256,256,1024], stage=4, block='d')
    X = identity_block(X, f=3, filters=[256,256,1024], stage=4, block='e')
    X = identity_block(X, f=3, filters=[256,256,1024], stage=4, block='f')
    #stage 5
    X = convolutional_block(X, f=3, filters=[512,512,2048], stage=5, block='a', s=2)
    X = identity_block(X, f=3, filters=[256,256,2048], stage=5, block='b')
    X = identity_block(X, f=3, filters=[256,256,2048], stage=5, block='c')
    #AVGPOOL
    X = AveragePooling2D(pool_size=(2,2))(X)
    #output layer
    X = Flatten()(X)
    X = Dense(classes, activation='softmax', name='fc'+str(classes), kernel_initializer=glorot_uniform(seed=0))(X)
    #model
    model = Model(inputs=X_input, outputs=X, name='ResNet50')
    return model

if __name__ == '__main__':
    model = ResNet50(input_shape=(64,64,3), classes=6)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()
    # Normalize image vectors
    X_train = X_train_orig/255.
    X_test = X_test_orig/255.
    # Convert training and test labels to one hot matrices
    Y_train = convert_to_one_hot(Y_train_orig, 6).T
    Y_test = convert_to_one_hot(Y_test_orig, 6).T
    print('-'*50)
    print ("number of training examples = " + str(X_train.shape[0]))
    print ("number of test examples = " + str(X_test.shape[0]))
    print ("X_train shape: " + str(X_train.shape))
    print ("Y_train shape: " + str(Y_train.shape))
    print ("X_test shape: " + str(X_test.shape))
    print ("Y_test shape: " + str(Y_test.shape))
    print('-'*50)
    model.fit(X_train, Y_train, epochs=20, batch_size=32)
    preds = model.evaluate(X_test, Y_test)
    print('-'*50)
    print('loss = '+str(preds[0]))
    print('test accuracy = '+str(preds[1]))
