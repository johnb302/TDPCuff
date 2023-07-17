#Libraries
import numpy as np
import pyqtgraph as pg
from arduino import *
import multiprocessing as mp
from pyqtgraph.Qt import QtGui, QtCore

def testConcurrency(barrier):
    current_time = datetime.datetime.now().strftime('%H:%M:%S:%f')
    barrier.wait()
    print(current_time[:-3])

if __name__ == "__main__":

    barrier = mp.Barrier(3)
    arduino_ports = ["COM3", "COM5", "COM9"]

    processes = [mp.Process(target=testConcurrency, args=(barrier,)) for _ in range(len(arduino_ports))]

    for p in processes:
        p.start()

    for process in processes:
        process.join()

    

        