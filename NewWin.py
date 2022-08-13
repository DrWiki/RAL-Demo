import argparse
from collections import deque
from time import perf_counter

import numpy as np
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
import pyqtgraph as pg
import pyqtgraph.functions as fn
import pyqtgraph.parametertree as ptree
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.Parameter import PARAM_TYPES
from pyqtgraph.parametertree.parameterTypes import GroupParameter
import threading
import Control
import sys
import PyQt5
import socket
import pandas as pd
import Universaltool.TransLogic.udp_logic as UDP
import Universaltool.TransLogic.Serial_logic as SER
import Universaltool.TransLogic.tcp_logic as TCP
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import time
import ctypes
import inspect
import Metadata
import struct
import pyqtgraph as pg
import binascii
import numpy as np

app = pg.mkQApp("Plot Speed Test")

class NewWin(QtWidgets.QWidget,UDP.UdpLogic, TCP.TcpLogic, SER.PyQt_Serial):
    def __init__(self):
        super(WinLogic, self).__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(update)
        self.timer.start(0)
    def update(self):
        pass

    def create(self):
        self.docker_Terminal = Dock("Terminal", size=(1, 1))
        self.docker_Receive = Dock("Recieve", size=(500, 300), closable=True)
        self.area = DockArea()
        self.area.addDock(self.docker_Terminal,'left')  ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
        self.area.addDock(self.docker_Receive, 'right')  ## place d2 at right edge of dock area
        self.w1 = pg.LayoutWidget()
        self.label = QtWidgets.QLabel(""" -- DockArea Example -- 
        This window has 6 Dock widgets in it. Each dock can be dragged
        by its title bar to occupy a different space within the window 
        but note that one dock has its title bar hidden). Additionally,
        the borders between docks may be dragged to resize. Docks that are dragged on top
        of one another are stacked in a tabbed layout. Double-click a dock title
        bar to place it in its own window.
        """)
        self.saveBtn = QtWidgets.QPushButton('Save dock state')
        self.restoreBtn = QtWidgets.QPushButton('Restore dock state')
        self.restoreBtn.setEnabled(False)
        self.w1.addWidget(self.label, row=0, col=0)

        self.w1.addWidget(saveBtn, row=1, col=0)
        self.w1.addWidget(restoreBtn, row=2, col=0)
        self.docker_Terminal.addWidget(self.w1)

        self.w5 = pg.ImageView()
        self.w5.setImage(np.random.normal(size=(100, 100)))
        self.docker_Receive.addWidget(self.w5)
        self.splitter = QtWidgets.QSplitter(1)

        self.cy = QtWidgets.QHBoxLayout(self)
        # win2 = QtWidgets.QWidget()
        self.horizontalLayout_3 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.params = ptree.Parameter.create(name='Parameters', type='group', children=self.children)
        self.pt = ptree.ParameterTree(showHeader=False)
        self.pt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.area.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pt.setParameters(params)
        self.pw = pg.PlotWidget()

        self.horizontalLayout_3.addWidget(self.pt)
        self.horizontalLayout_3.addWidget(self.area)
        self.cy.addLayout(horizontalLayout_3)
        self.cy.addWidget(pw)

        self.cy.setStretch(0, 0)
        self.cy.setStretch(1, 2)
        self.horizontalLayout_3.setStretch(0, 0)
        self.horizontalLayout_3.setStretch(1, 2)
        # win2.setLayout(horizontalLayout_3)
        # splitter.addWidget(win2)
        # splitter.show()
        # cy.addWidget(splitter)
        # win.show()

    def chile(self):
        self.children = [
            dict(name='TCP', title='TCP', type='group', children=[
                dict(name='Server', type='bool', value=True),
                dict(name='Server IP', type='str', value="0.0.0.0"),
                dict(name='Server PORT', type='int', limits=[0, 65535], value=8080),
                dict(name='Client', type='list', limits=["0.0.0.0"], value="0.0.0.0"),
            ]),
            dict(name='UDP', title='UDP', type='group', children=[
                dict(name='A IP', type='str', value="0.0.0.0"),
                dict(name='A PORT', type='int', limits=[0, 65535], value=8080),
                dict(name='B IP', type='str', value="0.0.0.0"),
                dict(name='B PORT', type='int', limits=[0, 65535], value=8080),

            ]),
            dict(name='Serial', title='Serial', type='group', children=[
                dict(name='COM', type='list', limits=["COMX"], value="COMX"),
                dict(name='BAUD RATE', type='int', limits=["9600", "115200"], value="115200"),
            ]),
            dict(name='File', title='File', type='group', children=[
                Parameter.create(name=f'Choose', type='action'),
                dict(name='Path', type='str', value="temp.csv"),
            ])
        ]
        return children
    def CONNECT(self):
        pass

    def run(self):
        self.show()


# don't limit frame rate to vsync
# sfmt = QtGui.QSurfaceFormat()
# sfmt.setSwapInterval(0)
# QtGui.QSurfaceFormat.setDefaultFormat(sfmt)
#
# class MonkeyCurveItem(pg.PlotCurveItem):
#     def __init__(self, *args, **kwds):
#         super().__init__(*args, **kwds)
#         self.monkey_mode = ''
#
#     def setMethod(self, param, value):
#         self.monkey_mode = value
#
#     def paint(self, painter, opt, widget):
#         if self.monkey_mode not in ['drawPolyline']:
#             return super().paint(painter, opt, widget)
#
#         painter.setRenderHint(painter.RenderHint.Antialiasing, self.opts['antialias'])
#         painter.setPen(pg.mkPen(self.opts['pen']))
#
#         if self.monkey_mode == 'drawPolyline':
#             painter.drawPolyline(fn.arrayToQPolygonF(self.xData, self.yData))

# default_pen = pg.mkPen()



# btn = Parameter.create(name=f'{name} All', type='action')
# btn.sigActivated.connect(activate)


# pw.setWindowTitle('pyqtgraph example: PlotSpeedTest')
# pw.setLabel('bottom', 'Index', units='B')
# curve = MonkeyCurveItem(pen=default_pen, brush='b')
# pw.addItem(curve)
# rollingAverageSize = 1000
# elapsed = deque(maxlen=rollingAverageSize)
#
# def resetTimings(*args):
#     elapsed.clear()
#
# def makeData(*args):
#     global data, connect_array, ptr
#     sigopts = params.child('sigopts')
#     nsamples = sigopts['nsamples']
#     frames = sigopts['frames']
#     Fs = sigopts['fsample']
#     A = sigopts['amplitude']
#     F = sigopts['frequency']
#     ttt = np.arange(frames * nsamples, dtype=np.float64) / Fs
#     data = A*np.sin(2*np.pi*F*ttt).reshape((frames, nsamples))
#     if sigopts['noise']:
#         data += np.random.normal(size=data.shape)
#     connect_array = np.ones(data.shape[-1], dtype=bool)
#     ptr = 0
#     pw.setRange(QtCore.QRectF(0, -10, nsamples, 20))
#
# def onUseOpenGLChanged(param, enable):
#     pw.useOpenGL(enable)
#
# def onEnableExperimentalChanged(param, enable):
#     pg.setConfigOption('enableExperimental', enable)
#
# def onPenChanged(param, pen):
#     curve.setPen(pen)
#
# def onFillChanged(param, enable):
#     curve.setFillLevel(0.0 if enable else None)
#
# def onSegmentedLineModeChanged(param, mode):
#     curve.setSegmentedLineMode(mode)

# params.child('sigopts').sigTreeStateChanged.connect(makeData)
# params.child('useOpenGL').sigValueChanged.connect(onUseOpenGLChanged)
# params.child('enableExperimental').sigValueChanged.connect(onEnableExperimentalChanged)
# params.child('pen').sigValueChanged.connect(onPenChanged)
# params.child('fill').sigValueChanged.connect(onFillChanged)
# params.child('plotMethod').sigValueChanged.connect(curve.setMethod)
# params.child('segmentedLineMode').sigValueChanged.connect(onSegmentedLineModeChanged)
# params.sigTreeStateChanged.connect(resetTimings)

# makeData()

fpsLastUpdate = perf_counter()
def update():
    global curve, data, ptr, elapsed, fpsLastUpdate

    options = ['antialias', 'connect', 'skipFiniteCheck']
    kwds = { k : params[k] for k in options }
    if kwds['connect'] == 'array':
        kwds['connect'] = connect_array

    # Measure
    t_start = perf_counter()
    curve.setData(data[ptr], **kwds)
    app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents)
    t_end = perf_counter()
    elapsed.append(t_end - t_start)
    ptr = (ptr + 1) % data.shape[0]

    # update fps at most once every 0.2 secs
    if t_end - fpsLastUpdate > 0.2:
        fpsLastUpdate = t_end
        average = np.mean(elapsed)
        fps = 1 / average
        pw.setTitle('%0.2f fps - %0.1f ms avg' % (fps, average * 1_000))



if __name__ == '__main__':
    pg.exec()
