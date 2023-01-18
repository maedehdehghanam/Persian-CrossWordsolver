import csv
import numpy as np 
filename = "classification_data .csv"
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = list(reader)
data = np.array(x)
print(data)