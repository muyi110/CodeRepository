#!/usr/bin/env python3
#此模块为主程序模块
import time
import logging
import platform
import threading
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
import numpy as np

from UI.MainFrame import MainFrame
from serial_set.serial_set import SerialSet
from data_processing.DoubleBufferQueue import DoubleBufferQueue
#from data_processing.BufferQueue import BufferQueue
from data_processing.DataParser import DataParserEEG, DataParserECG
from data_processing.Filter import ECGFilter

if platform.system() == "Windows":
    from serial.tools import list_ports
else:
    import glob
    import os
    import re

#配置日志的基本格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class Main(MainFrame):
    """主函数类"""
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master

        self._data_parse_complete_flag_eeg = False #数据解析完成标志
        self._data_parse_complete_flag_ecg = False #数据解析完成标志


        self.serial_listbox_eeg = list()   #返回一个空列表，存储USB设备名称
        self.serial_listbox_ecg = list()
        self.serial_listbox_gsr = list()

        self.delta_list = list()
        self.theta_list = list()
        self.lowalpha_list = list()
        self.highalpha_list = list()
        self.lowbeta_list = list()
        self.highbeta_list = list()
        self.lowgamma_list = list()
        self.midgamma_list = list()
        self.attention_list = list()
        self.meditation_list = list()
        self.raweeg_list = list()
        self.rawecg_list = list()
        self.rawecgTemp_list = list()
        self.rawecglowtemp_list = list()
        self.rawgsr_list = list()
        self.current_ten_eeg = 0
        self.current_raw_eeg = 0
        self.current_raw_ecg = 0
        self.current_raw_gsr = 0

        self.tabIndex = 0     #tabIndex=0: 脑波界面； tabIndex=1: 心电界面 tabIndex=2: 皮电界面
        self.find_all_devices()
        self.double_buffer = DoubleBufferQueue()
        #self.double_buffer = BufferQueue()
        self.dataParse_eeg = DataParserEEG()
        self.dataParse_ecg = DataParserECG()
        self.ecgfilter = ECGFilter()
        self.y_delta = [None]*500
        self.line_delta, = self.Delta_figure.plot(np.arange(0,500,1),self.y_delta,color = 'red')
        self.y_theta = [None]*500
        self.line_theta, = self.Theta_figure.plot(np.arange(0,500,1),self.y_theta,color = 'red')
        self.y_lowalpha = [None]*500
        self.line_lowalpha, = self.LowAlpha_figure.plot(np.arange(0,500,1),self.y_lowalpha,color = 'red')
        self.y_highalpha = [None]*500
        self.line_highalpha, = self.HighAlpha_figure.plot(np.arange(0,500,1),self.y_highalpha,color = 'red')
        self.y_lowbeta = [None]*500
        self.line_lowbeta, = self.LowBeta_figure.plot(np.arange(0,500,1),self.y_lowbeta,color = 'red')
        self.y_highbeta = [None]*500
        self.line_highbeta, = self.HighBeta_figure.plot(np.arange(0,500,1),self.y_highbeta,color = 'red')
        self.y_lowgamma = [None]*500
        self.line_lowgamma, = self.LowGamma_figure.plot(np.arange(0,500,1),self.y_lowgamma,color = 'red')
        self.y_midgamma = [None]*500
        self.line_midgamma, = self.MiddleGamma_figure.plot(np.arange(0,500,1),self.y_midgamma,color = 'red')

        self.y_eeg = [None]*1000
        self.line_eeg, = self.raw_eeg_figure.plot(np.arange(0,1000,1), self.y_eeg,color = 'red')
        self.y_ecg = [None]*1000
        self.line_ecg, = self.ecg_figure.plot(np.arange(0,1000,1), self.y_ecg,color = 'red')

    def find_all_devices(self):
        """线程检测连接设备的状态"""
        self.tabIndex = self.tabcontrol.index('current')  #获取当前的tab号
        #print(threading.active_count()) #获取程序运行线程数-------------------------------调试作用
        if self.tabIndex == 0:
            self.find_all_serial_devices_eeg()
        elif self.tabIndex == 1:
            self.find_all_serial_devices_ecg()
        elif self.tabIndex == 2:
            self.find_all_serial_devices_gsr()
        self.start_thread_timer(self.find_all_devices, 2)

    def find_all_serial_devices_eeg(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    temp_serial.append(strCom)
                for item in temp_serial:
                    if item not in self.serial_listbox_eeg:
                        self.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_eeg:
                    if item not in temp_serial:
                        size = self.eeg_frm_l_listbox.size()
                        index = list(self.eeg_frm_l_listbox.get(
                            0, size)).index(item)
                        self.eeg_frm_l_listbox.delete(index)
                self.serial_listbox_eeg = temp_serial

            elif platform.system() == "Linux":
                temp_serial = list()
                temp_serial = self.find_usb_tty()
                for item in temp_serial:
                    if item not in self.serial_listbox_eeg:
                        self.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_eeg:
                    if item not in temp_serial:
                        index = list(self.eeg_frm_l_listbox.get(
                            0, self.eeg_frm_l_listbox.size())).index(item)
                        self.eeg_frm_l_listbox.delete(index)
                self.serial_listbox_eeg = temp_serial
        except Exception as e:
            logging.error(e)

    def find_all_serial_devices_ecg(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    temp_serial.append(strCom)
                for item in temp_serial:
                    if item not in self.serial_listbox_ecg:
                        self.ecg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_ecg:
                    if item not in temp_serial:
                        size = self.ecg_frm_l_listbox.size()
                        index = list(self.ecg_frm_l_listbox.get(
                            0, size)).index(item)
                        self.ecg_frm_l_listbox.delete(index)
                self.serial_listbox_ecg = temp_serial

            elif platform.system() == "Linux":
                temp_serial = list()
                temp_serial = self.find_usb_tty()
                for item in temp_serial:
                    if item not in self.serial_listbox_ecg:
                        self.ecg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_ecg:
                    if item not in temp_serial:
                        index = list(self.ecg_frm_l_listbox.get(
                            0, self.ecg_frm_l_listbox.size())).index(item)
                        self.ecg_frm_l_listbox.delete(index)
                self.serial_listbox_ecg = temp_serial
        except Exception as e:
            logging.error(e)

    def find_all_serial_devices_gsr(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    temp_serial.append(strCom)
                for item in temp_serial:
                    if item not in self.serial_listbox_gsr:
                        self.gsr_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_gsr:
                    if item not in temp_serial:
                        size = self.gsr_frm_l_listbox.size()
                        index = list(self.gsr_frm_l_listbox.get(
                            0, size)).index(item)
                        self.gsr_frm_l_listbox.delete(index)
                self.serial_listbox_gsr = temp_serial

            elif platform.system() == "Linux":
                temp_serial = list()
                temp_serial = self.find_usb_tty()
                for item in temp_serial:
                    if item not in self.serial_listbox_gsr:
                        self.gsr_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_gsr:
                    if item not in temp_serial:
                        index = list(self.gsr_frm_l_listbox.get(
                            0, self.gsr_frm_l_listbox.size())).index(item)
                        self.gsr_frm_l_listbox.delete(index)
                self.serial_listbox_gsr = temp_serial
        except Exception as e:
            logging.error(e)

    def find_usb_tty(self, vendor_id=None, product_id=None):
        """查找Linux下的串口设备"""
        tty_devs = list()
        for dn in glob.glob('/sys/bus/usb/devices/*'):
            try:
                vid = int(open(os.path.join(dn, "idVendor")).read().strip(), 16)
                pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
                if ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)):
                    dns = glob.glob(os.path.join(
                        dn, os.path.basename(dn) + "*"))
                    for sdn in dns:
                        for fn in glob.glob(os.path.join(sdn, "*")):
                            if re.search(r"\/ttyUSB[0-9]+$", fn):
                                tty_devs.append(os.path.join(
                                    "/dev", os.path.basename(fn)))
            except Exception as ex:
                pass
        return tty_devs

    def start_thread_timer(self, callback, timer=1):
        """此线程用于查找USB设备"""
        temp_thread = threading.Timer(timer, callback)   #timer时间后，callback被调用
        temp_thread.setDaemon(True)                      #设置为守护线程
        temp_thread.start()

    def Toggle(self, event=None):
        """打开/关闭 设备，重写父类中的方法"""
        if self.tabIndex == 0:
            self.serial_toggle_eeg()
        elif self.tabIndex == 1:
            self.serial_toggle_ecg()
        elif self.tabIndex == 2:
            self.serial_toggle_gsr()

    def serial_toggle_eeg(self):
        """打开/关闭串口设备"""
        if self.eeg_left_btn["text"] == "Open":
            try:
                serial_index = self.eeg_frm_l_listbox.curselection() #获取当前选择的串口号
                if serial_index:
                    self.current_serial_str_eeg = self.eeg_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str_eeg = self.eeg_frm_l_listbox.get(
                        self.eeg_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str_eeg.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str_eeg
                self.baudrate = self.eeg_frm_left_combobox_baudrate.get()
                self.parity = "N"
                self.databit = "8"
                self.stopbit = "1"
                self.ser_eeg = SerialSet(Port=self.port,
                                        BaudRate=self.baudrate,
                                        ByteSize=self.databit,
                                        Parity=self.parity,
                                        Stopbits=self.stopbit)
                self.ser_eeg.on_connected_changed(self.serial_on_connected_changed_eeg)
            except Exception as e:
                logging.error(e)
                try:
                    self.eeg_status_label["text"] = "Open [{0}] Failed!".format(
                        self.current_serial_str_eeg)
                    self.eeg_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.eeg_left_btn["text"] == "Close":
            self.ser_eeg.disconnect()
            self.eeg_left_btn["text"] = "Open"
            self.eeg_left_btn["bg"] = "#008B8B"
            self.eeg_status_label["text"] = "Close Serial Successful!"
            self.eeg_left_btn["fg"] = "#8DEEEE"

    def serial_on_connected_changed_eeg(self, is_connected):
        """串口连接状态改变回调"""
        if is_connected:
            self.ser_eeg.connect()
            if self.ser_eeg._is_connected:
                self.eeg_status_label["text"] = "Open [{0}] Successful!".format(
                    self.current_serial_str_eeg)
                self.eeg_status_label["fg"] = "#66CD00"
                self.eeg_left_btn["text"] = "Close"
                self.eeg_left_btn["bg"] = "#F08080"
                self.ser_eeg.on_data_received(self.serial_on_data_received_eeg) #串口数据接收线程
                self.ser_eeg.on_data_received_parse(self.data_parse_eeg)#串口数据解析线程
            else:
                self.eeg_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str_eeg)
                self.eeg_status_label["fg"] = "#DC143C"
        else:
            self.ser_eeg.disconnect()
            self.eeg_left_btn["text"] = "Open"
            self.eeg_left_btn["bg"] = "#008B8B"
            self.eeg_status_label["text"] = "Close Serial Successful!"
            self.eeg_status_label["fg"] = "#8DEEEE"

    def serial_toggle_ecg(self):
        """打开/关闭串口设备"""
        if self.ecg_left_btn["text"] == "Open":
            try:
                serial_index = self.ecg_frm_l_listbox.curselection()
                if serial_index:
                    self.current_serial_str_ecg = self.ecg_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str_ecg = self.ecg_frm_l_listbox.get(
                        self.ecg_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str_ecg.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str_ecg
                self.baudrate = self.ecg_frm_left_combobox_baudrate.get()
                self.parity = "N"
                self.databit = "8"
                self.stopbit = "1"
                self.ser_ecg = SerialSet(Port=self.port,
                                        BaudRate=self.baudrate,
                                        ByteSize=self.databit,
                                        Parity=self.parity,
                                        Stopbits=self.stopbit)
                self.ser_ecg.on_connected_changed(self.serial_on_connected_changed_ecg)
            except Exception as e:
                logging.error(e)
                try:
                    self.ecg_status_label["text"] = "Open [{0}] Failed!".format(
                        self.current_serial_str_ecg)
                    self.ecg_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.ecg_left_btn["text"] == "Close":
            self.ser_ecg.disconnect()
            self.ecg_left_btn["text"] = "Open"
            self.ecg_left_btn["bg"] = "#008B8B"
            self.ecg_status_label["text"] = "Close Serial Successful!"
            self.ecg_left_btn["fg"] = "#8DEEEE"

    def serial_on_connected_changed_ecg(self, is_connected):
        """串口连接状态改变回调"""
        if is_connected:
            self.ser_ecg.connect()
            if self.ser_ecg._is_connected:
                self.ecg_status_label["text"] = "Open [{0}] Successful!".format(
                    self.current_serial_str_ecg)
                self.ecg_status_label["fg"] = "#66CD00"
                self.ecg_left_btn["text"] = "Close"
                self.ecg_left_btn["bg"] = "#F08080"
                self.ser_ecg.on_data_received(self.serial_on_data_received_ecg)
                self.ser_ecg.on_data_received_parse(self.data_parse_ecg)#串口数据解析线程
            else:
                self.ecg_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str_ecg)
                self.ecg_status_label["fg"] = "#DC143C"
        else:
            self.ser_ecg.disconnect()
            self.ecg_left_btn["text"] = "Open"
            self.ecg_left_btn["bg"] = "#008B8B"
            self.ecg_status_label["text"] = "Close Serial Successful!"
            self.ecg_status_label["fg"] = "#8DEEEE"

    def serial_toggle_gsr(self):
        """打开/关闭串口设备"""
        if self.gsr_left_btn["text"] == "Open":
            try:
                serial_index = self.gsr_frm_l_listbox.curselection()
                if serial_index:
                    self.current_serial_str_gsr = self.gsr_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str_gsr = self.gsr_frm_l_listbox.get(
                        self.gsr_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str_gsr.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str_gsr
                self.baudrate = self.gsr_frm_left_combobox_baudrate.get()
                self.parity = "N"
                self.databit = "8"
                self.stopbit = "1"
                self.ser_gsr = SerialSet(Port=self.port,
                                        BaudRate=self.baudrate,
                                        ByteSize=self.databit,
                                        Parity=self.parity,
                                        Stopbits=self.stopbit)
                self.ser_gsr.on_connected_changed(self.serial_on_connected_changed_gsr)
            except Exception as e:
                logging.error(e)
                try:
                    self.gsr_status_label["text"] = "Open [{0}] Failed!".format(
                        self.current_serial_str_gsr)
                    self.gsr_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.gsr_left_btn["text"] == "Close":
            self.ser_gsr.disconnect()
            self.gsr_left_btn["text"] = "Open"
            self.gsr_left_btn["bg"] = "#008B8B"
            self.gsr_status_label["text"] = "Close Serial Successful!"
            self.gsr_left_btn["fg"] = "#8DEEEE"

    def serial_on_connected_changed_gsr(self, is_connected):
        """串口连接状态改变回调"""
        if is_connected:
            self.ser_gsr.connect()
            if self.ser_gsr._is_connected:
                self.gsr_status_label["text"] = "Open [{0}] Successful!".format(
                    self.current_serial_str_gsr)
                self.gsr_status_label["fg"] = "#66CD00"
                self.gsr_left_btn["text"] = "Close"
                self.gsr_left_btn["bg"] = "#F08080"
                self.ser_gsr.on_data_received(self.serial_on_data_received_gsr)
                self.ser_gsr.on_data_received_parse(self.data_parse_gsr) #串口数据解析线程
            else:
                self.gsr_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str_gsr)
                self.gsr_status_label["fg"] = "#DC143C"
        else:
            self.ser_gsr.disconnect()
            self.gsr_left_btn["text"] = "Open"
            self.gsr_left_btn["bg"] = "#008B8B"
            self.gsr_status_label["text"] = "Close Serial Successful!"
            self.gsr_status_label["fg"] = "#8DEEEE"

    def serial_on_data_received_eeg(self, data):
        """串口接收数据"""
        for element in data:
            self.double_buffer.writer_eeg(element)
        self.ser_eeg._serial_received_data = True

    def serial_on_data_received_ecg(self, data):
        """串口接收数据"""
        for element in data:
            self.double_buffer.writer_ecg(element)
        self.ser_ecg._serial_received_data = True

    def serial_on_data_received_gsr(self, data):
        """串口接收数据"""
        pass

    def data_parse_eeg(self,data):
        """开始数据解析"""
        for element in self.double_buffer.reader_eeg():
            self.dataParse_eeg.parseByte(element)
        self.ser_eeg._serial_received_data = False
        self._data_parse_complete_flag_eeg = True

    def data_parse_ecg(self,data):
        for element in self.double_buffer.reader_ecg():
            self.dataParse_ecg.parseByte(element)
        self.ser_ecg._serial_received_data = False
        self._data_parse_complete_flag_ecg = True

    def data_parse_gsr(self,data):
        pass

    def eight_eeg_waveform_plot(self):
        temp_list = list()
        temp_list = self.dataParse_eeg.double_queue_parse_data_eeg.reader_ten_eeg()
        #画8种脑波窗口大小是500
        if (self.current_ten_eeg + len(temp_list)) > 500:
            #当最新取出的数据太多，只取最新的数据
            if len(temp_list) > 500:
                temp_list = temp_list[-500:]  #取最后500个数据
            originalIndex = self.current_ten_eeg
            self.current_ten_eeg = 474  #移出5%的空间(500x0.95-1)
            if self.current_ten_eeg > (500 - len(temp_list)):
                self.current_ten_eeg = 500 - len(temp_list)
            srcIndex = originalIndex - self.current_ten_eeg
            i = 0
            while i < srcIndex:              
                del self.delta_list[0]
                del self.theta_list[0]
                del self.lowalpha_list[0]
                del self.highalpha_list[0]
                del self.lowbeta_list[0]
                del self.highbeta_list[0]
                del self.lowgamma_list[0]
                del self.midgamma_list[0]
                del self.attention_list[0]
                del self.meditation_list[0]
                i = i + 1
        n = 0
        while n < len(temp_list):
            self.delta_list.append(temp_list[n]["delta"] / 30000)
            self.theta_list.append(temp_list[n]["theta"] / 15000)
            self.lowalpha_list.append(temp_list[n]["lowalpha"] / 4000)
            self.highalpha_list.append(temp_list[n]["highalpha"] / 3000)
            self.lowbeta_list.append(temp_list[n]["lowbeta"] / 2000)
            self.highbeta_list.append(temp_list[n]["highbeta"] / 2000)
            self.lowgamma_list.append(temp_list[n]["lowgamma"] / 1000)
            self.midgamma_list.append(temp_list[n]["midgamma"] / 700)
            self.attention_list.append(temp_list[n]["attention"])
            self.meditation_list.append(temp_list[n]["meditation"])
            self.current_ten_eeg += 1
            n = n + 1
        #下面开始触发画图
        self.draw_delta_eeg(self.delta_list)
        self.draw_theta_eeg(self.theta_list)
        self.draw_highalpha_eeg(self.highalpha_list)
        self.draw_lowbeta_eeg(self.lowbeta_list)
        self.draw_highbeta_eeg(self.highbeta_list)
        self.draw_lowgamma_eeg(self.lowgamma_list)
        self.draw_midgamma_eeg(self.midgamma_list)
        self.draw_lowalpha_eeg(self.lowalpha_list)

        self.wave_eeg.canvas_eeg.show()  #刷新绘图

    def draw_delta_eeg(self, kw):
        if len(kw) > 0:
            self.y_delta = kw[:]    #更新数据
            if len(self.y_delta) < 500:
                self.y_delta += [None]*(500 - len(self.y_delta))
            self.line_delta.set_ydata(self.y_delta)

    def draw_theta_eeg(self, kw):
        if len(kw) > 0:
            self.y_theta = kw[:]    #更新数据
            if len(self.y_theta) < 500:
                self.y_theta += [None]*(500 - len(self.y_theta))
            self.line_theta.set_ydata(self.y_theta)

    def draw_highalpha_eeg(self, kw):
         if len(kw) > 0:
            self.y_highalpha = kw[:]    #更新数据
            if len(self.y_highalpha) < 500:
                self.y_highalpha += [None]*(500 - len(self.y_highalpha))
            self.line_highalpha.set_ydata(self.y_highalpha)

    def draw_lowbeta_eeg(self, kw):
       if len(kw) > 0:
            self.y_lowbeta = kw[:]    #更新数据
            if len(self.y_lowbeta) < 500:
                self.y_lowbeta += [None]*(500 - len(self.y_lowbeta))
            self.line_lowbeta.set_ydata(self.y_lowbeta)


    def draw_highbeta_eeg(self, kw):
        if len(kw) > 0:
            self.y_highbeta = kw[:]    #更新数据
            if len(self.y_highbeta) < 500:
                self.y_highbeta += [None]*(500 - len(self.y_highbeta))
            self.line_highbeta.set_ydata(self.y_highbeta)


    def draw_lowgamma_eeg(self, kw):
        if len(kw) > 0:
            self.y_lowgamma = kw[:]    #更新数据
            if len(self.y_lowgamma) < 500:
                self.y_lowgamma += [None]*(500 - len(self.y_lowgamma))
            self.line_lowgamma.set_ydata(self.y_lowgamma)

    def draw_midgamma_eeg(self, kw):
        if len(kw) > 0:
            self.y_midgamma = kw[:]    #更新数据
            if len(self.y_midgamma) < 500:
                self.y_midgamma += [None]*(500 - len(self.y_midgamma))
            self.line_midgamma.set_ydata(self.y_midgamma)

    def draw_lowalpha_eeg(self, kw):
        if len(kw) > 0:
            self.y_lowalpha = kw[:]    #更新数据
            if len(self.y_lowalpha) < 500:
                self.y_lowalpha += [None]*(500 - len(self.y_lowalpha))
            self.line_lowalpha.set_ydata(self.y_lowalpha)

    def raw_eeg_waveform_plot(self):
        temp_list = list()
        temp_list = self.dataParse_eeg.double_queue_parse_data_eeg.reader_raw_eeg()
        #画原始脑波窗口大小是1000
        if (self.current_raw_eeg + len(temp_list)) > 1000:
            #当最新取出的数据太多，只取最新的数据
            if len(temp_list) > 1000:
                temp_list = temp_list[-1000:]  #取最后1000个数据
            originalIndex = self.current_raw_eeg
            self.current_raw_eeg = 949  #移出5%的空间(1000x0.95-1)
            if self.current_raw_eeg > (1000 - len(temp_list)):
                self.current_raw_eeg = 1000 - len(temp_list)
            srcIndex = originalIndex - self.current_raw_eeg
            i = 0
            while i < srcIndex:
                del self.raweeg_list[0]
                i = i + 1
        n = 0
        while n < len(temp_list):
            self.raweeg_list.append(temp_list[n] / 4)
            self.current_raw_eeg += 1
            n += 1
        #下面开始触发画图
        if len(self.raweeg_list) > 0:
            self.y_eeg = self.raweeg_list[:]    #更新数据
            if len(self.y_eeg) < 1000:
                self.y_eeg += [None]*(1000 - len(self.y_eeg))
            self.line_eeg.set_ydata(self.y_eeg)
            self.wave_raw_eeg.canvas_raweeg.show()  #刷新绘图

    def raw_ecg_waveform_plot(self):
        temp_list = list()
        temp_list = self.dataParse_ecg.double_queue_parse_data_ecg.reader_raw_ecg()
        #画原始心电窗口大小是1000
        if (self.current_raw_ecg + len(temp_list)) > 1000:
            #当最新取出的数据太多，只取最新的数据
            if len(temp_list) > 1000:
                temp_list = temp_list[-1000:]  #取最后1000个数据
            originalIndex = self.current_raw_ecg
            self.current_raw_ecg = 949  #移出5%的空间(1000x0.95-1)
            if self.current_raw_ecg > (1000 - len(temp_list)):
                self.current_raw_ecg = 1000 - len(temp_list)
            srcIndex = originalIndex - self.current_raw_ecg
            i = 0
            while i < srcIndex:               
                #self.rawecg_list[i] = self.rawecg_list[srcIndex]
                del self.rawecgTemp_list[0]
                #self.rawecglowtemp_list[i] = self.rawecglowtemp_list[srcIndex]
                i = i + 1
        n = 0
        while n < len(temp_list):
            #self.rawecg_list[self.current_raw_ecg] = temp_list[n] / 36
            self.rawecgTemp_list.append((temp_list[n] / 6)-62)
            self.current_raw_ecg = self.current_raw_ecg + 1
            n = n + 1
        #下面开始触发画图
        if len(self.rawecgTemp_list) > 0:
            self.y_ecg = self.rawecgTemp_list[:]    #更新数据
            if len(self.y_ecg) < 1000:
                self.y_ecg += [None]*(1000 - len(self.y_ecg))
            self.line_ecg.set_ydata(self.y_ecg)
            self.wave_ecg.canvas_ecg.show()  #刷新绘图
        #下面是心电数据滤波处理（可能有问题）
        #tempECGArry = list()
        #tempECGArry = self.rawecgTemp_list
        #arry = self.ecgfilter.filter(tempECGArry)
        #self.rawecg_list = arry
        #self.rawecglowtemp_list.clear()
        #i = 0
        #for element in self.rawecg_list:
        #    if element > -1500 and element < 0:
        #        element = element / 2
        #    if element > 0:
        #        element = element / 3
        #    self.rawecglowtemp_list.append(element)
        #    i = i + 1
        #averageArry1 = list()
        #averageArry1 = self.rawecglowtemp_list
        #averageArry = self.ecgfilter.averagefilter(N = 15, kw = averageArry1)
        #self.rawecg_list.clear()
        #t = 0
        #while t < len(averageArry):
        #    self.rawecg_list.append(averageArry[t])
        #    t = t + 1
        #下面开始触发画图
        #if len(self.rawecg_list) > 0:
        #    self.y_ecg = self.rawecg_list[:]    #更新数据
        #    if len(self.y_ecg) < 1000:
        #        self.y_ecg += [None]*(1000 - len(self.y_ecg))
        #    self.line_ecg.set_ydata(self.y_ecg)
        #    self.wave_ecg.canvas_ecg.show()  #刷新绘图

    def raw_gsr_waveform_plot(self):
        pass

    def eeg_siganl_plot(self):
        #下面是直接调用画图(如果效果不行，重新开个线程)
        if self._data_parse_complete_flag_eeg:
            if self.dataParse_eeg._flag_get_eeg_eight:
                self.eight_eeg_waveform_plot()
                self.dataParse_eeg._flag_get_eeg_eight = False
            self.raw_eeg_waveform_plot()
            self._data_parse_complete_flag_eeg = False
        self.root.after(20, self.eeg_siganl_plot)

    def ecg_siganl_plot(self):
        #下面是直接调用画图
        if self._data_parse_complete_flag_ecg:
            self.raw_ecg_waveform_plot()
            self._data_parse_complete_flag_ecg = False
        self.root.after(50, self.ecg_siganl_plot)



if __name__ == '__main__':
    root = tk.Tk()
    root.title('Physiological Data Visualization Software')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()

    style = ttk.Style()
    style.theme_create( "MyStyle", parent="clam", settings={
        "TNotebook.Tab": {"configure": {"padding": [50, 1] ,
        "background": "lightgrey", "foreground": "black", 
        "font":("Monaco", 14), 
        "activebackground": "blue", 
        "activeforeground": "white"},}})
    style.theme_use("MyStyle")
    app = Main(root)
    root.after(0, app.eeg_siganl_plot)
    root.after(0, app.ecg_siganl_plot)
    root.mainloop() 
