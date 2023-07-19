import time
from datetime import datetime
import serial

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
        temp_start = time.time()

        while self.run:

            # Get the current time
            now4 = datetime.now()
            time_string4 = now4.strftime("%H:%M:%S:%f")
            self.serial.write(b'A4\n')  # Request reading from A4
            value_A4 = float(self.serial.read_until(expected=b'\n').decode().strip())
            self.dq.put([self.name+'4', value_A4])
            print(f"-{self.name}4-{time_string4}T: {value_A4}")
            barrier.wait()

            now5 = datetime.now()
            time_string5 = now5.strftime("%H:%M:%S:%f")
            self.serial.write(b'A5\n') #A5 Reading
            value_A5 = float(self.serial.read_until(expected=b'\n').decode().strip())
            self.dq.put([self.name+'5',value_A5])
            print(f"-{self.name}5-{time_string5}T: {value_A5}")
            barrier.wait()

            now6 = datetime.now()
            time_string6 = now6.strftime("%H:%M:%S:%f")
            self.serial.write(b'A6\n') #A6 Reading
            value_A6 = float(self.serial.read_until(expected=b'\n').decode().strip())
            self.dq.put([self.name+'6',value_A6])
            print(f"-{self.name}6-{time_string6}T: {value_A6}")
            barrier.wait()

            if time.time() - temp_start > 12:
                self.dq.put(["STOP", -1.0])
                self.stop()

            time.sleep(0.001) # delay: 1 ms

        print("Aquisition Finished!")

    def stop(self):
        self.run = False