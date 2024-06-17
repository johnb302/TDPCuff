import pandas as pd
import numpy as np
import multiprocessing as mp
import math

class Recorder:
    def __init__(self, name):
        self.name = name
        self.matrix = pd.DataFrame(columns=[name + str(1), name + str(2), name + str(3)])
    
    def add(self, sensorNum, value):
        column_name = self.name + str(sensorNum)
        if column_name in self.matrix.columns:
            if self.matrix.empty:
                self.matrix.loc[len(self.matrix), column_name] = value
            else:
                for i in range(len(self.matrix[column_name])):
                    if math.isnan(self.matrix.loc[i, column_name]):
                        self.matrix.loc[i, column_name] = value
        else:
            print('Wrong board name./n')

    def writeData(self):
        self.matrix.to_csv(self.name + '_data.csv')
