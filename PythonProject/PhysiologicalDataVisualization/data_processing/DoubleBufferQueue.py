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