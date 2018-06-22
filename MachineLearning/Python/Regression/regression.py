#!/usr/bin/env python3
import numpy
import matplotlib.pyplot as plt
# The algorithm is off-line

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat = list()
    labelMat = list()
    with open(fileName) as fr:
        for line in fr:
            lineArr = list()
            curLine = line.strip().split('\t')
            for i in range(numFeat):
                lineArr.append(float(curLine[i]))
            dataMat.append(lineArr)
            labelMat.append(float(curLine[-1]))
    return dataMat, labelMat

def standRegres(xArr, yArr):
    xMat = numpy.mat(xArr)
    yMat = numpy.mat(yArr).T
    xTx = xMat.T * xMat
    if numpy.linalg.det(xTx) == 0.0:
        print('This matrix is singular, cannot do inverse')
        return
    ws = xTx.I * (xMat.T * yMat)
    return ws

# The function below is Locally Weighted Linear Regression(LWLR)

def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat = numpy.mat(xArr)
    yMat = numpy.mat(yArr).T
    m = numpy.shape(xMat)[0]
    weights = numpy.mat(numpy.eye(m))
    for j in range(m):
        diffMat = testPoint - xMat[j,:]
        weights[j,j] = numpy.exp(diffMat * (diffMat.T) / (-2.0*k**2))
    xTx = xMat.T * weights * xMat
    if numpy.linalg.det(xTx) == 0.0:
        print('This matrix is singular, cannot do inverse')
        return
    ws = xTx.I * (xMat.T * weights * yMat)
    return testPoint * ws

def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = numpy.shape(testArr)[0]
    yHat = numpy.zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

def standPlot(fig, xArr, yArr):
    ws = standRegres(xArr, yArr)
    xMat = numpy.mat(xArr)
    yMat = numpy.mat(yArr)
    yHat = xMat * ws
    print('Correlation coefficient between yEstimate and yActual:')
    print(numpy.corrcoef(yHat.T, yMat))
    ax = fig.add_subplot(221)
    ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])
    xCopy = xMat.copy()
    xCopy.sort(axis=0)
    yHat = xCopy * ws
    ax.set_title('standRegression')
    ax.plot(xCopy[:,1], yHat)

def lwlrPlot(fig, xArr, yArr):
    yHat_1 = lwlrTest(xArr, xArr, yArr, 1.0)
    yHat_2 = lwlrTest(xArr, xArr, yArr, 0.01)
    yHat_3 = lwlrTest(xArr, xArr, yArr, 0.003)
    xMat = numpy.mat(xArr)
    yMat = numpy.mat(yArr)
    strInd = xMat[:,1].argsort(axis=0)
    xSort = xMat[strInd][:,0,:]
    ax_lwlr_1 = fig.add_subplot(222)
    ax_lwlr_2 = fig.add_subplot(223)
    ax_lwlr_3 = fig.add_subplot(224)
    ax_lwlr_1.plot(xSort[:,1], yHat_1[strInd])
    ax_lwlr_2.plot(xSort[:,1], yHat_2[strInd])
    ax_lwlr_3.plot(xSort[:,1], yHat_3[strInd])
    ax_lwlr_1.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0], s=2, c='red')
    ax_lwlr_2.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0], s=2, c='red')
    ax_lwlr_3.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0], s=2, c='red')
    ax_lwlr_1.set_title('LWLR for k=1.0')
    ax_lwlr_2.set_title('LWLR for k=0.01')
    ax_lwlr_3.set_title('LWLR for k=0.03')

if __name__ == '__main__':
    xArr, yArr = loadDataSet('ex0.txt')
    fig = plt.figure()
    standPlot(fig, xArr, yArr)
    lwlrPlot(fig, xArr, yArr)
    plt.show()

    print(globals())
