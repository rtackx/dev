import sys

filename_bip = sys.argv[1]
filename_com = sys.argv[2]

coms = {}
with open(filename_com, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)

		coms[id_com] = line

neigh_top_nodes = {}
neigh_bot_nodes = {}
with open(filename_bip, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_top = line.pop(0)
		neigh_top_nodes[id_top] = line

		for id_bot in neigh_top_nodes[id_top]:
			neigh_bot_nodes.setdefault(id_bot, [])
			neigh_bot_nodes[id_bot].append(id_top)


separability_coms = {}
for id_com in coms:
	nb_internal_edges = 0
	nb_external_edges = 0

	list_visited_id_bot = []

	for id_top in coms[id_com]:
		nb_internal_edges += len(neigh_top_nodes[id_top])

		for id_bot in neigh_top_nodes[id_top]:
			if id_bot in list_visited_id_bot:
				continue
			
			list_visited_id_bot.append(id_bot)

			for id_top_neigh in neigh_bot_nodes[id_bot]:
				if id_top_neigh not in coms[id_com]:
					nb_external_edges += 1

	if nb_external_edges:
		separability_coms[id_com] = 1.0 * nb_internal_edges / nb_external_edges
	else:
		separability_coms[id_com] = nb_internal_edges


f = open(filename_bip + ".separability", 'w')
for id_com in separability_coms:
	f.write(id_com + ' ' + str(separability_coms[id_com]) + '\n')
f.close()
		






