import sys, os, subprocess, random, math
from random import randint, random, uniform

separator = '\t'

# Depth First Search of communities starting from the first layer
def recursive_cross_com_gathering(cross_communities_l1_l2, index_com1):
	if index_com1 not in cross_communities_l1_l2:
		return [index_com1]

	list_coms = [index_com1]

	for index_com2 in cross_communities_l1_l2[index_com1]:		
		list_coms.extend(recursive_cross_com_gathering(cross_communities_l1_l2, index_com2))

	return list_coms


def create_layers(outdir, nb_layers, dict_intra_params):
	layers = {}

	# create every layer based on LFR benchmark 
	for i in range(0, nb_layers):
		nb_com_layer = benchmark_lfr(i, outdir, dict_intra_params['n'], dict_intra_params['k'], dict_intra_params['maxk'], dict_intra_params['mu'])
		layers.setdefault(i, {})
		layers[i]['nb_coms'] = nb_com_layer
		layers[i]['nb_nodes'] = dict_intra_params['n']
		print "Layer %i created (with %i intra layer coms)" % (i, nb_com_layer)

	index_node = 0
	index_com = 0
	for i in range(0, nb_layers):
		rewrite_nodes_and_coms(i, outdir, index_node, index_com)
		
		layers[i]["from_id_node"] = index_node
		layers[i]["from_id_com"] = index_com

		index_node += layers[i]['nb_nodes']
		index_com += layers[i]['nb_coms']

	return layers


def rewrite_nodes_and_coms(num, directory, from_node, from_com):
	dir_layer = directory + "/layer" + str(num)
	filename_nodes = dir_layer + "/network.dat"
	filename_coms = dir_layer + "/community.dat"

	f_nodes = open(filename_nodes + "bis", 'w')
	with open(filename_nodes, 'r') as file:
		for line in file:
			line = line.replace("\n", "").replace(" ", "").split(separator)

			new_id1 = str(int(line[0]) + from_node)
			new_id2 = str(int(line[1]) + from_node)

			f_nodes.write(new_id1 + separator + new_id2 + '\n')
	f_nodes.close()

	os.popen("rm " + filename_nodes)
	os.popen("mv " + filename_nodes + "bis " + filename_nodes)

	f_coms = open(filename_coms + "bis", 'w')
	with open(filename_coms, 'r') as file:
		for line in file:
			line = line.replace("\n", "").replace(" ", "").split(separator)

			new_id1 = str(int(line[0]) + from_node)
			new_id2 = str(int(line[1]) + from_com)

			f_coms.write(new_id1 + separator + new_id2 + '\n')
	f_coms.close()

	os.popen("rm " + filename_coms)
	os.popen("mv " + filename_coms + "bis " + filename_coms)

def load_com_nodes(num, directory, layers):
	dir_layer = directory + "/layer" + str(num)
	filename_coms = dir_layer + "/community.dat"

	layers[num]['com_nodes'] = {}
	layers[num]['node_com'] = {}
	layers[num]['nodes'] = []

	with open(filename_coms, 'r') as file:
		for line in file:
			line = line.replace("\n", "").replace(" ", "").split(separator)

			index_com = int(line[1]) - 1
			layers[num]['com_nodes'].setdefault(index_com, [])
			layers[num]['com_nodes'][index_com].append(line[0])
			layers[num]['nodes'].append(line[0])
			layers[num]['node_com'][line[0]] = index_com

def benchmark_lfr(num, directory, n, k, maxk, mu):
	dir_layer = directory + "/layer" + str(num)
	if not os.path.exists(dir_layer):
		os.makedirs(dir_layer)

	cmd = "./benchmark -N %i -k %f -maxk %i -mu %f" % (n, k, maxk, mu)
	print cmd
	os.popen(cmd)
	cmd = "mv *.dat %s" % (dir_layer)
	os.popen(cmd)
	cmd = "cat %s/community.dat | cut -f 2 | sort | uniq | wc -l" % (dir_layer)
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	errcode = process.returncode
	nb_com_layer = int(out)
	return nb_com_layer

def create_cross_layer_communities(nb_layers, layers, alpha):
	cross_communities_l1_l2 = {}
	intra_coms = {}
	nb_intra_coms = 0

	for i in range(0, nb_layers-1):
		nb_min = min(layers[i]['nb_coms'], layers[i+1]['nb_coms'])
		nb_cross_coms = int(math.ceil(nb_min * alpha))
		
		list_id_coms_layer1 = range(layers[i]["from_id_com"], layers[i]["from_id_com"]+layers[i]['nb_coms'])
		list_id_coms_layer2 = range(layers[i+1]["from_id_com"], layers[i+1]["from_id_com"]+layers[i+1]['nb_coms'])
		
		j = 0
		while j < nb_cross_coms:
			j+= 1

			ind_l1 = randint(0, len(list_id_coms_layer1)-1)
			ind_l2 = randint(0, len(list_id_coms_layer2)-1)

			index_coms_l1 = list_id_coms_layer1[ind_l1]
			index_coms_l2 = list_id_coms_layer2[ind_l2]
			del list_id_coms_layer1[ind_l1]
			del list_id_coms_layer2[ind_l2]

			cross_communities_l1_l2.setdefault(index_coms_l1, [])
			cross_communities_l1_l2[index_coms_l1].append(index_coms_l2)


		intra_coms[i] = list_id_coms_layer1
		intra_coms[i+1] = list_id_coms_layer2
		nb_intra_coms += len(list_id_coms_layer1) + len(list_id_coms_layer2)

	cross_communities = []
	for index_com1 in cross_communities_l1_l2:
		list_coms = recursive_cross_com_gathering(cross_communities_l1_l2, index_com1)
		cross_communities.append(list_coms)

	return cross_communities, intra_coms, nb_intra_coms

def create_coupling_links(nb_layers, layers, d_param):
	couplings_links = {}
	for i in range(0, nb_layers-1):
		couplings_links.setdefault(i, {})
		couplings_links[i].setdefault(i+1, [])

		list_node_l1 = layers[i]['nodes']
		n_l1 = len(layers[i]['nodes'])
		list_node_l2 = layers[i+1]['nodes']
		n_l2 = len(layers[i+1]['nodes'])

		density = 0.0
		m = 0
		while density < d_param:
			ind_n1 = randint(0, n_l1-1)
			ind_n2 = randint(0, n_l2-1)

			index_node_l1 = list_node_l1[ind_n1]
			index_node_l2 = list_node_l2[ind_n2]

			if (index_node_l1, index_node_l2) not in couplings_links[i][i+1]:
				couplings_links[i][i+1].append((index_node_l1, index_node_l2))
				m += 1
				density = (1.0 * m) / (n_l1 * n_l2)

	return couplings_links

# attempt to create randomly a coupling link between nodes of index_com1 and index_com2
def add_coupling_links_inside_coms(l1, l2, index_com1, index_com2, couplings_links, layers):
	list_node_l1 = layers[l1]['com_nodes'][index_com1]
	n_l1 = len(list_node_l1)
	list_node_l2 = layers[l2]['com_nodes'][index_com2]
	n_l2 = len(list_node_l2)

	pair = []

	while len(pair) < (n_l1 * n_l2):
		ind_n1 = randint(0, n_l1-1)
		ind_n2 = randint(0, n_l2-1)
		index_node1 = list_node_l1[ind_n1]
		index_node2 = list_node_l2[ind_n2]

		if (index_node1, index_node2) not in couplings_links[l1][l2]:
			couplings_links[l1][l2].append((index_node1, index_node2))
			return 1
		else:
			pair.append((index_node1, index_node2))

	return 0

def add_coupling_links_outside_coms(l1, l2, index_com1, index_com2, couplings_links, layers):
	list_node_l1 = layers[l1]['com_nodes'][index_com1]
	n_l1 = len(list_node_l1)
	list_node_l2 = list(set(layers[l2]['nodes']) - set(layers[l2]['com_nodes'][index_com2]))
	n_l2 = len(list_node_l2)

	pair = []

	while len(pair) < (n_l1 * n_l2):
		ind_n1 = randint(0, n_l1-1)
		ind_n2 = randint(0, n_l2-1)
		index_node1 = list_node_l1[ind_n1]
		index_node2 = list_node_l2[ind_n2]

		if (index_node1, index_node2) not in couplings_links[l1][l2]:
			couplings_links[l1][l2].append((index_node1, index_node2))
			return 1
		else:
			pair.append((index_node1, index_node2))

	return 0

# modify existing coupling links to fit p_param condition
def apply_p_parameter(nb_layers, layers, couplings_links, cross_communities, p_param):
	for i in range(0, nb_layers-1):
		list_couplings_outside = []
		list_couplings_inside = []
		list_pair_coms = []

		nb_link_inside_cross_coms = 0
		nb_link_outside_cross_coms = 0

		for (index_node_l1, index_node_l2) in couplings_links[i][i+1]:
			index_com_node_l1 = layers[i]['node_com'][index_node_l1]
			index_com_node_l2 = layers[i+1]['node_com'][index_node_l2]

			find = False
			for list_coms in cross_communities:
				if index_com_node_l1 in list_coms and index_com_node_l2 in list_coms:
					find = True
					break

			if find:
				nb_link_inside_cross_coms += 1
				list_couplings_inside.append((index_node_l1, index_node_l2))

				if (index_com_node_l1, index_com_node_l2) not in list_pair_coms:
					list_pair_coms.append((index_com_node_l1, index_com_node_l2))
			else:
				nb_link_outside_cross_coms += 1
				list_couplings_outside.append((index_node_l1, index_node_l2))


		p_temp = (1.0 * nb_link_inside_cross_coms) / (nb_link_inside_cross_coms + nb_link_outside_cross_coms)
		nb_link_inside_cross_coms_real = nb_link_inside_cross_coms
		nb_link_outside_cross_coms_real = nb_link_outside_cross_coms

		if p_param > p_temp:
			while p_temp < p_param:
				ind_c = randint(0, len(list_couplings_outside)-1)
				couplings_links[i][i+1].remove(list_couplings_outside[ind_c])				
				

				success = 0
				pair = []
				while success == 0:
					ind_pair_coms = randint(0, len(list_pair_coms)-1)
					index_com1, index_com2 = list_pair_coms[ind_pair_coms]
					pair.append((index_com1, index_com2))

					success = add_coupling_links_inside_coms(i, i+1, index_com1, index_com2, couplings_links, layers)

					if len(pair) == len(list_pair_coms) and success == 0:
						success = 2

				nb_link_inside_cross_coms += 1
				nb_link_outside_cross_coms -= 1
				
				if success == 1:
					del list_couplings_outside[ind_c]
					nb_link_inside_cross_coms_real += 1
					nb_link_outside_cross_coms_real -= 1
				else:
					couplings_links[i][i+1].append(list_couplings_outside[ind_c])					

				p_temp = (1.0 * nb_link_inside_cross_coms) / (nb_link_inside_cross_coms + nb_link_outside_cross_coms)

		elif p_param < p_temp:
			while p_temp > p_param:
				ind_c = randint(0, len(list_couplings_inside)-1)
				couplings_links[i][i+1].remove(list_couplings_inside[ind_c])
				del list_couplings_inside[ind_c]

				success = 0
				pair = []
				while success == 0:
					ind_pair_coms = randint(0, len(list_pair_coms)-1)
					index_com1, index_com2 = list_pair_coms[ind_pair_coms]
					pair.append((index_com1, index_com2))

					success = add_coupling_links_outside_coms(i, i+1, index_com1, index_com2, couplings_links, layers)

					if len(pair) == len(list_pair_coms):
						success = 1

				nb_link_inside_cross_coms -= 1
				nb_link_outside_cross_coms += 1
				p_temp = (1.0 * nb_link_inside_cross_coms) / (nb_link_inside_cross_coms + nb_link_outside_cross_coms)


	print str(nb_link_inside_cross_coms) + "/ ( " + str(nb_link_inside_cross_coms) + " + " + str(nb_link_outside_cross_coms) + ")"
	
	p_temp_real = (1.0 * nb_link_inside_cross_coms_real) / (nb_link_inside_cross_coms_real + nb_link_outside_cross_coms_real)
	print p_temp, p_temp_real

	t = 0
	for l1 in couplings_links:
		for l2 in couplings_links[l1]:
			t += len(couplings_links[l1][l2])
	print t

	return nb_link_inside_cross_coms, nb_link_outside_cross_coms


def write_soum_format(directory, nb_layers, layers, nb_couplings, couplings_links, nb_com, cross_communities, intra_coms):
	f = open(directory + "/new_format", 'w')

	#nb of layers
	f.write(str(nb_layers) + '\n')

	for i in range(0, nb_layers):
		# nodes of layer i
		f.write(" ".join(layers[i]['nodes']) + '\n')

		filelayer = directory + "/layer" + str(i) + "/network.dat"
		# edges of layer i
		edges = []
		with open(filelayer, 'r') as file:
			for line in file:
				line = line.replace("\n", "").split(separator)

				edges.append((line[0], line[1]))


		f.write(str(len(edges)) + '\n')
		for e1, e2 in edges:
			f.write(e1 + ' ' + e2 + '\n')

	#nb couplings
	f.write(str(len(couplings_links)) + '\n')
	
	# coupling edges
	for l1 in couplings_links:
		for l2 in couplings_links[l1]:
			f.write(str(l1) + ' ' + str(l2) + '\n')

			f.write(str(len(couplings_links[l1][l2])) + '\n')
			for e1, e2 in couplings_links[l1][l2]:
				f.write(e1 + ' ' + e2 + '\n')

	# nb of community 
	f.write(str(nb_com) + '\n')
	
	for list_coms in cross_communities:
		for index_com in list_coms:
			for i in range(0, nb_layers):
				if index_com in layers[i]['com_nodes']:
					f.write(" ".join(layers[i]['com_nodes'][index_com]))
					break
			f.write(' ')
		f.write('\n')

	for i in range(0, nb_layers):
		for index_com in intra_coms[i]:
			f.write(" ".join(layers[i]['com_nodes'][index_com]) + '\n')

	f.close()

def usage():
	print "Usage : ./lfr_multilayer <outdir> <nb_layers> <INTRA> <INTER>"
	print "--------------------------------------"
	print "outdir : choose a directory where will be stored the multilayer network"
	print "nb_layers : number of layers of the multilayer network"
	print "---------------INTRA---------------"
	print "Intralayer parameters (over all layers) :"
	print "-n : number of nodes"
	print "-k : average degree"
	print "-maxk : maximum degree"
	print "-mu : mixing parameter"
	print "---------------INTER---------------"
	print "-p : set p to control fraction of interlayer edges (coupling links) within community"
	print "-a : set alpha parameter to control fraction of multilayer communities, 0.0  "
	print "-d : set density of interlayers edges"

def main(argv):
	if len(argv) != 16:
		usage()
		sys.exit(1)

	dict_intra_params = {}
	dict_inter_params = {}
	outdir = ""
	nb_layers = -1

	skip = False
	for i in range(0, len(argv)):
		if skip:
			skip = False
			continue

		if i == 0:
			outdir = argv[0]
		elif i == 1:
			nb_layers = int(argv[1])
		else:
			skip = True
			if argv[i] == "-n":
				dict_intra_params['n'] = int(argv[i+1])
			elif argv[i] == "-k":
				dict_intra_params['k'] = float(argv[i+1])
			elif argv[i] == "-maxk":
				dict_intra_params['maxk'] = int(argv[i+1])
			elif argv[i] == "-mu":
				dict_intra_params['mu'] = float(argv[i+1])
			elif argv[i] == "-p":
				dict_inter_params['p'] = float(argv[i+1])
			elif argv[i] == "-a":
				dict_inter_params['a'] = float(argv[i+1])
			elif argv[i] == "-d":
				dict_inter_params['d'] = float(argv[i+1])
			elif argv[i] == "-h":
				usage()
				sys.exit(1)
			else:
				print "%s parameter is unknown" % argv[i]
				sys.exit(1)


	layers = create_layers(outdir, nb_layers, dict_intra_params)
	# store in layers nodes for communities
	for i in range(0, nb_layers):
		load_com_nodes(i, outdir, layers)

	cross_communities, intra_coms, nb_intra_coms =  create_cross_layer_communities(nb_layers, layers, dict_inter_params['a'])
	nb_com = len(cross_communities) + nb_intra_coms

	couplings_links = create_coupling_links(nb_layers, layers, dict_inter_params['d'])

	# modify coupling links
	nb_link_inside_cross_coms, nb_link_outside_cross_coms = apply_p_parameter(nb_layers, layers, couplings_links, cross_communities, dict_inter_params['p'])
	#nb_couplings = nb_link_inside_cross_coms + nb_link_outside_cross_coms

	nb_couplings = 0
	f = open(outdir + "/couplings", 'w')
	for i in range(0, nb_layers-1):
		for (index_node1, index_node2) in couplings_links[i][i+1]:
			f.write(index_node1 + ' ' + index_node2 + '\n')
			nb_couplings += 1
	f.close()

	write_soum_format(outdir, nb_layers, layers, nb_couplings, couplings_links, nb_com, cross_communities, intra_coms)

	print "Statistics :"
	print "Nb of cross layer com : %i" % len(cross_communities)
	print "Nb of intra layer com : %i" % nb_intra_coms
	print "Nb coupling links : %i" % nb_couplings
	print "Interlayer density : %f" % (1.0 * nb_couplings / (pow(dict_intra_params['n'], 2) * (nb_layers-1)))

if __name__  == "__main__":
	main(sys.argv[1:])
