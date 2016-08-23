import sys

# must be an edgelist file format
filename = sys.argv[1]

id_index_nodes = {}
index = 0

with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		if line[0] not in id_index_nodes:
			id_index_nodes[line[0]] = str(index)
			index += 1
		if line[1] not in id_index_nodes:
			id_index_nodes[line[1]] = str(index)
			index += 1

f = open(filename + ".renumbered", 'w')
with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		f.write(id_index_nodes[line[0]] + " " + id_index_nodes[line[1]])
		if len(line) == 3:
			f.write(" " + line[2])
		f.write('\n')
f.close()