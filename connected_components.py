import sys

filename_graph = sys.argv[1]
if len(sys.argv) == 3:
	sep = sys.argv[2]
else:
	sep = " "

connected_components = {}

print "Loading edges..."

with open(filename_graph, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split(sep)

			if line[0] not in connected_components and line[1] not in connected_components:
				connected_components[line[0]] = set()
				id_comp = line[0]
			elif line[0] in connected_components:
				id_comp = line[0]
			else:
				id_comp = line[1]

			connected_components[id_comp].add(line[0])
			connected_components[id_comp].add(line[1])

print "Finding connected components..."

keys_id = connected_components.keys()
for id_comp1 in keys_id:
	find = False
	for id_comp2 in connected_components.keys():
		if id_comp1 == id_comp2:
			continue

		for id_node in connected_components[id_comp1]:
			if id_node in connected_components[id_comp2]:
				find = True
				break

		if find:
			for id_node in connected_components[id_comp2]:
				connected_components[id_comp1].add(id_node)
			del connected_components[id_comp2]
			keys_id.remove(id_comp2)
			find = False


connected_components = list(connected_components.values())

ordered_list_cc = sorted(connected_components, key=len, reverse=True)
print "Number of connected components : " + str(len(ordered_list_cc))
dist_size_cc = {}
for cc in ordered_list_cc:
	if len(cc) not in dist_size_cc:
		dist_size_cc[len(cc)] = 0
	dist_size_cc[len(cc)] += 1
print dist_size_cc

print "Writing giant component..."

f = open(filename_graph + "_giant", 'w')
with open(filename_graph, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split(sep)

			if line[0] in ordered_list_cc[0]:
				f.write(line[0] + " " + line[1])
				if len(line) == 3:
					f.write(" " + line[2])
				f.write('\n')
f.close()