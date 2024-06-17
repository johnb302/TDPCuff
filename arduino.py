import time
from datetime import datetime
import serial
from dataWriter import Recorder

'''
Print Sensor Readings Code:
now4 = datetime.now()
time_string4 = now4.strftime("%H:%M:%S:%f")
#print(f"-{self.name}4-{time_string4}T: {value_A4}")
'''

class Arduino:
    #Initilizer
    #Establish Serial Connection
    def __init__(self, port, baudrate, name, dq):
        self.name = name
        self.dq = dq
        self.serial = serial.Serial(port, baudrate, timeout= 10)
        print(f'Arduino Connected!')
        self.run = True

    def read(self, barrier):
        print(f'{self.name} preparing to run...')
        self.serial.reset_input_buffer()
        time.sleep(2) #Allow time for Arduinos to prepare
        data = Recorder(self.name)

        while self.run:
            try:
                self.serial.write(b'A4\n')  # Request reading from A4
                value_A4 = float(self.serial.read_until(expected=b'\n').decode().strip())
                self.dq.put([self.name+'4', value_A4])
                data.add(1, value_A4)
                barrier.wait(timeout=5)

                self.serial.write(b'A5\n') #A5 Reading
                value_A5 = float(self.serial.read_until(expected=b'\n').decode().strip())
                self.dq.put([self.name+'5',value_A5])
                data.add(2, value_A5)
                barrier.wait(timeout=5)

                self.serial.write(b'A6\n') #A6 Reading
                value_A6 = float(self.serial.read_until(expected=b'\n').decode().strip())
                self.dq.put([self.name+'6',value_A6])
                data.add(3, value_A6)
                barrier.wait(timeout=5)

                time.sleep(0.001)

            except: 
                self.dq.put(["STOP", -1.0])
                self.stop()
                data.writeData()

        print(f"{self.name} has stopped!")

    def stop(self):
        self.run = False
        self.serial.close()
        print(f'Closed {self.name} Serial Connection')