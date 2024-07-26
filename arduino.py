import time
from datetime import datetime
import serial
from dataWriter import Recorder
from test import stop_Flag
import process_manager


'''
Print Sensor Readings Code:
now4 = datetime.now()
time_string4 = now4.strftime("%H:%M:%S:%f")
#print(f"-{self.name}4-{time_string4}T: {value_A4}")
'''

class Arduino:
    #Initializer
    #Establish Serial Connection
    def __init__(self, port, baudrate, name, dq, acquire):
        self.name = name
        self.dq = dq
        self.serial = serial.Serial(port, baudrate, timeout= 10)
        print(f'Arduino Connected!')
        self.run = True
        self.data = Recorder(self.name)
        self.acquire = acquire

    def read(self, barrier):
        print(f'{self.name} preparing to run...')
        self.serial.reset_input_buffer()
        time.sleep(2) #Allow time for Arduinos to prepare

        # check if arduino is apart of data acquisition
        if self.acquire == True:
            while self.run:
                try:
                    # write A4 to serial buffer so Serial.available() > 0 is true
                    self.serial.write(b'A4\n')  # Request reading from A4
                    value_A4 = float(self.serial.read_until(expected=b'\n').decode().strip().replace('\r.', ''))
                    self.dq.put([self.name+'4', value_A4]) # store value in queue
                    self.data.add(1, value_A4) # add value to recorder
                    barrier.wait(timeout=5)

                    # write A5 to serial buffer so Serial.available() > 0 is true
                    self.serial.write(b'A5\n') #A5 Reading
                    value_A5 = float(self.serial.read_until(expected=b'\n').decode().strip().replace('\r.', ''))
                    self.dq.put([self.name+'5',value_A5]) # store value in queue
                    self.data.add(2, value_A5) # add value to recorder
                    barrier.wait(timeout=5)
                        
                    # write A5 to serial buffer so Serial.available() > 0 is true
                    self.serial.write(b'A6\n') #A6 Reading
                    value_A6 = float(self.serial.read_until(expected=b'\n').decode().strip().replace('\r.', ''))
                    self.dq.put([self.name+'6',value_A6]) # store value in queue
                    self.data.add(3, value_A6) # add value to recorder
                    barrier.wait(timeout=5)

                    self.data.writeData()

                    time.sleep(0.001)

                except Exception: 
                    self.dq.put(["STOP", -1.0])
                    self.data.writeData()
                    print(Exception)
        else:
            self.serial.write(b'Start\n')

            while self.run:
                try:
                    command = self.serial.read_until()
                    command = command.decode("utf-8")
                    print("command: ", command)
                    if (command == 'End\n'):
                        process_manager.terminate_processes()
                    else:
                        continue

                except Exception:
                    continue

    def stop(self):
        self.run = False
        print('Stop run')
        self.dq.put(["STOP", -1.0])
        stop_Flag.value += 1
        if self.serial.is_open:
            self.serial.close()
        print(f'Closed {self.name} Serial Connection')

