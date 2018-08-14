#此模块为串口通信配置模块#

import sys
import time
import serial
import logging
import binascii
import platform
import threading

if platform.system == "Windows":
    from serial.tool import list_ports
else:
    import glob
    import os
    import re

class SerialSet():
    def __init__(self, Port="COM6", BaudRate="57600", ByteSize="8", Parity="N", Stopbits="1"):
        """初始化一些串口参数"""
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        
        self._serial = None
        self._is_connected = False
        self._is_serial_exist = True
        self._serial_received_data = False

    def connect(self, timeout = 1):
        """连接设备,超时等待时间1S"""
        self._serial = serial.Serial()
        self._serial.port = self.port
        self._serial.baudrate = self.baudrate
        self._serial.bytesize = int(self.bytesize)
        self._serial.parity = self.parity
        self._serial.stopbits = int(self.stopbits)
        self._serial.timeout = timeout

        try:
            self._serial.open()
            if self._serial.isOpen():
                self._is_connected = True
        except Exception as e:
            self._is_connected = False
            logging.error(e)  #在控制台上输出错误信息

    def disconnect(self):
        """断开设备"""
        if self._serial:
            self._serial.close()

    def on_connected_changed(self, func):
        """串口状态改变回调函数"""
        tConnected = threading.Thread(target=self._on_connected_changed, args=(func, ))
        tConnected.setDaemon(True)  #守护线程
        tConnected.start()

    def _on_connected_changed(self, func):
        """串口状态改变回调函数"""
        self._is_connected_temp = False
        while True:   #死循环，保证线程一直运行
            if self._is_serial_exist:
                if platform.system() == "Windows":
                    for com in list_ports.comports():
                        if com[0] == self.port:
                            self._is_connected = True
                            break
                elif platform.system() == "Linux":
                    if self.port in self.find_usb_tty():
                        self._is_connected = True
                if self._is_connected_temp != self._is_connected:
                    func(self._is_connected)
                self._is_connected_temp = self._is_connected
                time.sleep(1)
            else:
                break

    def on_data_received(self, func):
        """串口收到数据回调函数"""
        tDataReceived = threading.Thread(target=self._on_data_received, args=(func, ))
        tDataReceived.setDaemon(True)
        tDataReceived.start()

    def _on_data_received(self, func):                #当串口关闭时，此线程会结束
        """串口收到数据回调函数"""
        while True:
            if self._is_connected:
                try:
                    number = self._serial.inWaiting() #返回接受缓冲中字节数
                    if number > 0:
                        data = self._serial.read(number)
                        if data:
                            func(data)
                    time.sleep(0.01)
                except Exception:
                    self._is_connected = False
                    self._is_serial_exist = False
                    self._serial = None
                    break
    def on_data_received_parse(self, func):
        """数据解析线程"""
        tDataParse = threading.Thread(target=self._on_data_received_parse, args=(func, ))
        tDataParse.setDaemon(True)
        tDataParse.start()

    def _on_data_received_parse(self, func):
        while True:
            if self._is_serial_exist:
                if self._serial_received_data:   #判断串口是否收到数据
                    try:
                        func(1)
                        time.sleep(0.01)
                    except Exception:
                        self._serial_received_data = False
                time.sleep(0.01)
            else:
                break

    def find_usb_tty(self, vendor_id=None, product_id=None):
        """查找Linux下的串口设备"""
        tty_devs = list()
        for dn in glob.glob("/sys/bus/usb/devices/*"):
            try:
                vid = int(open(os.path.join(dn, "idVendor")).read().strip(), 16)
                pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
                if ((vendor_id is None) or (vid ==vendor_id)) and ((product_id is None) or (pid == product_id)):
                    dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                    for sdn in dns:
                        for fn in glob.glob(os.path.join(sdn, "*")):
                            if re.search(r"\/ttyUSB[0-9]+$", fn):
                                tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        for an in glob.glob('/sys/class/tty/*'):
                            if re.search(r"\/ttyACM[0-9]+$", an):
                                if os.path.join("/dev", os.path.basename(an)) in tty_devs:
                                    continue
                                tty_devs.append(os.path.join("/dev", os.path.basename(an)))                            
            except Exception:
                pass
        return tty_devs

#下面为串口模块测试#
if __name__ == "__main__":
    myserial = SerialSet()
    usbcom = myserial.find_usb_tty()
    print(usbcom[0])
    newserial = SerialSet(usbcom[0])
    newserial.connect()
    if newserial._is_connected:
        print("open")
