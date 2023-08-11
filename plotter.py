import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import queue
from PyQt6.QtGui import QFont

class RealTimePlotter(object):
    def __init__(self, q, colors):
        self.q = q
        self.colors = colors
        self.app = pg.mkQApp("Sensor Plot")
        self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()

        self.win = pg.GraphicsLayoutWidget(show=True, title="Sensor Plot")
        self.win.resize(1000,600)
        self.win.setWindowTitle('Live Plotter')
        self.win.setBackground('w')
    
        self.view.pg.setConfigOptions(antialias=True)

        self.plot = self.win.addPlot(title='Real Time Plot')
        self.plot.showGrid(x=False, y=False)
        self.plot.setYRange(0,0.25)
        self.plot.enableAutoRange('y', False)

        self.tick_font = QFont()
        self.tick_font.setPointSize(18)
        self.tick_font.setBold(True)  # Set tick font to bold

        # Customize the x-axis
        self.x_axis = self.plot.getAxis('bottom')
        self.x_axis.setPen(pg.mkPen(color='k', width=3))
        self.x_axis.setLabel('# of Sensor Readings', **{'font-size': '24pt'})
        self.x_axis.setStyle(tickFont=self.tick_font)

        # Customize the y-axis
        self.y_axis = self.plot.getAxis('left')
        self.y_axis.setPen(pg.mkPen(color='k', width=3))
        self.y_axis.setLabel('Voltage (volts)', **{'font-size': '24pt'})
        self.y_axis.setStyle(tickFont=self.tick_font)

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
                    if self.stop_signal == 3: self.timer.stop()
                    continue

                if sensorname not in self.data:
                    self.data[sensorname] = np.zeros(1000)  # Start with 1000 zeros using NumPy array
                    self.curves[sensorname] = self.plot.plot(pen=pg.mkPen(
                        color=(self.colors[sensorname]), width=2))
                    self.ptr[sensorname] = 0

                self.data[sensorname] = np.append(self.data[sensorname], data)

                self.curves[sensorname].setData(self.data[sensorname])
                # Update the X range to show the most recent 1000 data points
                self.plot.setXRange(max(0, len(self.data[sensorname]) - 1000), len(self.data[sensorname]))

                self.ptr[sensorname] += 1

            except queue.Empty:
                pass

    def start(self):
        self.app.exec()