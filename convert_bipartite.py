#!/usr/bin/python
import getopt, sys, os

def usage():
	usage = "Usage : convert_bipartite <OPTION> <output_dataset>\n"
	usage += "Option\tLong option\tDescription\n"
	usage += "-h\t--help\t\tDisplay this message\n"
	usage += "-a\t--adjacency\tConvert a adjacency graph <FILE> into a bipartite graph\n"
	usage += "-b\t--bipartite\tConvert a bipartite graph <FILE> into a adjacency graph\n"
	usage += "-p\t--projection\tConvert a adjacency graph <FILE> remplacing strings by numbers\n"
	#usage += "-t\t--type\t\tIndicate if the data file contains identifiers (usually the node ID) at the beginning of each line <Default 0[NO], 1[YES]>\n"
	print usage

def create_projection(adj_graph, projection=True):
	list_top_nodes = {}
	list_bot_nodes = {}
	list_nodes = {}
	index = 0
	
	f = open(adj_graph + ".corresp", 'w')

	with open(adj_graph, 'r') as f_adj_graph:
		for line in f_adj_graph:
			if "%" not in line:
				line = line.replace("\n", "").split()

				if projection:
					if line[0] not in list_nodes:
						list_nodes[line[0]] = str(index)
						f.write(str(index) + " " + line[0] + "\n")
						index += 1
					if line[1] not in list_nodes:
						list_nodes[line[1]] = str(index)
						f.write(str(index) + " " + line[1] + "\n")
						index += 1
				else:# pour biparti
					if line[0] not in list_top_nodes:
						list_top_nodes[line[0]] = str(index)
						f.write(str(index) + " " + line[0] + "\n")
						index += 1
					if line[1] not in list_bot_nodes:
						list_bot_nodes[line[1]] = str(index)
						f.write(str(index) + " " + line[1] + "\n")
						index += 1

	f.close()
	f = open(adj_graph + ".adjency_ww", 'w')

	with open(adj_graph, 'r') as f_adj_graph:
		for line in f_adj_graph:
			if "%" not in line:
				line = line.split()

				if projection:
					f.write(list_nodes[line[0]] + " " + list_nodes[line[1]])					
				else:
					f.write(list_top_nodes[line[0]] + " " + list_bot_nodes[line[1]])

				if len(line) == 3:
					f.write(" " + line[2])
				f.write("\n")

	f.close()

def create_bipartite(adj_graph, reversed = False):
	list_nodes = {}

	with open(adj_graph, 'r') as f_adj_graph:
		for line in f_adj_graph:
			if "%" not in line:
				nodes = line[:-1].split()

				'''if reversed:
					if nodes[1] not in list_nodes:
						list_nodes[nodes[1]] = []
					# Avoid multiple edges
					if nodes[0] not in list_nodes[nodes[1]]:
						list_nodes[nodes[1]].append(nodes[0])
				else:
				'''
				if nodes[0] not in list_nodes:
					list_nodes[nodes[0]] = []
				# Avoid multiple edges
				#if nodes[1] not in list_nodes[nodes[0]]:
				list_nodes[nodes[0]].append(nodes[1])

	
	name = "bipartite"
	if reversed:
		name = "reversed_" + name

	with open(adj_graph + "." + name, 'w') as f_graph_bip:
		for node in list_nodes:
			f_graph_bip.write(str(node) + ' ' + ' '.join(list_nodes[node]) + '\n')

def create_adjacency(bip_graph):
	list_nodes = {}
	i = 0

	f = open(bip_graph + ".adjacency", 'w')

	with open(bip_graph, 'r') as f_bip_graph:
		for line in f_bip_graph:
			line = line.split()

			index_top = line[0]
			line.pop(0)

			for l in line:
				f.write(str(index_top) + ' ' + str(l) + '\n')

	f.close()

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ha:b:t:p:", ["help", "adjacency=", "bipartite=", "projection="])
	except getopt.GetoptError, e:
		usage()
		print "Error >>> %s" % str(e)
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif opt in ("-a", "--adjacency"):
			create_bipartite(arg)
		elif opt in ("-b", "--bipartite"):
			create_adjacency(arg)
		elif opt in ("-p", "--projection"):
			create_projection(arg)
		else:
			sys.exit(1)