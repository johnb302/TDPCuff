import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import queue

class RealTimePlotter(object):
    def __init__(self, q):
        self.q = q
        self.app = pg.mkQApp("Sensor Plot")

        self.win = pg.GraphicsLayoutWidget(show=True, title="Sensor Plot")
        self.win.resize(1000,600)
        self.win.setWindowTitle('Live Plotter')

        pg.setConfigOptions(antialias=True)

        self.plot = self.win.addPlot(title='Real Time Plot')
        self.plot.showGrid(x=True, y=True)

        self.data = {}
        self.curves = {}

        self.ptr = {}
        self.stop_signal = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Refresh rate in ms

    def update(self):
        while not self.q.empty():
            try:
                sensorname, data = self.q.get(block=False)

                if sensorname == "STOP":
                    self.stop_signal += 1
                    if self.stop_signal == 3: self.timer.stop() #QtGui.QApplication.instance().quit()
                    continue

                if sensorname not in self.data:
                    self.data[sensorname] = np.zeros(1000)  # Start with 1000 zeros
                    self.curves[sensorname] = self.plot.plot(pen=pg.mkPen(color=(np.random.randint(0,255), 
                                                                                 np.random.randint(0,255), np.random.randint(0,255)), 
                                                                                 width=2))
                    self.ptr[sensorname] = 0

                # Shift data in the array one sample left
                self.data[sensorname][:-1] = self.data[sensorname][1:]  
                # Append the new value
                self.data[sensorname][-1] = data  

                self.curves[sensorname].setData(self.data[sensorname])
                self.curves[sensorname].setPos(self.ptr[sensorname], 0)
                self.ptr[sensorname] += 1

            except queue.Empty:
                pass

    def start(self):
        self.app.exec()
