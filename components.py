import sys

# bipartite file
filename = sys.argv[1]

top_nodes = {}

with open(filename, 'r') as file:
	for line in file:
			line = line.replace('\n', '').split()

			id = line.pop(0)
			top_nodes[id] = line

for id_top_node in top_nodes:
	nb_element_overlap = 0

	for id_bot_node in top_nodes[id_top_node]:
		for id_top_node2 in top_nodes:
			if id_top_node != id_top_node2 and id_bot_node in top_nodes[id_top_node2]:
				nb_element_overlap += 1
				break
	print id_top_node + " : " + str(nb_element_overlap) + " / " + str(len(top_nodes[id_top_node])) 
