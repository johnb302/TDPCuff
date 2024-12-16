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
    emptyQueue = mp.Queue()

    ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"]
    names = ["B", "R", "G", "Cuff"]

    # Instantiate 3 arduinos for data acquisition
    arduino_instances = [Arduino(ports[i], 115200, names[i], dataQueue, True) for i in range(3)]
    # Instantiate another arduino for cuff pressurization
    arduino_instances.append(Arduino(ports[3], 9600, names[3], emptyQueue, False))

    # ard_processes = [mp.Process(target=openArduino, args=(sensor_barrier, 
    #                      names[i], ports[i], dataQueue)) for i in range(len(ports))]
    ard_processes = [mp.Process(target = arduino_instances[i].read, args=(sensor_barrier,)) for i in range(len(ports))]
    ard_processes.append(mp.Process(target = startPlotter, args=(dataQueue, sensorColors)))

    process_manager.set_instances(arduino_instances)

    for p in ard_processes:
        p.start()

    while stop_Flag.value != 4:
        continue

    for arduino in range(5):
        ard_processes[arduino].terminate()
        print('Joining Arduino...')
        ard_processes[arduino].join()

    print("Acquisition Finished!")
