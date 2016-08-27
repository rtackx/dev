import sys

filename_coms = sys.argv[1] 
filename_bip = sys.argv[2]

degree_nodes = {}
with open(filename_bip, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_node = line.pop(0)
		degree_nodes[id_node] = len(line)

coms = {}
with open(filename_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)
		if len(line) == 1:
			continue

		coms[id_com] = 0
		for id_node in line:		
			coms[id_com] += degree_nodes[id_node]

f = open(filename_coms + ".nb_edges_coms", 'w')
for id_com in coms:
	f.write(id_com + ' ' + str(coms[id_com]) + '\n')
f.close()