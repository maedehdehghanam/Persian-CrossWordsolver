import numpy as np 

f = open("sample.txt", "r")
''''
get the dimention of the table
'''
dim = f.readline()
m   = int(dim.split()[0])
n   = int(dim.split()[1])
'''
get the table's shape to make the grid
'''
shape = f.readline()
shape_list = list(shape)
grid= np.array(shape_list[0:-1]).reshape((m,n)) 

print(grid)