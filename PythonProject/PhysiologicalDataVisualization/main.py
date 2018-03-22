#此模块为主程序模块
import time
import logging
import platform
import threading
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk

from UI.MainFrame import MainFrame
from serial_set.serial_set import SerialSet

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

        self.serial_listbox = list()   #返回一个空列表，存储USB设备名称
        self.find_all_devices()
        self.main_frame = MainFrame(self.root)

    def find_all_devices(self):
        """线程检测连接设备的状态"""
        self.find_all_serial_devices()
        self.start_thread_timer(self.find_all_devices, 1)

    def find_all_serial_devices(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.main_frame.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        size = self.main_frame.eeg_frm_l_listbox.size()
                        index = list(self.main_frame.eeg_frm_l_listbox.get(
                            0, size)).index(item)
                        self.main_frame.eeg_frm_l_listbox.delete(index)

                self.serial_listbox = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.main_frame.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        index = list(self.main_frame.eeg_frm_l_listbox.get(
                            0, self.main_frame.eeg_frm_l_listbox.size())).index(item)
                        self.main_frame.eeg_frm_l_listbox.delete(index)
                self.serial_listbox = self.temp_serial
        except Exception as e:
            logging.error(e)