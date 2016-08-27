import sys

filename_coms = sys.argv[1]
filename_attr = sys.argv[2]

coms = {}
with open(filename_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)
		if len(line) == 1:
			continue
		
		coms[id_com] = line

attr = {}
with open(filename_attr, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		movie = line.pop(0)
		attr[movie] = line


similarity = {}
for id_com in coms:
	coms_sim = []
	
	for movie in coms[id_com]:

