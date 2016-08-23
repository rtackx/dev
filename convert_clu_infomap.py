import sys

filename_clu = sys.argv[1]
# example : ./Infomap IMDB_movies-actors_1980-2010.bipartite_num.adjency IMDB -i bipartite --clu --map -z --show-bipartite-nodes
filename_table_num = sys.argv[2]

table_nums = {}
with open(filename_table_num, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		table_nums[line[1]] = line[0]

coms = {}
level = 1

with open(filename_clu, 'r') as file:
	for line in file:
		if line[0] == "n":
			continue

		line = line.replace("\n", "").split()

		id_com = line[1]
		coms.setdefault(id_com, [])
		coms[id_com].append(line[0][1:])


f = open(filename_clu + ".coms", 'w')
for id_com in coms:
	string = id_com
	for index_node in coms[id_com]:
		if index_node in table_nums:
			string += ' ' + table_nums[index_node]

	if string != id_com:
		f.write(string + '\n')
f.close()