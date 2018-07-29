#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
Buliding a logistic regression classifier to recognize cats
'''
import os
import glob
import numbers
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image
from scipy import ndimage
from lr_utils import load_dataset

train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()
#Example of a picture
index = 5
plt.imshow(train_set_x_orig[index])
plt.show()
#print('y = '+str(train_set_y[:, index])+", it's a '"+classes[np.squeeze(train_set_y[:, index])].decode('utf-8')+"'picture.")
#show the dataset information
m_train = train_set_x_orig.shape[0]
m_test = test_set_x_orig.shape[0]
num_px = train_set_x_orig.shape[1]
print('number of training examples: {}.'.format(m_train))
print('number of testing examples: {}.'.format(m_test))
print('height/width of each image: {}.'.format(num_px))
print('each image is of size: ({},{},{}).'.format(num_px, num_px, 3))
print('train_set_x_shape: {}.'.format(train_set_x_orig.shape))
print('train_set_y_shape: {}.'.format(train_set_y.shape))
print('test_set_x_shape: {}.'.format(test_set_x_orig.shape))
print('test_set_y_shape: {}.'.format(test_set_y.shape))
#Reshape the training and test examples. After this, the dataset is a numpy-array where each column represents a flattened image.
train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T
print('-'*50)
print('-'*50)
print('train_set_x_flatten shape: {}.'.format(train_set_x_flatten.shape))
print('train_set_y shape: {}.'.format(train_set_y.shape))
print('test_set_x_flatten shape: {}.'.format(test_set_x_flatten.shape))
print('test_set_y shape: {}.'.format(test_set_y.shape))
print('sanity check after reshaping: {}.'.format(train_set_x_flatten[0:5, 0]))
#Standardize the dataset
train_set_x = train_set_x_flatten / 255.
test_set_x = test_set_x_flatten / 255.
#Common steps for pre-processing a new dataset are:
#1.Figure out the dimensions and shapes of the problem
#2.Reshape the dataset such that each example is now a vector of size(num_px*num_px*3,1)
#3.'Standardize' the data

def sigmoid(z):
    '''
    z--A scalar or numpy array of any size
    '''
    s = 1 / (1 + np.exp(-z))
    return s
#initialize with zeros
def initialize_with_zeros(dim):
    '''
    This function creates a vector of zeros of shape(dim,1) for w    and b to 0.
    Argument:
    dim--size of the w vector we want
    Returns:
    w--initialized vector of shape(dim, 1)
    b--initialized scalar(corresponds to the bias)
    '''
    w = np.zeros((dim, 1))
    b = 0
    assert(w.shape == (dim, 1))
    assert(isinstance(b, numbers.Real))
    return w, b
# propagate algorithm
def propagate(w, b, X, Y):
    '''
    Implement the cost function and it's gradient for the propagation
    Arguments:
    w--weights, a numpy array of size(num_px*num_px*3,1)
    b--bias, a scalar
    X--data of size(num_px*num_px*3, number of examples)
    Y--label of size(1, number of examples)
    Return:
    cost--negative log-likelihood cost for logistic regression
    dw--gradient of loss with repect to w
    db--gradient of loss with respect to b
    grads--a dic with 'dw' and 'db'
    '''
    m = X.shape[1]
    #Forward Propagation
    A = sigmoid(np.dot(w.T, X) + b)
    cost = -1 / m * np.sum(Y * np.log(A) + (1-Y) * np.log(1-A))
    #Backward Propagation
    dw = 1 / m * np.dot(X, (A-Y).T)
    db = 1 / m * np.sum(A-Y)
    grads = {'dw':dw, 'db':db}
    return grads, cost
# Arguments optimize
def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost = False):
    '''
    This function optimizes w and b by running a gradient descent algorithm
    Arguments:
    w--weights, a numpy array of size(num_px*num_px*3,1)
    b--bias, a scalar
    X--data of size(num_px*num_px*3, number of examples)
    Y--label of size(1, number of examples)
    num_iterations--number of iterations of the optimization loop
    learning_rate--learning rate of the gradient descent update rule
    print_cost--True to print the loss every 100 steps
    Return:
    params--dictionary containing w and b
    grads--dictionary containing the gradients of w and b with respect to the cost function
    costs--list of all the costs computed during the optimization, this will be used to plot learning curve
    '''
    costs = []
    for i in range(num_iterations):
        #cost and gradient calculation
        grads, cost = propagate(w, b, X, Y)
        dw = grads['dw']
        db = grads['db']
        #update arguments
        w = w - learning_rate * dw
        b = b - learning_rate * db
        #record the costs(plot curve)
        if i % 100 == 0:
            costs.append(cost)
        #print the cost
        if print_cost and i % 100 == 0:
            print('Cost after iteration {}: {}.'.format(i, cost))
    params = {'w':w, 'b':b}
    grads = {'dw':dw, 'db':db}
    return params, grads, costs
#predict
def predict(w, b, X):
    '''
    Predict whether the label is 0 or 1 using learned arguments
    Arguments:
    w--weights, a numpy array of size(num_px*num_px*3,1)
    b--bias, a scalar
    X--data of size(num_px*num_px*3, number of examples)
    Return:
    Y_prediction--a numpy array containing all predictions
    '''
    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    #w = w.reshape(X.shape[0], 1)
    A = sigmoid(np.dot(w.T, X) + b)
    for i in range(A.shape[1]):
        if A[0, i] <= 0.5:
            Y_prediction[0, i] = 0
        else:
            Y_prediction[0, i] = 1
    assert(Y_prediction.shape == (1, m))
    return Y_prediction
#model
def model(X_train, Y_train, X_test, Y_test, num_iterations=2000, learning_rate = 0.5, print_cost=False):
    '''
    Builds the logistic regression model
    Arguments:
    X_train -- training set represented by a numpy array of shape (num_px*num_px*3, m_train)
    Y_train -- training labels represented by a numpy array of shape (1, m_train)
    X_test -- test set represented by a numpy array of shape (num_px*num_px*3, m_test)
    Y_test -- test labels represented by a numpy array of shape (1, m_test)
    num_iterations -- hyperparameter representing the number of iterations to optimize the parameters
    learning_rate -- hyperparameter representing the learning rate used in the update rule of optimize()
    Return:
    d--information about the model
    '''
    #initialize parameters with zeros
    w, b = initialize_with_zeros(X_train.shape[0])
    #gradient descent
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost)
    w = parameters['w']
    b = parameters['b']
    #predict test/train set 
    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)
    #print train/test Error
    print('train accuracy: {}%'.format(100 - np.mean(np.abs(Y_prediction_train-Y_train)) * 100))
    print('test accuracy: {}%'.format(100 - np.mean(np.abs(Y_prediction_test-Y_test)) * 100))
    d = {'costs':costs,'Y_prediction_test':Y_prediction_test,
         'Y_prediction_train':Y_prediction_train, 'w':w,
         'b':b, 'learning_rate':learning_rate, 
         'num_iterations':num_iterations,
         }
    return d

if __name__ == '__main__':
    print('-'*50)
    print('-'*50)
    d = model(train_set_x, train_set_y, test_set_x, test_set_y,
              num_iterations=2000, learning_rate=0.005, print_cost=True)
    #example of a picture that was wrongly classified
    index=1
    plt.imshow(test_set_x[:,index].reshape((num_px, num_px,3)))
    plt.show()
    print('-'*50)
    print('-'*50)
    print ("y = " + str(test_set_y[0,index]) + ", you predicted that it is a \"" + classes[int(d["Y_prediction_test"][0,index])].decode("utf-8") +  "\" picture.")
    #plot the cost function 
    costs = np.squeeze(d['costs'])#Remove single-dimensional entries from the shape of an array.
    fig = plt.figure()
    costplot = fig.add_subplot(121)
    costplot.plot(costs)
    costplot.set_ylabel('cost')
    costplot.set_xlabel('iterations(per hundreds)')
    costplot.set_title('learning rate = '+str(d['learning_rate']))
    #for different learning rate
    learning_rates = [0.01, 0.001, 0.0001]
    models = {}
    for i in learning_rates:
        print('-'*50)
        print('learning rate is: '+str(i))
        models[str(i)] = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 2000, learning_rate = i, print_cost = False)
        print('\n'+'-'*50)
    plots = fig.add_subplot(122)
    for i in learning_rates:
        plots.plot(np.squeeze(models[str(i)]['costs']), label=str(models[str(i)]['learning_rate']))
    plots.set_ylabel('cost')
    plots.set_xlabel('iterations')
    legend = plots.legend(loc='upper center', shadow=False)
    plt.show()
    #Test with my own image
    my_image_path = glob.glob(os.path.join('./images', '*'))#list
    fig = plt.figure()
    number = 0
    for fname in my_image_path:
        number += 1
        image = np.array(ndimage.imread(fname, flatten=False))
        my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
        my_predicted_image = predict(d['w'],d['b'],my_image)
        if len(my_image_path)%4 == 0:
            imageshow_rows = int(len(my_image_path)/2)
        else:
            imageshow_rows = int(len(my_image_path)/2)+1
        imageplot = fig.add_subplot(imageshow_rows,2,number)
        imageplot.imshow(image)
        print('-'*50)
        print('y = '+str(np.squeeze(my_predicted_image))+' '+classes[int(np.squeeze(my_predicted_image)),].decode("utf-8"))
    plt.show()
