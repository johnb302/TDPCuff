import pandas as pd
import numpy as np
import multiprocessing as mp
import math

class Recorder:
    def __init__(self):
        self.matrix = pd.DataFrame(columns=['R1', 'R2', 'R3', 'G1', 'G2', 'G3', 'B1', 'B2', 'B3'])
    
    def add(self, name, position, value):
        c = ['B', 'R', 'G']
        if name in c:
            column_name = name + str(position)
            if column_name in self.matrix.columns:
                # Find next row index to add to
                if self.matrix.empty:
                    self.matrix.loc[len(self.matrix), column_name] = value
                else:
                    for i in range(len(self.matrix[column_name])):
                        if math.isnan(self.matrix.loc[i, column_name]):
                            self.matrix.loc[i, column_name] = value
        else:
            print('Wrong board name./n')

ex = Recorder()
ex.add('B', 1, 10)
ex.add('B', 1, 20)
ex.add('R', 2, 30)
ex.add('R', 1, 55)
print(ex.matrix)
