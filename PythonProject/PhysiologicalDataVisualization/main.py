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
from data_processing.DoubleBufferQueue import DoubleBufferQueue
#from data_processing.BufferQueue import BufferQueue
from data_processing.DataParser import DataParserEEG, DataParserECG

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

        self.serial_listbox_eeg = list()   #返回一个空列表，存储USB设备名称
        self.serial_listbox_ecg = list()
        self.serial_listbox_gsr = list()
        self.find_all_devices()
        self.tabIndex = 0     #tabIndex=0: 脑波界面； tabIndex=1: 心电界面 tabIndex=2: 皮电界面
        self.double_buffer = DoubleBufferQueue()
        #self.double_buffer = BufferQueue()
        self.dataParse_eeg = DataParserEEG()
        self.dataParse_ecg = DataParserECG()

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
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox_eeg:
                        self.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_eeg:
                    if item not in self.temp_serial:
                        size = self.eeg_frm_l_listbox.size()
                        index = list(self.eeg_frm_l_listbox.get(
                            0, size)).index(item)
                        self.eeg_frm_l_listbox.delete(index)
                self.serial_listbox_eeg = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox_eeg:
                        self.eeg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_eeg:
                    if item not in self.temp_serial:
                        index = list(self.eeg_frm_l_listbox.get(
                            0, self.eeg_frm_l_listbox.size())).index(item)
                        self.eeg_frm_l_listbox.delete(index)
                self.serial_listbox_eeg = self.temp_serial
        except Exception as e:
            logging.error(e)

    def find_all_serial_devices_ecg(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox_ecg:
                        self.ecg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_ecg:
                    if item not in self.temp_serial:
                        size = self.ecg_frm_l_listbox.size()
                        index = list(self.ecg_frm_l_listbox.get(
                            0, size)).index(item)
                        self.ecg_frm_l_listbox.delete(index)
                self.serial_listbox_ecg = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox_ecg:
                        self.ecg_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_ecg:
                    if item not in self.temp_serial:
                        index = list(self.ecg_frm_l_listbox.get(
                            0, self.ecg_frm_l_listbox.size())).index(item)
                        self.ecg_frm_l_listbox.delete(index)
                self.serial_listbox_ecg = self.temp_serial
        except Exception as e:
            logging.error(e)

    def find_all_serial_devices_gsr(self):
        """检查串口设备"""
        try:
            if platform.system() == "Windows":
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox_gsr:
                        self.gsr_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_gsr:
                    if item not in self.temp_serial:
                        size = self.gsr_frm_l_listbox.size()
                        index = list(self.gsr_frm_l_listbox.get(
                            0, size)).index(item)
                        self.gsr_frm_l_listbox.delete(index)
                self.serial_listbox_gsr = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox_gsr:
                        self.gsr_frm_l_listbox.insert("end", item)
                for item in self.serial_listbox_gsr:
                    if item not in self.temp_serial:
                        index = list(self.gsr_frm_l_listbox.get(
                            0, self.gsr_frm_l_listbox.size())).index(item)
                        self.gsr_frm_l_listbox.delete(index)
                self.serial_listbox_gsr = self.temp_serial
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
                    self.current_serial_str = self.eeg_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str = self.eeg_frm_l_listbox.get(
                        self.eeg_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str
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
                        self.current_serial_str)
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
                    self.current_serial_str)
                self.eeg_status_label["fg"] = "#66CD00"
                self.eeg_left_btn["text"] = "Close"
                self.eeg_left_btn["bg"] = "#F08080"
                self.ser_eeg.on_data_received(self.serial_on_data_received_eeg) #串口数据接收线程
                self.ser_eeg.on_data_received_parse(self.data_parse_eeg)#串口数据解析线程
            else:
                self.eeg_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str)
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
                    self.current_serial_str = self.ecg_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str = self.ecg_frm_l_listbox.get(
                        self.ecg_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str
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
                        self.current_serial_str)
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
                    self.current_serial_str)
                self.ecg_status_label["fg"] = "#66CD00"
                self.ecg_left_btn["text"] = "Close"
                self.ecg_left_btn["bg"] = "#F08080"
                self.ser_ecg.on_data_received(self.serial_on_data_received_ecg)
                self.ser_ecg.on_data_received_parse(self.data_parse_ecg)#串口数据解析线程
            else:
                self.ecg_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str)
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
                    self.current_serial_str = self.gsr_frm_l_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str = self.gsr_frm_l_listbox.get(
                        self.gsr_frm_l_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str
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
                        self.current_serial_str)
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
                    self.current_serial_str)
                self.gsr_status_label["fg"] = "#66CD00"
                self.gsr_left_btn["text"] = "Close"
                self.gsr_left_btn["bg"] = "#F08080"
                self.ser_gsr.on_data_received(self.serial_on_data_received_gsr)
                self.ser_gsr.on_data_received_parse(self.data_parse_gsr) #串口数据解析线程
            else:
                self.gsr_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str)
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

    def data_parse_eeg(self):
        """开始数据解析"""
        for element in self.double_buffer.reader_eeg():
            self.dataParse_eeg.parseByte(data)
        self.ser_eeg._serial_received_data = False

    def data_parse_ecg(self):
        for element in self.double_buffer.reader_ecg():
            self.dataParse_ecg.parseByte(data)
        self.ser_ecg._serial_received_data = False

    def data_parse_gsr(self):
        pass



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

    Main(root)

    root.mainloop() 