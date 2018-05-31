import numpy
import operator

def createDataSet():
    '''创建数据集'''
    group = numpy.array([[1.0, 1.1],[0, 0],[0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
