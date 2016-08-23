import sys

filename_coms_of_coms = sys.argv[1]
filename_coms_nodes = sys.argv[2]

coms_nodes = {}
with open(filename_coms_nodes, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id = line.pop(0)
		coms_nodes[id] = line

filename_coms_unfolded = "unfolded_coms_nodes"
f_coms_unfolded = open(filename_coms_unfolded, 'w')
with open(filename_coms_of_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com_of_coms = line.pop(0)

		f_coms_unfolded.write(id_com_of_coms + " ")
		for id_com in line:
			for id_node in coms_nodes[id_com]:
				f_coms_unfolded.write(" " + id_node)
		f_coms_unfolded.write('\n')
f_coms_unfolded.close()
