# a link exist between 2 actors if they have played together for at least 2 different movies

import sys

filename_bip = sys.argv[1]
filename_coms = sys.argv[2]

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
actor_movies = {}

with open(filename_bip, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_movie = line.pop(0)
		movies[id_movie] = set(line)
		
		for i in range(0, len(line)):
			id_actor = line[i]
			netdata.setdefault(id_actor, set())
			actor_movies.setdefault(id_actor, set())

			for j in range(i+1, len(line)):
				id_actor2 = line[j]
				netdata.setdefault(id_actor2, set())
				actor_movies.setdefault(id_actor2, set())

				if id_actor2 in actor_movies[id_actor]:
					netdata[id_actor].add(id_actor2)
					netdata[id_actor2].add(id_actor)
				else:
					actor_movies[id_actor].add(id_actor2)
					actor_movies[id_actor2].add(id_actor)


f = open(filename_coms + ".actor_network_sparse", 'w')
for id_actor in netdata:
	for id_actor2 in netdata[id_actor]:
		f.write(id_actor + ' ' + id_actor2 + '\n')
f.close()

measure = {}

for id_com in coms:
	list_actor = set()
	for id_movie in coms[id_com]:
		list_actor |= movies[id_movie]
	list_actor = list(list_actor)

	nb_link = 0
	for i in range(0, len(list_actor)):
		for j in range(i+1, len(list_actor)):
			if list_actor[i] in netdata[list_actor[j]]:
				nb_link += 1

	measure[id_com] = 1.0 * nb_link / (len(list_actor) * (len(list_actor) - 1) / 2.0)

f = open(filename_coms + ".actor_network_sparse_measure", 'w')
for id_com in measure:
	f.write(id_com + ' ' + str(measure[id_com]) + '\n')
f.close()




