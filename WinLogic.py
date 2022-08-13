import WinLayout
import sys
import time
from time import perf_counter
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import pyqtgraph as pg
import torch
from scipy.signal import butter, lfilter, freqz
import torch.nn.functional as F
# import CNN1DTool.Braille.models as models

labeldict = {
    "0": "Silk-flat",
    "1": "Silk-cir4",
    "2": "Silk-cir6",
    "3": "Silk-tri4",
    "4": "Silk-tri6",
    "5": "Paper-flat",
    "6": "Paper-cir4",
    "7": "Paper-cir6",
    "8": "Paper-tri4",
    "9": "Paper-tri6",
    "10": "Acrylic",
    "11": "Bakelite",
    "12": "Carbon_fiber",
    "13": "Epoxy_plate",
    "14": "Marble",
    "15": "Leather",
    "16": "Nylon",
    "17": "Glass",
    "18": "Resin",
    "19": "Wood"
}

class WinLogic(WinLayout.WinLayout):
    def __init__(self, parent=None):
        super(WinLogic, self).__init__(parent)
        self.CONNECT()
        self.th0 = threading.Thread(target=self.update0)
        self.th1 = threading.Thread(target=self.update1)
        self.CNN1D = None
        self.Loadnet()


        ###################################
        self.nSamples = 200

        # self.plot0 = pg.plot()
        self.plot0.setWindowTitle('thumb')
        self.curves0 = []
        for i in range(4):
            self.curve = pg.PlotCurveItem(pen=({'color': (i, 4), 'width': 2}))
            self.plot0.addItem(self.curve)
            self.curves0.append(self.curve)
        self.plot0.setYRange(-120, 120)
        self.plot0.setXRange(0, self.nSamples)


        self.plot1.setWindowTitle('forefinger')
        self.curves1 = []
        for i in range(4):
            self.curve = pg.PlotCurveItem(pen=({'color': (i, 4), 'width': 2}))
            self.plot1.addItem(self.curve)
            self.curves1.append(self.curve)
        self.plot1.setYRange(-120, 120)
        self.plot1.setXRange(0, self.nSamples)

        self.plot2 = pg.plot()
        self.plot2.setWindowTitle('middle finger')
        self.curves2 = []
        for i in range(4):
            self.curve = pg.PlotCurveItem(pen=({'color': (i, 4), 'width': 2}))
            self.plot2.addItem(self.curve)
            self.curves2.append(self.curve)
        self.plot2.setYRange(-120, 120)
        self.plot2.setXRange(0, self.nSamples)

        self.plot3 = pg.plot()
        self.plot3.setWindowTitle('ring finger')
        self.curves3 = []
        for i in range(4):
            self.curve = pg.PlotCurveItem(pen=({'color': (i, 4), 'width': 2}))
            self.plot3.addItem(self.curve)
            self.curves3.append(self.curve)
        self.plot3.setYRange(-120, 120)
        self.plot3.setXRange(0, self.nSamples)

        self.plot4 = pg.plot()
        self.plot4.setWindowTitle('little finger')
        self.curves4 = []
        for i in range(4):
            self.curve = pg.PlotCurveItem(pen=({'color': (i, 4), 'width': 2}))
            self.plot4.addItem(self.curve)
            self.curves4.append(self.curve)
        self.plot4.setYRange(-120, 120)
        self.plot4.setXRange(0, self.nSamples)

        self.timer0 = QtCore.QTimer()
        self.timer0.timeout.connect(self.update0)
        self.timer0.start(0)

        # self.count = 0


    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y  # Filter requirements.

    def lowpass(self, data):
        return self.butter_lowpass_filter(data, 50, 200, order=5)

    def Loadnet(self):
        self.CNN1D = torch.load("./res/models/100GAS4.pth", map_location=torch.device('cpu'))
        print(self.CNN1D)

    def predict(self, li):
        li = li.reshape((1,1,1400))
        li = li.astype(np.float32)
        output = self.CNN1D(torch.from_numpy(li))

        temp = li
        for i in range(16):
            temp = np.concatenate((temp,li), axis=0)
        output = self.CNN1D(torch.from_numpy(temp))

        ans = F.log_softmax(output, dim=1).argmax(dim=1).detach().numpy()[0]
        self.PB.setText(labeldict[str(ans)])
        return

    def CONNECT(self):
        # self.MyCB.signal_NewDataComing.connect(self.ProcessData)
        self.MyCB.signal_trigerthread.connect(self.triger)

    def triger(self, flag):
        if flag==1:
            self.th0.start()
            # self.th1.start()

        if flag==4:
            self.th0.start()
            # self.th1.start()

    #一张画布：200Hz
    #二张画布：160Hz
    #三张画布：90Hz
    #四张画布：85Hz
    def update0(self):
        if self.MyCB.metadata.datareadyX == True:
            self.MyCB.metadata.datareadyX = False
            self.curves0[0].setData([x[0] for x in self.MyCB.metadata.DataStreamX[-self.nSamples-1:-1]])
            self.curves0[1].setData([x[1] for x in self.MyCB.metadata.DataStreamX[-self.nSamples-1:-1]])
            self.curves0[2].setData([x[2] for x in self.MyCB.metadata.DataStreamX[-self.nSamples - 1:-1]])
            self.curves0[3].setData([x[3] for x in self.MyCB.metadata.DataStreamX[-self.nSamples - 1:-1]])
        while not self.MyCB.metadata.datareadyX:
            pg.QtGui.QApplication.processEvents()

        if self.MyCB.metadata.datareadyY == True:
            self.MyCB.metadata.datareadyY = False
            self.curves1[0].setData([x[0] for x in self.MyCB.metadata.DataStreamY[-self.nSamples - 1:-1]])
            self.curves1[1].setData([x[1] for x in self.MyCB.metadata.DataStreamY[-self.nSamples - 1:-1]])
            self.curves1[2].setData([x[2] for x in self.MyCB.metadata.DataStreamY[-self.nSamples - 1:-1]])
            self.curves1[3].setData([x[3] for x in self.MyCB.metadata.DataStreamY[-self.nSamples - 1:-1]])
        while not self.MyCB.metadata.datareadyY:
            pg.QtGui.QApplication.processEvents()

        if self.MyCB.metadata.datareadyZ == True:
            self.MyCB.metadata.datareadyZ = False
            self.curves2[0].setData([x[0] for x in self.MyCB.metadata.DataStreamZ[-self.nSamples - 1:-1]])
            self.curves2[1].setData([x[1] for x in self.MyCB.metadata.DataStreamZ[-self.nSamples - 1:-1]])
            self.curves2[2].setData([x[2] for x in self.MyCB.metadata.DataStreamZ[-self.nSamples - 1:-1]])
            self.curves2[3].setData([x[3] for x in self.MyCB.metadata.DataStreamZ[-self.nSamples - 1:-1]])
        while not self.MyCB.metadata.datareadyZ:
            pg.QtGui.QApplication.processEvents()

        if self.MyCB.metadata.datareadyRX == True:
            self.MyCB.metadata.datareadyRX = False
            self.curves3[0].setData([x[0] for x in self.MyCB.metadata.DataStreamRX[-self.nSamples - 1:-1]])
            self.curves3[1].setData([x[1] for x in self.MyCB.metadata.DataStreamRX[-self.nSamples - 1:-1]])
            self.curves3[2].setData([x[2] for x in self.MyCB.metadata.DataStreamRX[-self.nSamples - 1:-1]])
            self.curves3[3].setData([x[3] for x in self.MyCB.metadata.DataStreamRX[-self.nSamples - 1:-1]])
        while not self.MyCB.metadata.datareadyRX:
            pg.QtGui.QApplication.processEvents()

        if self.MyCB.metadata.datareadyRY == True:
            self.MyCB.metadata.datareadyRY = False
            self.curves4[0].setData([x[0] for x in self.MyCB.metadata.DataStreamRY[-self.nSamples - 1:-1]])
            self.curves4[1].setData([x[1] for x in self.MyCB.metadata.DataStreamRY[-self.nSamples - 1:-1]])
            self.curves4[2].setData([x[2] for x in self.MyCB.metadata.DataStreamRY[-self.nSamples - 1:-1]])
            self.curves4[3].setData([x[3] for x in self.MyCB.metadata.DataStreamRY[-self.nSamples - 1:-1]])
        while not self.MyCB.metadata.datareadyRY:
            pg.QtGui.QApplication.processEvents()
        # now = perf_counter()
        # self.count = self.count + 1
        # print(self.count)
        # print(now)

    def update1(self):
        if self.MyCB.metadata.datareadyY == True:
            self.MyCB.metadata.datareadyY = False
            self.curve1.setData(np.array(self.MyCB.metadata.DataStreamY[-self.nSamples - 1:-1]))
            # self.curve2.setData(np.array(self.MyCB.metadata.DataStreamX[-self.nSamples - 1:-1]))
        while not self.MyCB.metadata.datareadyY:
            pg.QtGui.QApplication.processEvents()



if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    app = pg.mkQApp("Flowchart Example")
    # app.setAttribute(QtCore.Qt.AA_Use96Dpi)
    mainWindow = WinLogic()
    mainWindow.show()
    pg.exec()
    # sys.exit(app.exec_())
