import time
from datetime import datetime
import serial

class Arduino:
    #Initilizer
    #Establish Serial Connection
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.serial = serial.Serial(port, baudrate) #115200
        self.run = True

    def read(self, barrier):
        while self.run:
            # Get the current time
            now = datetime.now()
            time_string = now.strftime("%H:%M:%S:%f")
            self.serial.write(b'A4\n')  # Request reading from A4
            value_A4 = float(self.serial.readline().decode().strip())
            barrier.wait()
            print(f'{value_A4}')
            print(time_string)
            #self.serial.write(b'A5\n')  # Request reading from A5
            #value_A5 = float(self.serial.readline().decode().strip())
            #barrier.wait()
            #self.serial.write(b'A6\n')  # Request reading from A6
            #value_A6 = float(self.serial.readline().decode().strip())
            #barrier.wait()
            time.sleep(0.001) # delay: 1 ms

    def stop(self):
        self.run = False