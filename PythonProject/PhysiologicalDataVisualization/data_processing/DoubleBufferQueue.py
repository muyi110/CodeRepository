#此模块为双缓冲模块，用于数据处理，采用两个list实现
import threading
import queue

class BufferQueue():
    """采用自带的Queue模块"""
    def __init__(self, maxsize=2048):
        self.queue_eeg = Queue(maxsize)
        self.queue_ecg = Queue(maxsize)
        self.queue_gsr = Queue(maxsize)

    def writer_eeg(self, data):
        self.queue_eeg.put(data, block=1)

    def writer_ecg(self, data):
        self.queue_ecg.put(data, block=1)
    
    def writer_gsr(self, data):
        self.queue_gsr.put(data, block=1)

    def reader_eeg(self):
        temp = self.queue_eeg.get(block=1)
        queue_eeg.task_done()
        return temp
    
    def reader_eeg(self):
        temp = self.queue_ecg.get(block=1)
        queue_ecg.task_done()
        return temp

    def reader_eeg(self):
        temp = self.queue_gsr.get(block=1)
        queue_gsr.task_done()
        return temp

class DoubleBufferQueue():
    """双缓存实现"""
    def __init__(self):
        #脑电
        self.eeg_list = list()
        self.eeg_list0 = list()
        self.eeg_list1 = list()
        #心电
        self.ecg_list = list()
        self.ecg_list0 = list()
        self.ecg_list1 = list()
        #皮肤电
        self.gsr_list = list()
        self.gsr_list0 = list()
        self.gsr_list1 = list()

        self.eeg_list = self.eeg_list0
        self.ecg_list = self.ecg_list0
        self.gsr_list = self.gsr_list0
        self._flag_eeg = True   #_flag = True: list指向list0;    否则指向list1
        self._flag_ecg = True
        self._flag_gsr = True

    def writer_eeg(self, data):
        lock_eeg = threading.Lock()
        lock_eeg.acquire()
        try:
            self.eeg_list.append(data)
        finally:
            lock_eeg.release()     #释放锁

    def writer_ecg(self, data):
        lock_ecg = threading.Lock()
        lock_ecg.acquire()
        try:
            self.ecg_list.append(data)
        finally:
            lock_ecg.release()     #释放锁

    def writer_gsr(self, data):
        lock_gsr = threading.Lock()
        lock_gsr.acquire()
        try:
            self.gsr_list.append(data)
        finally:
            lock_gsr.release()     #释放锁

    def reader_eeg(self):
        lock_eeg_ = threading.Lock()
        lock_eeg_.acquire()
        try:
            temp_list = self.eeg_list[:]
            if self._flag_eeg:
                self.eeg_list = self.eeg_list1
                self.eeg_list0.clear()
                self._flag_eeg = False
            else:
                self.eeg_list = self.eeg_list0
                self.eeg_list1.clear()
                self._flag_eeg = True
        finally:
            lock_eeg_.release()
        return temp_list

    def reader_ecg(self):
        lock_ecg_ = threading.Lock()
        lock_ecg_.acquire()
        try:
            temp_list = self.ecg_list[:]
            if self._flag_ecg:
                self.ecg_list = self.ecg_list1
                self.ecg_list0.clear()
                self._flag_ecg = False
            else:
                self.ecg_list = self.ecg_list0
                self.ecg_list1.clear()
                self._flag_ecg = True
        finally:
            lock_ecg_.release()
        return temp_list

    def reader_gsr(self):
        lock_gsr_ = threading.Lock()
        lock_gsr_.acquire()
        try:
            temp_list = self.gsr_list[:]
            if self._flag_gsr:
                self.gsr_list = self.gsr_list1
                self.gsr_list0.clear()
                self._flag_gsr = False
            else:
                self.gsr_list = self.gsr_list0
                self.gsr_list1.clear()
                self._flag_gsr = True
        finally:
            lock_gsr_.release()
        return temp_list

class DoubleBufferQueue_ParseData_eeg():
    """双缓存实现"""
    def __init__(self):
        #8种脑电波加注意力和冥想
        self.ten_eeg_list = list()
        self.ten_eeg_list0 = list()
        self.ten_eeg_list1 = list()
        #原始脑电波
        self.raw_eeg_list = list()
        self.raw_eeg_list0 = list()
        self.raw_eeg_list1 = list()

        self.ten_eeg_list = self.ten_eeg_list0
        self.raw_eeg_list = self.raw_eeg_list0
        self._flag_ten_eeg = True   #_flag = True: list指向list0;    否则指向list1
        self._flag_raw_eeg = True

    def writer_ten_eeg(self, data):
        lock_ten_eeg = threading.Lock()
        lock_ten_eeg.acquire()
        try:
            self.ten_eeg_list.append(data)
        finally:
            lock_ten_eeg.release()     #释放锁

    def writer_raw_eeg(self, data):
        lock_raw_eeg = threading.Lock()
        lock_raw_eeg.acquire()
        try:
            self.raw_eeg_list.append(data)
        finally:
            lock_raw_eeg.release()     #释放锁

    def reader_ten_eeg(self):
        lock_ten_eeg_ = threading.Lock()
        lock_ten_eeg_.acquire()
        try:
            temp_list = self.ten_eeg_list[:]
            if self._flag_ten_eeg:
                self.ten_eeg_list = self.ten_eeg_list1
                self.ten_eeg_list0.clear()
                self._flag_ten_eeg = False
            else:
                self.ten_eeg_list = self.ten_eeg_list0
                self.ten_eeg_list1.clear()
                self._flag_ten_eeg = True
        finally:
            lock_ten_eeg_.release()
        return temp_list

    def reader_raw_eeg(self):
        lock_raw_eeg_ = threading.Lock()
        lock_raw_eeg_.acquire()
        try:
            temp_list = self.raw_eeg_list[:]
            if self._flag_raw_eeg:
                self.raw_eeg_list = self.raw_eeg_list1
                self.raw_eeg_list0.clear()
                self._flag_raw_eeg = False
            else:
                self.raw_eeg_list = self.raw_eeg_list0
                self.raw_eeg_list1.clear()
                self._flag_raw_eeg = True
        finally:
            lock_raw_eeg_.release()
        return temp_list

class DoubleBufferQueue_ParseData_ecg():
    """双缓存实现"""
    def __init__(self):
        #原始心电信号
        self.raw_ecg_list = list()
        self.raw_ecg_list0 = list()
        self.raw_ecg_list1 = list()
        #心率值
        self.heartValue_list = list()
        self.heartValue_list0 = list()
        self.heartValue_list1 = list()

        self.raw_ecg_list = self.raw_ecg_list0
        self.heartValue_list = self.heartValue_list0
        self._flag_raw_ecg = True  #_flag = True: list指向list0;    否则指向list1
        self._flag_heartValue = True

    def writer_raw_ecg(self, data):
        lock_raw_ecg = threading.Lock()
        lock_raw_ecg.acquire()
        try:
            self.raw_ecg_list.append(data)
        finally:
            lock_raw_ecg.release()     #释放锁

    def writer_heartValue(self, data):
        lock_heartValue = threading.Lock()
        lock_heartValue.acquire()
        try:
            self.heartValue_list.append(data)
        finally:
            lock_heartValue.release()     #释放锁

    def reader_raw_ecg(self):
        lock_raw_ecg_ = threading.Lock()
        lock_raw_ecg_.acquire()
        try:
            temp_list = self.raw_ecg_list[:]
            if self._flag_raw_ecg:
                self.raw_ecg_list = self.raw_ecg_list1
                self.raw_ecg_list0.clear()
                self._flag_raw_ecg = False
            else:
                self.raw_ecg_list = self.raw_ecg_list0
                self.raw_ecg_list1.clear()
                self._flag_raw_ecg = True
        finally:
            lock_raw_ecg_.release()
        return temp_list

    def reader_heartValue(self):
        lock_heartValue_ = threading.Lock()
        lock_heartValue_.acquire()
        try:
            temp_list = self.heartValue_list[:]
            if self._flag_heartValue:
                self.heartValue_list = self.heartValue_list1
                self.heartValue_list0.clear()
                self._flag_heartValue = False
            else:
                self.heartValue_list = self.heartValue_list0
                self.rheartValue_list1.clear()
                self._flag_heartValue = True
        finally:
            lock_heartValue_.release()
        return temp_list