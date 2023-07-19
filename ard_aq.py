#Libraries
from arduino import *
from plotter import *
import multiprocessing as mp

def openArduino(barrier, name, port, dqueue, baudrate = 115200):
    ard = Arduino(port, baudrate, name, dqueue)
    ard.read(barrier)

def startPlotter():
    plotter = Plotter()
    plotter.plot()

if __name__ == "__main__":

    #initial_barrier = mp.Barrier(3)
    sensor_barrier = mp.Barrier(3)
    dataQueue = mp.Queue()

    ports = ["COM3", "COM5", "COM9"]
    names = ["G", "B", "R"]

    ard_processes = [mp.Process(target=openArduino, args=(sensor_barrier, 
                        names[i], ports[i], dataQueue)) for i in range(len(ports))]
    #ard_processes.append(mp.Process(target = startPlotter, args=()))

    for p in ard_processes:
        p.start()

    for process in ard_processes:
        process.join()
