import time
from datetime import datetime
import serial

class Arduino:
    #Initilizer
    #Establish Serial Connection
    def __init__(self, port, baudrate, name):
        self.serial = serial.Serial(port, baudrate, timeout= 10)
        print(f'Arduino Connected!')
        self.name = name
        self.run = True

    def read(self, barrier):
        print(f'{self.name} preparing to run...')
        while self.run:
            # Get the current time
            now = datetime.now()
            time_string = now.strftime("%H:%M:%S:%f")
            self.serial.write(b'A4\n')  # Request reading from A4
            line4 = self.serial.read_until(expected=b'\n').decode().strip()
            #value_A4 = float(line)
            print(f"-{self.name}4-{time_string}T: {line4}")
            barrier.wait()
            self.serial.write(b'A5\n') #A5 Reading
            line5 = self.serial.read_until(expected=b'\n').decode().strip()
            #value_A5 = float(line)
            print(f"-{self.name}5-{time_string}T: {line5}")
            barrier.wait()
            self.serial.write(b'A6\n') #A6 Reading
            line6 = self.serial.read_until(expected=b'\n').decode().strip()
           # value_A6 = float(line)
            print(f"-{self.name}6-{time_string}T: {line6}")
            barrier.wait()
            time.sleep(0.001) # delay: 1 ms

    def stop(self):
        self.run = False