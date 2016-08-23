import sys

def write_result(filename_results, data):
	f = open(filename_results, 'w')
	for id in data:
		f.write(id + " " + str(data[id]) + "\n")
	f.close()

def get_modularity_coms(coms, nodes_layer1, nodes_layer2, coupling_links, m):
	modularity_coms = {}

	for com_id in coms:
		mod = 0.0		

		for node_id1 in coms[com_id]:
			for node_id2 in coms[com_id]:
				adjacent = False
				k_id1 = 0.0
				k_id2 = 0.0
				score = 0.0

				if node_id1 == node_id2:
					continue

				if node_id1 in nodes_layer1 and node_id2 in nodes_layer1:
					k_id1 = len(nodes_layer1[node_id1])
					k_id2 = len(nodes_layer1[node_id2])

					if node_id1 in nodes_layer1[node_id2]:
						adjacent = True
				elif node_id1 in nodes_layer2 and node_id2 in nodes_layer2:
					k_id1 = len(nodes_layer2[node_id1])
					k_id2 = len(nodes_layer2[node_id2])
					
					if node_id1 in nodes_layer2[node_id2]:						
						adjacent = True
				else:
					if node_id1 in coupling_links and node_id2 in coupling_links:
						k_id1 = len(coupling_links[node_id1])
						k_id2 = len(coupling_links[node_id2])

						if node_id1 in coupling_links[node_id2]:
							adjacent = True
					else:
						print "Something weird between " + node_id1 + " and " + node_id2 + " (com : " + com_id + ")"
						continue
				
				if adjacent:
					score = 1.0 - (k_id1 * k_id2) / (2.0 * m)
				else:
					score = 0.0 - (k_id1 * k_id2) / (2.0 * m)

				mod += score

		modularity_coms[com_id] = mod / (2.0 * m)

	return modularity_coms


def get_features_links_coms(coms, nodes_layer1, nodes_layer2, coupling_links):
	# format for com_id : ( 
	#			 (nb_intra_links_layer1, nb_nodes_layer1),
	#			 (nb_intra_links_layer2, nb_nodes_layer2),
	#             nb_inter_links
	# 			)
	feature_links_com = {}

	for com_id in coms:
		nb_intra_links_layer1 = 0
		nb_external_links_layer1 = 0
		nb_nodes_layer1 = set()
		nb_intra_links_layer2 = 0
		nb_external_links_layer2 = 0
		nb_nodes_layer2 = set()
		nb_inter_links = 0

		for node_id1 in coms[com_id]:
			if node_id1 in nodes_layer1:
				for node_id2 in nodes_layer1[node_id1]:
					if node_id2 in coms[com_id]:
						nb_intra_links_layer1 += 1
						nb_nodes_layer1.add(node_id2)
					else:
						nb_external_links_layer1 += 1
			else:
				for node_id2 in nodes_layer2[node_id1]:
					if node_id2 in coms[com_id]:
						nb_intra_links_layer2 += 1
						nb_nodes_layer2.add(node_id2)
					else:
						nb_external_links_layer2 += 1
		
		for node_l1 in nb_nodes_layer1:
			if node_l1 not in coupling_links:
				continue

			for node_l2 in nb_nodes_layer2:
				if node_l2 in coupling_links[node_l1]:
					nb_inter_links += 1

		feature_links_com[com_id] = ((nb_intra_links_layer1, nb_external_links_layer1, len(nb_nodes_layer1)), (nb_intra_links_layer2, nb_external_links_layer2, len(nb_nodes_layer2)), nb_inter_links)

	return feature_links_com

def get_fraction_intra_inter_links(nodes_layer, coupling_links):
	fraction_intra_inter_links = {}

	for node_id in nodes_layer:
		if node_id in coupling_links:
			fraction_intra_inter_links[node_id] = 1.0 * len(coupling_links[node_id]) / len(nodes_layer[node_id])
		else:
			fraction_intra_inter_links[node_id] = 0.0

	return fraction_intra_inter_links

def get_fraction_intra_inter_weigthed_links(nodes_layer_weights, coupling_links_weights):
	fraction_intra_inter_weighted_links = {}

	for node_id1 in nodes_layer_weights:
		if node_id1 in coupling_links_weights:
			w_layer = 0.0
			for node_id2 in nodes_layer_weights[node_id1]:
				w_layer += nodes_layer_weights[node_id1][node_id2]

			w_coupling = 0.0
			for node_id2 in coupling_links_weights[node_id1]:
				w_coupling += coupling_links_weights[node_id1][node_id2]

			fraction_intra_inter_weighted_links[node_id] = 1.0 * w_layer / w_coupling
		else:
			fraction_intra_inter_weighted_links[node_id] = 0.0

	return fraction_intra_inter_weighted_links

def load_coms_layer(filename_coms_layer):
	coms_layer = {}

	with open(filename_coms_layer, 'r') as file:
		for line in file:
			line = line.replace('\n', '').split()

			com_id = line.pop(0)
			coms_layer[com_id] = set(line)

	return coms_layer

def load_layer(filename_layer):
	nodes_layer = {}
	nodes_layer_weights = {}
	m = 0

	with open(filename_layer, 'r') as file:
		for line in file:
			line = line.replace('\n', '').split()
			
			nodes_layer.setdefault(line[0], set())
			nodes_layer.setdefault(line[1], set())
			nodes_layer[line[0]].add(line[1])
			nodes_layer[line[1]].add(line[0])
			m += 1

			'''if len(line) == 3:
				nodes_layer_weights.setdefault(line[0], {})
				nodes_layer_weights.setdefault(line[1], {})
				nodes_layer_weights[line[0]].setdefault(line[1], {})
				nodes_layer_weights[line[1]].setdefault(line[0], {})
				nodes_layer_weights[line[0]][line[1]] = float(line[2])
				nodes_layer_weights[line[1]][line[0]] = float(line[2])'''

	return nodes_layer, nodes_layer_weights, m

filename_layer1 = sys.argv[1]
filename_layer2 = sys.argv[2]
filename_layer_coupling = sys.argv[3]
filename_communities = sys.argv[4]
filename_results_dir = sys.argv[5]

print "Loading layer 1"
nodes_l1, nodes_l1_weights, m_l1 = load_layer(filename_layer1)
print "Loading layer 2"
nodes_l2, nodes_l2_weights, m_l2 = load_layer(filename_layer2)
print "Loading coupling links"
coupling_links, coupling_links_weights, m_coupling = load_layer(filename_layer_coupling)

m = m_l1 + m_l2 + m_couplings
print "Layer 1 : " + str(len(nodes_l1)) + " (" + str(m_l1) + " links)"
print "Layer 2 : " + str(len(nodes_l2)) + " (" + str(m_l2) + " links)"
print "Layer coupling : " + str(len(coupling_links)) + " (" + str(m_coupling) + " links)"
print "In total : " + str(len(nodes_l1) + len(nodes_l2) + len(coupling_links)) + " (" + str(m) + " links)"

'''print "Computing intra-inter links of layer 1"
fraction_intra_inter_links_layer1 = get_fraction_intra_inter_links(nodes_l1, coupling_links)
print "Computing intra-inter links of layer 2"
fraction_intra_inter_links_layer2 = get_fraction_intra_inter_links(nodes_l2, coupling_links)
write_result(filename_results_dir + "/fraction_intra_inter_links.layer1", fraction_intra_inter_links_layer1)
write_result(filename_results_dir + "/fraction_intra_inter_links.layer2", fraction_intra_inter_links_layer2)'''

'''fraction_intra_inter_weighted_links_layer1 = get_fraction_intra_inter_weigthed_links(nodes_l1_weights, coupling_links_weights)
fraction_intra_inter_weighted_links_layer2 = get_fraction_intra_inter_weigthed_links(nodes_l2_weights, coupling_links_weights)
write_result(filename_results_dir + "/fraction_intra_inter_links.layer1.weights", fraction_intra_inter_weighted_links_layer1)
write_result(filename_results_dir + "/fraction_intra_inter_links.layer2.weights", fraction_intra_inter_weighted_links_layer2)'''

print "Loading community file"
coms_layer = load_coms_layer(filename_communities)
print "Computing community features"
feature_links_com_layer = get_features_links_coms(coms_layer, nodes_l1, nodes_l2, coupling_links)
print "Computing community modularities"
modularity_coms = get_modularity_coms(coms_layer, nodes_l1, nodes_l2, coupling_links, m)

'''f1 = open(filename_results_dir + "/coms_density_intra_link_layer1", 'w')
f2 = open(filename_results_dir + "/coms_density_intra_link_layer2", 'w')
f3 = open(filename_results_dir + "/coms_density_inter_link", 'w')
f4 = open(filename_results_dir + "/separability_layer1", 'w')
f5 = open(filename_results_dir + "/separability_layer2", 'w')
f6 = open(filename_results_dir + "/separability", 'w')
for com_id in feature_links_com_layer:
	(nb_intra_links_layer1, nb_external_links_layer1, nb_nodes_layer1), (nb_intra_links_layer2, nb_external_links_layer2, nb_nodes_layer2), nb_inter_links = feature_links_com_layer[com_id]

	if nb_nodes_layer1 == 0:
		f1.write(com_id + " 0.0\n") 
	else:
		f1.write(com_id + " " + str(1.0 * nb_intra_links_layer1 / (nb_nodes_layer1 * (nb_nodes_layer1 - 1))) + "\n")
	if nb_nodes_layer2 == 0:
		f2.write(com_id + " 0.0\n")
	else: 
		f2.write(com_id + " " + str(1.0 * nb_intra_links_layer2 / (nb_nodes_layer2 * (nb_nodes_layer2 - 1))) + "\n")
	if nb_nodes_layer1 == 0 or nb_nodes_layer2 == 0:
		f3.write(com_id + " 0.0\n")
	else:
		f3.write(com_id + " " + str(1.0 * nb_inter_links / (nb_nodes_layer1 * nb_nodes_layer2)) + "\n")

	if nb_external_links_layer1 == 0:
		f4.write(com_id + " " + str(nb_intra_links_layer1) + "\n")
	else:
		f4.write(com_id + " " + str(1.0 * nb_intra_links_layer1 / (nb_external_links_layer1 + nb_inter_links)) + "\n")
	if nb_external_links_layer2 == 0:
		f5.write(com_id + " " + str(nb_intra_links_layer2) + "\n")
	else:
		f5.write(com_id + " " + str(1.0 * nb_intra_links_layer2 / (nb_external_links_layer2 + nb_inter_links)) + "\n")
	if nb_external_links_layer1 == 0 and nb_external_links_layer2 == 0:
		f6.write(com_id + " " + str(nb_intra_links_layer1 + nb_intra_links_layer2 + nb_inter_links) + "\n")
	else:
		f6.write(com_id + " " + str(1.0 * (nb_intra_links_layer1 + nb_intra_links_layer2 + nb_inter_links) / (nb_external_links_layer1 + nb_external_links_layer2)) + "\n")

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()'''