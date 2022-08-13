from PyQt5 import QtCore, QtWidgets


class Signals():
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_write_msg = QtCore.pyqtSignal(str)
    signal_NewClientAdded = QtCore.pyqtSignal(tuple)
    signal_NewDataComing = QtCore.pyqtSignal(str)
    signal_PackedDataComing = QtCore.pyqtSignal(bytes)
    signal_trigerthread = QtCore.pyqtSignal(int)

    def __init__(self):
        self.connect()

    def connect(self):
        self.signal_write_msg.connect(self.write_msg)
        self.signal_NewClientAdded.connect(self.NewClient)

    def NewClient(self,dp):

        return
    def write_msg(self, msg):
        # signal_write_msg信号会触发这个函数
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的
        :return: None
        """
        return
