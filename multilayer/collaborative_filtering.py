import sys, math

def load_layer(filename, links_coupling):
	data = {}

	with open(filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			if line[0] in links_coupling and line[1] in links_coupling:

				if line[0] not in data:
					data[line[0]] = []
				if line[1] not in data:
					data[line[1]] = []

				data[line[0]].append(line[1])
				data[line[1]].append(line[0])

	return data

def load_coupling(filename):
	# assuming that links go from l1 to l2
	coupling = {}
	nodes_l2 = {}
	weights = {}

	with open(filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			if line[0] not in coupling:
				coupling[line[0]] = []
			if line[1] not in nodes_l2:
				nodes_l2[line[1]] = []
				weights[line[1]] = {}

			coupling[line[0]].append(line[1])
			nodes_l2[line[1]].append(line[0])
			weights[line[1]][line[0]] = float(line[2])

	return coupling, nodes_l2, weights

def jaccard_similarity(node1_l1, node2_l1, links_coupling):
	A = set(links_coupling[node1_l1])
	B = set(links_coupling[node2_l1])
	return 1.0 * len(A.intersection(B)) / len(A.union(B))

def jaccard_similarity_asym(node1_l1, node2_l1, links_coupling):
	A = set(links_coupling[node1_l1])
	B = set(links_coupling[node2_l1])
	return 1.0 * len(A.intersection(B)) / len(A)

def sim_pearson(node1_l1, node2_l1, links_coupling, weights):
	common_items = []
	for node_l2 in links_coupling[node2_l1]:
		if node_l2 in links_coupling[node1_l1]:
			common_items.append(node_l2)

	if len(common_items) == 0:
		return 0.0

	n = len(common_items)
	sum1 = sum([weights[it][node1_l1] for it in common_items])
	sum2 = sum([weights[it][node2_l1] for it in common_items])
	sum1_sqr = sum([pow(weights[it][node1_l1], 2) for it in common_items])
	sum2_sqr = sum([pow(weights[it][node2_l1], 2) for it in common_items])
	product_sum = sum([weights[it][node1_l1] * weights[it][node2_l1] for it in common_items])

	'''print node1_l1, node2_l1
	print common_items
	print sum1, sum2
	print sum1_sqr, sum2_sqr
	print product_sum'''

	#Calculate r (Pearson score)
	num = product_sum - (sum1 * sum2 / n * 1.0)
	den = math.sqrt((sum1_sqr - pow(sum1, 2) / n * 1.0) * (sum2_sqr - pow(sum2, 2) / n * 1.0))
	if den == 0.0:
		return 0.0

	r = 1.0 * num / den

	return r

def top_similar_l1(node_l1, nodes_l1, links_coupling):
	# get top 15 more similar
	top = 4
	if len(nodes_l1[node_l1]) < top:
		top = len(nodes_l1[node_l1])

	list_neighborhood_sim = []
	for node_l2 in nodes_l1[node_l1]:
		jaccard_value = jaccard_similarity_asym(node_l1, node_l2, links_coupling)
		if jaccard_value > 0.0:
			list_neighborhood_sim.append([jaccard_value, node_l2])

	if len(list_neighborhood_sim) == 0:
		return set()

	list_neighborhood_sim.sort()
	list_neighborhood_sim.reverse()

	return set(zip(*list_neighborhood_sim[0:top])[1])

def get_recommendations(node_l1, nodes_l1, links_coupling, weights):
	recommendation = {}
	sum_sims = {}
	for node_l1_bis in nodes_l1:
		if node_l1 == node_l1_bis:
			continue

		sim = sim_pearson(node_l1, node_l1_bis, links_coupling, weights)
		
		if sim <= 0.0:
			continue

		for node_l2 in links_coupling[node_l1_bis]:
			if node_l2 not in links_coupling[node_l1]:
				if node_l2 not in recommendation:
					recommendation[node_l2] = 0.0

				recommendation[node_l2] += weights[node_l2][node_l1_bis] * sim
				sum_sims.setdefault(node_l2, 0.0)
				sum_sims[node_l2] += sim

	rankings = [(1.0 * total / sum_sims[node_l2], node_l2) for node_l2, total in recommendation.items()]
	rankings.sort()
	rankings.reverse()

	return rankings

if __name__  == "__main__":
	filename_layer1 = sys.argv[1]
	filename_coupling = sys.argv[2]

	links_coupling, nodes_l2, weights = load_coupling(filename_coupling)
	nodes_l1 = load_layer(filename_layer1, links_coupling)

	nodes_l1_recommendation = {}
	i = 1
	for node_l1 in nodes_l1:
		print str(i) + " / " + str(len(nodes_l1)) 
		i += 1
		if i == 15000:
			break

		list_rec = get_recommendations(node_l1, nodes_l1, links_coupling, weights)

		top = 15
		if len(list_rec) < top:
			top = len(list_rec)
		if len(list_rec) == 0:
			nodes_l1_recommendation[node_l1] = ()
		else:
			nodes_l1_recommendation[node_l1] = zip(*list_rec)[1]

	f = open("CF_communities", 'w')
	for node_l1 in nodes_l1_recommendation:
		f.write(str(node_l1))
		for node_l2 in nodes_l1_recommendation[node_l1]:
			f.write(" " + node_l2)			
		f.write('\n')
	f.close()

	'''print "Computing similar layer 1 nodes"
	list_similar_l1 = {}
	for node_l1 in nodes_l1:
		list_similar_l1[node_l1] = top_similar_l1(node_l1, nodes_l1, links_coupling)
		
	print "Computing recommended layer 2 nodes"
	recommanded_l2 = {}
	for node1_l1 in list_similar_l1:
		recommanded_l2[node1_l1] = set()
		for node2_l1 in list_similar_l1[node1_l1]:
			for node_l2 in links_coupling[node2_l1]:
				if node_l2 not in links_coupling[node1_l1]:
					recommanded_l2[node1_l1].add(node_l2)

	print "Aggregating layer 1 nodes into communities"
	list_communities_l1 = {}
	index = 0
	for node1_l1 in list_similar_l1:
		list_communities_l1[index] = set([node1_l1])
		list_communities_l1[index] = list_communities_l1[index].union(list_similar_l1[node1_l1])
		index += 1

	keys_id_com = list_communities_l1.keys()
	for id_com1 in keys_id_com:
		find = False
		for id_com2 in list_communities_l1.keys():
			if id_com1 == id_com2:
				continue

			for id_node in list_communities_l1[id_com1]:
				if id_node in list_communities_l1[id_com2]:
					find = True
					break

			if find:
				for id_node in list_communities_l1[id_com2]:
					list_communities_l1[id_com1].add(id_node)
				del list_communities_l1[id_com2]
				keys_id_com.remove(id_com2)
				find = False


	print "Adding recommended layer 2 nodes into communities"
	list_communities_l2 = {}
	for id_com1 in list_communities_l1:
		list_communities_l2[id_com1] = set([])

		for node_l1 in list_communities_l1[id_com1]:
			for node_l2 in recommanded_l2[node_l1]:
				list_communities_l2[id_com1].add(node_l2)

	nb_similar_nodes_l1 = 0
	nb_similar_nodes_l2 = 0

	f = open("CF_communities", 'w')
	for id_com in list_communities_l1:
		f.write(str(id_com))

		nb_similar_nodes_l1 += len(list_communities_l1[id_com])
		nb_similar_nodes_l2 += len(list_communities_l2[id_com])

		for node_l1 in list_communities_l1[id_com]:
			f.write(" " + node_l1)
		for node_l2 in list_communities_l2[id_com]:
			f.write(" " + node_l2)
		f.write('\n')
	f.close()

	print "Statistics :"

	print "Nb node l1 : " + str(len(nodes_l1))
	print "Nb node l2 : " + str(len(nodes_l2))
	print "Nb node l1 in coupling : " + str(len(links_coupling))
	print "Nb of community : " + str(len(list_similar_l1))
	print "Overlap layer 1 : " + str(1 - (1.0 * nb_similar_nodes_l1 / len(nodes_l1)))
	print "Overlap layer 2 : " + str(1 - (1.0 * nb_similar_nodes_l2 / len(nodes_l2)))'''
