#Libraries
from arduino import *
import multiprocessing as mp

def start_aq(barrier):
    barrier.wait()

if __name__ == "__main__":

    initial_barrier = mp.Barrier(3)
    sensor_barrier = mp.Barrier(3)

    arduino_ports = ["COM3", "COM5", "COM9"]
    arduinos = [Arduino(port) for port in arduino_ports]

    helper_processes = []
    #for _ in range(2):
        #helper_processes.append(mp.Process(target = ))

    ard_processes = [mp.Process(target=arduino.read, args=(sensor_barrier, )) for arduino in range(len(arduinos))]

    #for p in processes:
        #p.start()

    #for process in processes:
        #process.join()

    

        