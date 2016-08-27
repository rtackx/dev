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
actor_total = {}
movie_actors = {}
with open(filename_bip, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_movie = line.pop(0)
		movie_actors[id_movie] = set(line)

		for id_actor in line:
			netdata.setdefault(id_actor, {})
			actor_total.setdefault(id_actor, 0)

			for id_actor2 in line:
				if id_actor == id_actor2:
					continue
				netdata[id_actor].setdefault(id_actor2, 0)
				netdata[id_actor][id_actor2] += 1
				actor_total[id_actor] += 1

f = open(filename_bip + ".actor_network_weighted", 'w')
f2 = open(filename_bip + ".actor_network", 'w')
for id_actor in netdata:
	for id_actor2 in netdata[id_actor]:
		netdata[id_actor][id_actor2] = 1.0 * netdata[id_actor][id_actor2] / actor_total[id_actor]
		f.write(id_actor + ' ' + id_actor2 + ' ' + str(netdata[id_actor][id_actor2]) + '\n')
		f2.write(id_actor + ' ' + id_actor2 + '\n')
f.close()
f2.close()

coms_actor_measure = {}
for id_com in coms:
	coms_actor_measure[id_com] = 0.0

	list_actors = set()
	for id_movie in coms[id_com]:
		list_actors |= movie_actors[id_movie]
	list_actors = list(list_actors)

	for i in range(0, len(list_actors)):
		for y in range(i+1, len(list_actors)):
			id_actor = list_actors[i]
			id_actor2 = list_actors[y]

			if id_actor2 in netdata[id_actor]:
				coms_actor_measure[id_com] += netdata[id_actor][id_actor2]

	coms_actor_measure[id_com] /= 1.0 * (len(list_actors) * (len(list_actors) - 1) / 2.0)

f = open(filename_coms + ".actors_measure", 'w')
for id_com in coms_actor_measure:
	f.write(id_com + ' ' + str(coms_actor_measure[id_com]) + '\n')
f.close()




