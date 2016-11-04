import sys

filename_network = sys.argv[1]
nodes = {}

index = 0

with open(filename_network, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		index_node1 = line[0]
		index_node2 = line[1]

		if index_node1 not in nodes:
			nodes[index_node1] = index
			index += 1
		if index_node2 not in nodes:
			nodes[index_node2] = index
			index += 1

f = open(filename_network + '_table_num', 'w')
for index in nodes:
	f.write(index + ' ' + str(nodes[index]) + '\n')
f.close()

f = open(filename_network + '_num', 'w')
with open(filename_network, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		index_node1 = line[0]
		index_node2 = line[1]

		f.write(str(nodes[index_node1]) + ' ' + str(nodes[index_node2]) + '\n')

f.close()

