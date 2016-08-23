import sys

filename_tree = sys.argv[1]
filename_table_num = sys.argv[2]

table_nums = {}
with open(filename_table_num, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		table_nums[line[1]] = line[0]


hier_coms = {}
level = 1

with open(filename_tree, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		# first node index has to be 0
		if line[0] == "0":
			coms = {}
			hier_coms[level] = coms
			level += 1

		id_com = line[1]
		coms.setdefault(id_com, [])
		coms[id_com].append(line[0])

f = open(filename_tree + "_lvl1", 'w')
for id_com in hier_coms[1]:
	string = id_com
	for index_node in hier_coms[1][id_com]:
		if index_node in table_nums:
			string += ' ' + table_nums[index_node]

	if string != id_com:
		f.write(string + '\n')
f.close()