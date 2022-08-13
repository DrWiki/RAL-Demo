#!/usr/bin/python
"""
Update a simple plot as rapidly as possible to measure speed.
"""

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

# don't limit frame rate to vsync
sfmt = QtGui.QSurfaceFormat()
sfmt.setSwapInterval(0)
QtGui.QSurfaceFormat.setDefaultFormat(sfmt)

class MonkeyCurveItem(pg.PlotCurveItem):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.monkey_mode = ''

    def setMethod(self, param, value):
        self.monkey_mode = value

    def paint(self, painter, opt, widget):
        if self.monkey_mode not in ['drawPolyline']:
            return super().paint(painter, opt, widget)

        painter.setRenderHint(painter.RenderHint.Antialiasing, self.opts['antialias'])
        painter.setPen(pg.mkPen(self.opts['pen']))

        if self.monkey_mode == 'drawPolyline':
            painter.drawPolyline(fn.arrayToQPolygonF(self.xData, self.yData))

app = pg.mkQApp("Plot Speed Test")
default_pen = pg.mkPen()



# btn = Parameter.create(name=f'{name} All', type='action')
# btn.sigActivated.connect(activate)
children = [
    dict(name='TCP', title='TCP', type='group', children=[
        dict(name='Server', type='bool', value=True),
        dict(name='Server IP', type='str',  value="0.0.0.0"),
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
        dict(name='COM', type='list', limits=["COMX"],value="COMX"),
        dict(name='BAUD RATE', type='int', limits=["9600","115200"], value="115200"),
    ]),
    dict(name='File', title='File', type='group', children=[
        Parameter.create(name=f'Choose', type='action'),
        dict(name='Path', type='str', value="temp.csv"),
    ])
]
d1 = Dock("Dock1", size=(1, 1))     ## give this dock the minimum possible size
d2 = Dock("Dock2 - Console", size=(500,300), closable=True)
area = DockArea()
area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'right')     ## place d2 at right edge of dock area
w1 = pg.LayoutWidget()
label = QtWidgets.QLabel(""" -- DockArea Example -- 
This window has 6 Dock widgets in it. Each dock can be dragged
by its title bar to occupy a different space within the window 
but note that one dock has its title bar hidden). Additionally,
the borders between docks may be dragged to resize. Docks that are dragged on top
of one another are stacked in a tabbed layout. Double-click a dock title
bar to place it in its own window.
""")
saveBtn = QtWidgets.QPushButton('Save dock state')
restoreBtn = QtWidgets.QPushButton('Restore dock state')
restoreBtn.setEnabled(False)
w1.addWidget(label, row=0, col=0)

w1.addWidget(saveBtn, row=1, col=0)
w1.addWidget(restoreBtn, row=2, col=0)
d1.addWidget(w1)

w5 = pg.ImageView()
w5.setImage(np.random.normal(size=(100,100)))
d2.addWidget(w5)
splitter = QtWidgets.QSplitter(1)
# splitter = QtWidgets.QSplitter(1)

win = QtWidgets.QWidget()
cy = QtWidgets.QFrame()
# win2 = QtWidgets.QWidget()
horizontalLayout_3 = QtWidgets.QVBoxLayout()
horizontalLayout_3.setObjectName("horizontalLayout_3")

params = ptree.Parameter.create(name='Parameters', type='group', children=children)
pt = ptree.ParameterTree(showHeader=False)
pt.setParameters(params)
pw = pg.PlotWidget()

horizontalLayout_3.addWidget(pt)
horizontalLayout_3.addWidget(area)
cy.setLayout(horizontalLayout_3)
splitter.addWidget(cy)

splitter.addWidget(pw)
horizontalLayout_3.setStretch(0, 0)
horizontalLayout_3.setStretch(1, 2)
# win2.setLayout(horizontalLayout_3)
# splitter.addWidget(win2)
# splitter.show()
# cy.addWidget(splitter)
win.show()

pw.setWindowTitle('pyqtgraph example: PlotSpeedTest')
pw.setLabel('bottom', 'Index', units='B')
curve = MonkeyCurveItem(pen=default_pen, brush='b')
pw.addItem(curve)
rollingAverageSize = 1000
elapsed = deque(maxlen=rollingAverageSize)

def resetTimings(*args):
    elapsed.clear()

def makeData(*args):
    global data, connect_array, ptr
    sigopts = params.child('sigopts')
    nsamples = sigopts['nsamples']
    frames = sigopts['frames']
    Fs = sigopts['fsample']
    A = sigopts['amplitude']
    F = sigopts['frequency']
    ttt = np.arange(frames * nsamples, dtype=np.float64) / Fs
    data = A*np.sin(2*np.pi*F*ttt).reshape((frames, nsamples))
    if sigopts['noise']:
        data += np.random.normal(size=data.shape)
    connect_array = np.ones(data.shape[-1], dtype=bool)
    ptr = 0
    pw.setRange(QtCore.QRectF(0, -10, nsamples, 20))

def onUseOpenGLChanged(param, enable):
    pw.useOpenGL(enable)

def onEnableExperimentalChanged(param, enable):
    pg.setConfigOption('enableExperimental', enable)

def onPenChanged(param, pen):
    curve.setPen(pen)

def onFillChanged(param, enable):
    curve.setFillLevel(0.0 if enable else None)

def onSegmentedLineModeChanged(param, mode):
    curve.setSegmentedLineMode(mode)

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

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    pg.exec()
