import os
import numpy
import operator

def createDataSet():
    '''创建数据集'''
    group = numpy.array([[1.0, 1.1],[1.0, 1.0],[0, 0],[0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
 
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDisIndicies = distances.argsort()
    classCount = dict()
    for i in range(k):
        voteIlabel = labels[sortedDisIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1),\
                              reverse=True)
    return sortedClassCount[0][0]

def file_to_matrix(filename):
    with open(filename) as fr:
        arrayOLines = fr.readlines()
        numberOfLines = len(arrayOLines)
        returnMat = numpy.zeros((numberOfLines, 3))
        classLabelVector = list()
        index = 0
        for line in arrayOLines:
            line = line.strip()                 #remove the leading and tailing whitespace 
            listFromLine = line.split('\t')     #return a list
            returnMat[index, :] = listFromLine[0:3]
            classLabelVector.append(int(listFromLine[-1]))
            index += 1
        return returnMat, classLabelVector

def autoNorm(dataSet):
    '''Normalize the data'''
    minValue = dataSet.min(axis=0)
    maxValue = dataSet.max(axis=0)
    ranges = maxValue - minValue
    normDataSet = numpy.zeros(dataSet.shape)
    m = dataSet.shape[0]
    normDataSet = dataSet - numpy.tile(minValue, (m, 1))
    normDataSet = normDataSet / numpy.tile(ranges, (m, 1))
    return normDataSet, ranges, minValue

def datingClassTest(k):
    hoRatio = 0.1       # Test samples's ratio
    datingDataMat, datingLabels = file_to_matrix('datingTestSet2.txt')
    normMat, ranges, minValue = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], k)
        print('The classifier came back with: %d, the real answer is: %d' % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print('The total error rate is: %f' % (errorCount/float(numTestVecs)))

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input('percentage of time spent playing video games:'))
    ffMailes = float(input('frequent flier miles earned per year:'))
    iceCream = float(input('liters of ice cream consumed per year:'))
    datingDataMat, datingLabels = file_to_matrix('datingTestSet2.txt')
    normMat, ranges, minValue = autoNorm(datingDataMat)
    inArr = numpy.array([ffMailes, percentTats, iceCream])
    classifierResult = classify0((inArr-minValue)/ranges, normMat, datingLabels, 3)
    print('you will probably like this person: ', resultList[classifierResult - 1])

def img_to_vector(filename):
    returnVect = numpy.zeros((1,1024))
    with open(filename) as fr:
        for i in range(32):
            lineStr = fr.readline()
            for j in range(32):
                returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest(k):
    hwLabels = list()
    trainingFileList = os.listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = numpy.zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img_to_vector('trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img_to_vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, k)
        print('The classifier came back with: %d, the real answer is: %d' % (classifierResult, classNumStr))
        if classifierResult != classNumStr :
            errorCount += 1.0
    print('\nthe total number of errors is: %d' % errorCount)
    print('the total error rate is: %f' % (errorCount / float(mTest)))

