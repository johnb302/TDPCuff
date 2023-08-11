#Libraries
from arduino import *
from plotter import *
import multiprocessing as mp

def openArduino(barrier, name, port, dqueue, baudrate = 115200):
    ard = Arduino(port, baudrate, name, dqueue)
    ard.read(barrier)
    return

def startPlotter(dqueue,colors):
    plotter = RealTimePlotter(dqueue,colors)
    plotter.start()
    return

if __name__ == "__main__":

    sensorColors = {
        'R4': (255,0,0),
        'R5': (132,5,5),
        'R6': (202,112,112),
        'G4': (0,255,0),
        'G5': (5,132,5),
        'G6': (112,202,112),
        'B4': (0,0,255),
        'B5': (5,5,132),
        'B6': (77,115,153)
    }

    sensor_barrier = mp.Barrier(3)
    dataQueue = mp.Queue()

    ports = ["COM18", "COM19", "COM20"]
    names = ["B", "R", "G"]

    ard_processes = [mp.Process(target=openArduino, args=(sensor_barrier, 
                        names[i], ports[i], dataQueue)) for i in range(len(ports))]
    ard_processes.append(mp.Process(target = startPlotter, args=(dataQueue, sensorColors,)))

    for p in ard_processes:
        p.start()

    for process in ard_processes:
        process.join()

    print("Acquisition Finished!")
