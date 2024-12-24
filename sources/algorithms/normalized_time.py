from dataclasses import dataclass
from pathlib import Path
import csv

@dataclass
class Normalized_time():
    def __init__(self,measures:list[float]):
         if len(measures) != 10:
              raise ValueError("Normalized_time need to have 10 samples")
         self.nt_0 = measures[0]
         self.nt_1 = measures[1]
         self.nt_2 = measures[2]
         self.nt_3 = measures[3]
         self.nt_4 = measures[4]
         self.nt_5 = measures[5]
         self.nt_6 = measures[6]
         self.nt_7 = measures[7]
         self.nt_8 = measures[8]
         self.nt_9 = measures[9]

    nt_0: float
    nt_1: float
    nt_2: float
    nt_3: float
    nt_4: float
    nt_5: float
    nt_6: float
    nt_7: float
    nt_8: float
    nt_9: float

def deserialize_norm_time_from_csv(file:Path)-> Normalized_time:
    with open(file) as nt_file:
        reader = csv.reader(nt_file, delimiter='\t')
        frequency = []
        try:
            for row in reader:
                row = row
                if row[2] == 'F0':
                    continue
                frequency.append(row[2])
        except Exception as e: 
            print(e)
            exit(-1)

        return Normalized_time(frequency)
