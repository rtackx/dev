import sys

filename_tree = sys.argv[1]
filename_table_num = sys.argv[2]

def get_com(lvl, com_id, hier_coms):
	if lvl == 1:
		return hier_coms[lvl][com_id]
	else:
		list_node = []
		for id_node in hier_coms[lvl][com_id]:
			list_node.extend(get_com(lvl-1, id_node, hier_coms))
		return list_node

table_nums = {}
with open(filename_table_num, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		table_nums[line[1]] = line[0]


hier_coms = {}
level = 0

with open(filename_tree, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		# first node index has to be 0
		if line[0] == "0":
			coms = {}
			level += 1
			hier_coms[level] = coms			

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

f = open(filename_tree + "_lvl" + str(level), 'w')
for id_com in hier_coms[level]:
	string = id_com
	list_node = get_com(level, id_com, hier_coms)

	for index_node in list_node:
		if index_node in table_nums:
			string += ' ' + table_nums[index_node]

	if string != id_com:
		f.write(string + '\n')
f.close()