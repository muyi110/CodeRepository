#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import math
import os
import numpy as np
np.random.seed(123)
print('NumPy:{}'.format(np.__version__))
import pandas as pd
print('Pandas:{}'.format(pd.__version__))
import sklearn as sk
from sklearn import preprocessing as skpp
print('Scikit-Learn:{}'.format(sk.__version__))
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({'font.size':20, 'figure.figsize':[15,10]})
print('Matplotlib:{}'.format(mpl.__version__))
import tensorflow as tf
tf.set_random_seed(123)
print('TensorFlow:{}'.format(tf.__version__))

#import data
DATASETSLIB_HOME = './dataset'
filepath = os.path.join(DATASETSLIB_HOME, 
                        'international-airline-passengers.csv')
#header=0: specify the first row as column index
#usecols[1]: read the '1'th column data
dataframe = pd.read_csv(filepath, usecols=[1], header=0)
dataset = dataframe.values
dataset = dataset.astype(np.float32)
#visualizing data
plt.plot(dataset, label='Original Data')
plt.legend() #show the label
plt.xlabel('Timesteps')
plt.ylabel('Total Passengers')
plt.show()
#normalize the dataset
scaler = skpp.MinMaxScaler(feature_range=(0,1))
normalized_dataset = scaler.fit_transform(dataset)
#in case of timeseries, always split test train first
def train_test_split(timeseries, train_size=0.75, val_size=0.0):
    if train_size >= 1:
        raise ValueError('train_size has to be between 0 and 1')
    if val_size >= 1:
        raise ValueError('val_size has to be between 0 and 1')
    N = timeseries.shape[0]
    train_size = int(N * train_size)
    val_size = int(N * val_size)
    test_size = N- train_size - val_size
    if(val_size > 0):
        train, val, test = timeseries[:train_size],\
                           timeseries[train_size:train_size+val_size],\
                           timeseries[train_size+val_size:]
        return train, val, test
    else:
        train, test = timeseries[0:train_size],\
                      timeseries[train_size:len(timeseries)]
        return train, test

def mvts_to_xy(*tslist, n_x=1, n_y=1, x_idx=None, y_idx=None):
    n_ts = len(tslist)
    if n_ts == 0:
        raise ValueError('At least one timeseries required as input')
    result = []
    for ts in tslist:
        ts_cols = 1 if ts.ndim == 1 else ts.shape[1]
        if x_idx is None:
            x_idx = range(0, ts_cols)
        if y_idx is None:
            y_idx = range(0, ts_cols)
        n_x_vars = len(x_idx)#number of x variables
        n_y_vars = len(y_idx)#number of y variables
        ts_rows = ts.shape[0]
        n_rows = ts_rows - n_x - n_y + 1#number of samples
        dataX = np.empty(shape=(n_rows, n_x_vars*n_x), dtype=np.float32)
        dataY = np.empty(shape=(n_rows, n_y_vars*n_y), dtype=np.float32)
        #input sequence x (t-n,...t-1)
        from_col = 0
        for i in range(n_x, 0, -1):
            dataX[:, from_col:from_col+n_x_vars] = shift(ts[:,x_idx],i)[n_x:ts_rows-n_y+1]
            from_col = from_col + n_x_vars
        #forecast sequence(t, t+1, ..., t+n)
        from_col = 0
        for i in range(0, n_y):
            dataY[:, from_col:from_col+n_y_vars] = shift(ts[:,y_idx],i)[n_x:ts_rows-n_y+1]
            from_col = from_col + n_y_vars
        result.append(dataX)
        result.append(dataY)
    return result
            
def shift(arr, num, fill_value=0):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result = arr
    return result

#split into train and test sets
train, test = train_test_split(normalized_dataset, train_size=0.67)
#convert into supervised learning set of input data and label
n_x = 1 #number of past timesteps to learn/predict next step
n_y = 1 #number of future time steps to learn/predict
X_train, Y_train, X_test, Y_test = mvts_to_xy(train, test, n_x=n_x, n_y=n_y)
#TensorFLow SimpleRNN for TimeSeries Data
state_size = 4
n_epochs = 600
n_timesteps = n_x
n_x_vars = 1
n_y_vars = 1
learning_rate = 0.1
tf.reset_default_graph()
X_p = tf.placeholder(tf.float32,[None, n_timesteps, n_x_vars], name='X_p')
Y_p = tf.placeholder(tf.float32,[None, n_timesteps, n_y_vars], name='Y_p')
rnn_inputs = tf.unstack(X_p, axis=1)
cell = tf.nn.rnn_cell.BasicRNNCell(state_size)
rnn_outputs, final_state = tf.nn.static_rnn(cell, rnn_inputs, dtype=tf.float32)
W = tf.get_variable('W', [state_size, n_y_vars])
b = tf.get_variable('b', [n_y_vars], initializer=tf.constant_initializer(0.0))
predictions = [tf.matmul(rnn_output, W) + b for rnn_output in rnn_outputs]
print(predictions)
y_as_list = tf.unstack(Y_p, num=n_timesteps, axis=1)
print(y_as_list)
mse = tf.losses.mean_squared_error
losses = [mse(labels=label, predictions=prediction) \
          for prediction, label in zip(predictions, y_as_list)]
total_loss = tf.reduce_mean(losses)
optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(total_loss)

with tf.Session() as tfs:
    tfs.run(tf.global_variables_initializer())
    epoch_loss = 0.0
    for epoch in range(n_epochs):
        feed_dict = {X_p:X_train.reshape(-1, n_timesteps, n_x_vars),
                     Y_p:Y_train.reshape(-1, n_timesteps, n_x_vars)}
        epoch_loss, y_train_pred, _ = tfs.run([total_loss, predictions, optimizer], feed_dict=feed_dict)
    print('train_mse = {}'.format(epoch_loss))
    feed_dict = {X_p:X_test.reshape(-1, n_timesteps, n_x_vars),
                 Y_p:Y_test.reshape(-1, n_timesteps, n_y_vars)}
    test_loss, y_test_pred = tfs.run([total_loss, predictions], feed_dict=feed_dict)
    print('test_mse = {}'.format(test_loss))
    print('test rmse = {}'.format(math.sqrt(test_loss)))

y_train_pred = y_train_pred[0]
y_test_pred = y_test_pred[0]
#invert predictions
y_train_pred = scaler.inverse_transform(y_train_pred)
y_test_pred = scaler.inverse_transform(y_test_pred)
#invert originals
y_train_orig = scaler.inverse_transform(Y_train)
y_test_orig = scaler.inverse_transform(Y_test)
#shift train predictions for plotting
trainPredicPlot = np.empty_like(dataset)
trainPredicPlot[:,:] = np.nan
trainPredicPlot[n_x-1:len(y_train_pred)+n_x-1,:] = y_train_pred
#shift test predictions for plotting
testPredicPlot = np.empty_like(dataset)
testPredicPlot[:,:] = np.nan
testPredicPlot[len(y_train_pred)+(n_x*2)-1:len(dataset)-1,:] = y_test_pred
#plot baseline and predictions
plt.plot(dataset, label='Original Data')
plt.plot(trainPredicPlot, label='y_train_pred')
plt.plot(testPredicPlot, label='y_test_pred')
plt.legend()
plt.xlabel('Timesteps')
plt.ylabel('Total Passengers')
plt.show()

#Tensorflow LSTM for TimeSeries Data
n_epochs = 600
n_timesteps = n_x
n_x_vars = 1
n_y_vars = 1
learning_rate = 0.1
tf.reset_default_graph()
X_p = tf.placeholder(tf.float32,[None, n_timesteps, n_x_vars], name='X_p')
Y_p = tf.placeholder(tf.float32,[None, n_timesteps, n_y_vars], name='Y_p')
rnn_inputs = tf.unstack(X_p, axis=1)
cell = tf.nn.rnn_cell.LSTMCell(state_size)
rnn_outputs, final_state = tf.nn.static_rnn(cell, rnn_inputs, dtype=tf.float32)
W = tf.get_variable('W', [state_size, n_y_vars])
b = tf.get_variable('b', [n_y_vars], initializer=tf.constant_initializer(0.0))
predictions = [tf.matmul(rnn_output, W)+b for rnn_output in rnn_outputs]
y_as_list = tf.unstack(Y_p, num=n_timesteps, axis=1)
mse = tf.losses.mean_squared_error
losses = [mse(labels=label, predictions=prediction) for prediction, label in zip(predictions, y_as_list)]
total_loss = tf.reduce_mean(losses)
optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(total_loss)

with tf.Session() as tfs:
    tfs.run(tf.global_variables_initializer())
    epoch_loss = 0.0
    for epoch in range(n_epochs):
        feed_dict = {X_p:X_train.reshape(-1, n_timesteps, n_x_vars),
                     Y_p:Y_train.reshape(-1, n_timesteps, n_x_vars)}
        epoch_loss, y_train_pred, _ = tfs.run([total_loss, predictions, optimizer], feed_dict=feed_dict)
    print('train_mse = {}'.format(epoch_loss))
    feed_dict = {X_p:X_test.reshape(-1, n_timesteps, n_x_vars),
                 Y_p:Y_test.reshape(-1, n_timesteps, n_y_vars)}
    test_loss, y_test_pred = tfs.run([total_loss, predictions], feed_dict=feed_dict)
    print('test_mse = {}'.format(test_loss))
    print('test rmse = {}'.format(math.sqrt(test_loss)))

y_train_pred = y_train_pred[0]
y_test_pred = y_test_pred[0]
#invert predictions
y_train_pred = scaler.inverse_transform(y_train_pred)
y_test_pred = scaler.inverse_transform(y_test_pred)
#invert originals
y_train_orig = scaler.inverse_transform(Y_train)
y_test_orig = scaler.inverse_transform(Y_test)
#shift train predictions for plotting
trainPredicPlot = np.empty_like(dataset)
trainPredicPlot[:,:] = np.nan
trainPredicPlot[n_x-1:len(y_train_pred)+n_x-1,:] = y_train_pred
#shift test predictions for plotting
testPredicPlot = np.empty_like(dataset)
testPredicPlot[:,:] = np.nan
testPredicPlot[len(y_train_pred)+(n_x*2)-1:len(dataset)-1,:] = y_test_pred
#plot baseline and predictions
plt.plot(dataset, label='Original Data')
plt.plot(trainPredicPlot, label='y_train_pred')
plt.plot(testPredicPlot, label='y_test_pred')
plt.legend()
plt.xlabel('Timesteps')
plt.ylabel('Total Passengers')
plt.show()

#TensorFlow GRU for TimeSeries Data

n_epochs = 600
n_timesteps = n_x
n_x_vars = 1
n_y_vars = 1
learning_rate = 0.1
tf.reset_default_graph()
X_p = tf.placeholder(tf.float32,[None, n_timesteps, n_x_vars], name='X_p')
Y_p = tf.placeholder(tf.float32,[None, n_timesteps, n_y_vars], name='Y_p')
rnn_inputs = tf.unstack(X_p, axis=1)
cell = tf.nn.rnn_cell.GRUCell(state_size)
rnn_outputs, final_state = tf.nn.static_rnn(cell, rnn_inputs, dtype=tf.float32)
W = tf.get_variable('W', [state_size, n_y_vars])
b = tf.get_variable('b', [n_y_vars], initializer=tf.constant_initializer(0.0))
predictions = [tf.matmul(rnn_output, W)+b for rnn_output in rnn_outputs]
y_as_list = tf.unstack(Y_p, num=n_timesteps, axis=1)
mse = tf.losses.mean_squared_error
losses = [mse(labels=label, predictions=prediction) for prediction, label in zip(predictions, y_as_list)]
total_loss = tf.reduce_mean(losses)
optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(total_loss)

with tf.Session() as tfs:
    tfs.run(tf.global_variables_initializer())
    epoch_loss = 0.0
    for epoch in range(n_epochs):
        feed_dict = {X_p:X_train.reshape(-1, n_timesteps, n_x_vars),
                     Y_p:Y_train.reshape(-1, n_timesteps, n_y_vars)}
        epoch_loss, y_train_pred, _ = tfs.run([total_loss, predictions, optimizer], feed_dict=feed_dict)
    print('train_mse = {}'.format(epoch_loss))
    feed_dict = {X_p:X_test.reshape(-1, n_timesteps, n_x_vars),
                 Y_p:Y_test.reshape(-1, n_timesteps, n_y_vars)}
    test_loss, y_test_pred = tfs.run([total_loss, predictions], feed_dict=feed_dict)
    print('test_mse = {}'.format(test_loss))
    print('test rmse = {}'.format(math.sqrt(test_loss)))

y_train_pred = y_train_pred[0]
y_test_pred = y_test_pred[0]
#invert predictions
y_train_pred = scaler.inverse_transform(y_train_pred)
y_test_pred = scaler.inverse_transform(y_test_pred)
#invert originals
y_train_orig = scaler.inverse_transform(Y_train)
y_test_orig = scaler.inverse_transform(Y_test)
#shift train predictions for plotting
trainPredicPlot = np.empty_like(dataset)
trainPredicPlot[:,:] = np.nan
trainPredicPlot[n_x-1:len(y_train_pred)+n_x-1,:] = y_train_pred
#shift test predictions for plotting
testPredicPlot = np.empty_like(dataset)
testPredicPlot[:,:] = np.nan
testPredicPlot[len(y_train_pred)+(n_x*2)-1:len(dataset)-1,:] = y_test_pred
#plot baseline and predictions
plt.plot(dataset, label='Original Data')
plt.plot(trainPredicPlot, label='y_train_pred')
plt.plot(testPredicPlot, label='y_test_pred')
plt.legend()
plt.xlabel('Timesteps')
plt.ylabel('Total Passengers')
plt.show()
