import numpy as np 
'''
OPEN SAMPLE.TXT
'''
f = open("sample.txt", "r")
''''
get the dimention of the table
'''
dim = f.readline()
m   = int(num.split()[0])
n   = int(num.split()[1])
'''
get the table's shape to make the grid
'''
shape = f.readline()
shpe_list = list(shpe)
grid= np.array(shape_list[0:-1]).reshape((m,n)) 

