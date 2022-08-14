# -*- coding: utf-8 -*-
import binascii
import re
from PyQt5.QtSerialPort import QSerialPort
from PyQt5 import QtCore
import Signal


class PyQt_Serial(Signal.Signals):
    # signal_write_msg = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ser_com = QSerialPort()
        self.ser_sendCount = 0
        self.ser_receiveCount = 0
        self.ser_encoding = 'utf-8'  # 'gbk'
        self.ser_HEXSEND = False
        self.ser_HEXSHOW = False
        self.ser_NAME = "COM1"
        self.ser_BAUDRATE = 115200

    def on_openSerial(self):
        self.ser_com.setPortName(self.ser_NAME)
        if self.ser_com.open(QSerialPort.ReadWrite) == False:
            self.signal_write_msg.emit('开串口失败')
        else:
            self.ser_com.setBaudRate(self.ser_BAUDRATE)
            self.ser_com.readyRead.connect(self.on_receiveData)  # 接收数据
            self.signal_write_msg.emit('开启串口 波特率是：'+str(self.ser_BAUDRATE))

    def on_closeSerial(self):
        self.ser_com.close()

    def on_sendData(self, txData):
        if self.ser_HEXSEND:
            s = txData.replace(' ', '')
            if len(s) % 2 == 1:  # 如果16进制不是偶数个字符,去掉最后一个
                self.signal_write_msg.emit('十六进制数不是偶数个')
                return

            if not s.isalnum():
                self.signal_write_msg.emit('包含非十六进制数')
                return

            try:
                hexData = binascii.a2b_hex(s)
            except:
                self.signal_write_msg.emit('转换出错')
                return

            try:
                n = self.com.write(hexData)
            except:
                self.signal_write_msg.emit('发送出错')
                return
        else:
            n = self.ser_com.write(txData.encode(self.ser_encoding, "ignore"))
        self.ser_sendCount += n

    def on_receiveData(self):
        receivedData = None
        try:
            '''将串口接收到的QByteArray格式数据转为bytes,并用gkb或utf8解码'''
            receivedData = bytes(self.ser_com.readAll())
        except:
            self.signal_write_msg.emit('接收出错')

        if len(receivedData) > 0:

            self.signal_PackedDataComing.emit(receivedData[0:20])

            self.ser_receiveCount += len(receivedData)
            if self.ser_HEXSHOW == False:
                receivedData = receivedData.decode(self.ser_encoding, 'ignore')
                # data_list = re.findall(r"\d+.*\d+", receivedData)
                self.signal_write_msg.emit(receivedData)
                self.signal_NewDataComing.emit(receivedData)

            else:
                data = binascii.b2a_hex(receivedData).decode('ascii')
                pattern = re.compile('.{2,2}')
                hexStr = (' '.join(pattern.findall(data)) + ' ').upper()
                self.signal_write_msg.emit(hexStr)
                self.signal_NewDataComing.emit(hexStr)

