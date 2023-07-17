#Libraries
from arduino import *
import multiprocessing as mp


if __name__ == "__main__":

    #initial_barrier = mp.Barrier(3)
    sensor_barrier = mp.Barrier(3)

    arduino_ports = ["COM3", "COM5", "COM9"]

    helper_processes = []

    a = Arduino(115200,'COM3')
    a.read()
    #for _ in range(2):
        #helper_processes.append(mp.Process(target = ))

    #ard_processes = [mp.Process(target=openArduino, args=(sensor_barrier, port)) for port in arduino_ports]

    #for p in ard_processes:
        #p.start()

    #for process in ard_processes:
        #process.join()
