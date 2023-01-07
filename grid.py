import numpy as np 

def make_grid(file):
	f = open(file, "r")
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
	#backwarding the string
	shape =''.join(reversed(shape))
	shape_list = list(shape)
	shape_list = shape_list[1:]
	grid= np.array(shape_list).reshape((m,n))

	#backward every line of the table 
	for i in range(m):
		grid[i] = np.flipud(grid[i])
	return grid

'''
get the info
'''
def get_info(file):
	f = open(file, "r")
	dim = f.readline()
	m   = int(dim.split()[0])
	n   = int(dim.split()[1])
	shape = f.readline()
	info = f.readline()
	info_list = info.split('@')
	horizental_info = []
	vertical_info =[]
	for index,value in enumerate(info_list):
		row = value.split('#')
		row_list=[]
		for i in range(len(row)):
			key = row[i]
			if key[0]=='&':
				key = key[1:]
			elif key[-1] == '&':
				key = key[:-1]
			data = {
					"KEY" : key,
					"VALUE": "",
					}
			row_list.append(data)
		if index<m:
			horizental_info.append(row_list)
		else:
			vertical_info.append(row_list)
	return horizental_info,vertical_info 
