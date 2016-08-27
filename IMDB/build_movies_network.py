import sys

filename_bip = sys.argv[1]
filename_coms = sys.argv[2]

print "Loading communities..."

coms = {}
with open(filename_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)
		if len(line) == 1:
			continue

		coms[id_com] = line

netdata = {}
movies = {}

print "Loading bipartite..."

with open(filename_bip, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_movie = line.pop(0)
		movies[id_movie] = set(line)

intersections = {}

print "Computing intersections inside communities..."

for id_com in coms:
	#max_inter = 0
	nb_inter = 0
	nb_inter_total = 0

	for i in range(0, len(coms[id_com])):
		id_movie = coms[id_com][i]
		nb_inter_total += len(movies[id_movie])

		for j in range(i+1, len(coms[id_com])):
			id_movie2 = coms[id_com][j]
			inter = len(movies[id_movie].intersection(movies[id_movie2]))

			nb_inter += inter

	intersections[id_com] = 1.0 * nb_inter / (nb_inter_total * (len(coms[id_com]) - 1))

f = open(filename_coms + ".movies_inter", 'w')
for id_com in intersections:
	f.write(id_com + ' ' + str(intersections[id_com]) + '\n')
f.close()

min_intersections = {}

print "Computing min intersections inside communities..."

for id_com in coms:
	set_node_inter = set()
	set_node_inter_total = set()

	for i in range(0, len(coms[id_com])):
		id_movie = coms[id_com][i]
		set_node_inter_total |= movies[id_movie]

		for j in range(i+1, len(coms[id_com])):
			id_movie2 = coms[id_com][j]
			set_node_inter |= (movies[id_movie] & movies[id_movie2])

	min_intersections[id_com] = 1.0 * len(set_node_inter & set_node_inter_total) / len(set_node_inter_total)

f = open(filename_coms + ".movies_min_inter", 'w')
for id_com in min_intersections:
	f.write(id_com + ' ' + str(min_intersections[id_com]) + '\n')
f.close()
