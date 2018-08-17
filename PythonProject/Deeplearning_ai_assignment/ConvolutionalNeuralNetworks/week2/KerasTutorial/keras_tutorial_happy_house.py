#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import keras
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from kt_utils import *
import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

# model
def HappyModel(input_shape):
    '''
    Arguments:
    input_shape--shape of the images of the dataset
    Returns:
    model--a Model() instance in Keras
    '''
    X_input = Input(shape=input_shape)
    X = ZeroPadding2D(padding=(1, 1))(X_input)
    X = Conv2D(filters=8, kernel_size=(3,3), strides=(1, 1))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)
    X = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid')(X)

    X = ZeroPadding2D(padding=(1, 1))(X)
    X = Conv2D(filters=16, kernel_size=(3,3), strides=(1, 1))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)
    X = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid')(X)

    X = ZeroPadding2D(padding=(1, 1))(X)
    X = Conv2D(filters=32, kernel_size=(3,3), strides=(1, 1))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)
    X = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid')(X)
    #FC
    X = Flatten()(X)
    Y = Dense(1, activation='sigmoid')(X)
    model = Model(inputs=X_input, outputs=Y, name='HappyModel')
    return model

if __name__ == '__main__':
    X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()
    X_train = X_train_orig / 255.
    X_test = X_test_orig / 255.
    Y_train = Y_train_orig.T
    Y_test = Y_test_orig.T
    print('-'*50)
    print('number of training examples = '+str(X_train.shape[0]))
    print('number of test examples = '+str(X_test.shape[0]))
    print('X_train shape: '+str(X_train.shape))
    print('X_test shape: '+str(X_test.shape))
    print('Y_train shape: '+str(Y_train.shape))
    print('Y_test shape: '+str(Y_test.shape))
    print('-'*50)
    happyModel = HappyModel((64, 64, 3))
    happyModel.compile(optimizer=keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0), loss='binary_crossentropy', metrics=['accuracy'])
    happyModel.fit(x=X_train, y=Y_train, batch_size=16, epochs=20)
    preds = happyModel.evaluate(x=X_test, y=Y_test)
    print('Loss = '+str(preds[0]))
    print('Test accurary = '+str(preds[1]))
