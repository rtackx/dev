import sys

#top nodes
filename_coms = sys.argv[2]
#bottom nodes
filename_network


coms = {}
with open(filename_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)
		if len(line) == 1:
			continue

		coms[id_com] = line

