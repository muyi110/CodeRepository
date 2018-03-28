#此模块为心电信号滤波器算法实现(整系数滤波)

class ECGFilter():
    def __init__(self):
        pass

    def filter(self, *kw):
        filterResult = list()
        filter1 = list()
        filter2 = list()
        filter3 = list()
        filter4 = list()
        length = len(kw)

        i = 0
        while i < length:
            if i == 0:
                filter1[i] = kw[i]
            elif i > 0 and i < 120:
                filter1[i] = filter1[i-1] + kw[i]
            else:
                filter1[i] = filter1[i-1] + kw[i] - kw[i-120]
            i = i + 1
        j = 0
        while j < length:
            if j == 0:
                filter2[j] = filter1[j]
            elif j > 0 and j < 120:
                filter2[j] = filter2[j-1] + filter1[j]
            else:
                filter2[j] = filter2[j-1] + filter1[j] - filter1[j - 120]
            j = j + 1
        m = 0
        while m < length:
            filter3[m] = filter2[m] / (120 * 120)
            m = m + 1
        #初始化filter4
        num = 0
        while num < length:
            filter4[num] = 0
            num = num + 1
        n = 0
        while n < length:
            if n > 119 or n == 119:
                filter4[n] = kw[n - 119]
            n = n + 1
        t = 0
        while t < length:
            filterResult[t] = filter4[t] - filter3[t]
            t = t + 1
        return filterResult

    def averagefilter(self, N, *kw):
        averagefilterResult = list()
        Sum = 0
        i = 0
        while i < len(kw):
            j = 0
            while j < N:
                if i >= j:
                    Sum = Sum + kw[i - j]
                j = j + 1
            averagefilterResult[i] = Sum / N
            Sum = 0
            i = i + 1
        return averagefilterResult