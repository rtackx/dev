import sys
import igraph

def load(filename):
	data = {}

	with open(filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			id_com = line.pop(0)
			data[int(id_com)] = line

	return data

def shape_to_membership(com):
	overlap = 0

	membership_nodes = {}
	for id_com in com:
		for id_node in com[id_com]:
			if int(id_node) in membership_nodes:
				overlap += 1
			else:
				membership_nodes[int(id_node)] = id_com

	print "Nb of overlap : " + str(overlap)
	list_id_nodes = membership_nodes.keys()
	list_id_nodes.sort()

	membership_coms = []
	for id_node in list_id_nodes:
		membership_coms.append(membership_nodes[id_node])
	print len(membership_nodes)
	return membership_coms


filename_com1 = sys.argv[1]
filename_com2 = sys.argv[2]

coms1 = load(filename_com1)
coms2 = load(filename_com2)

membership_com1 = shape_to_membership(coms1)
membership_com2 = shape_to_membership(coms2)

r = igraph.compare_communities(membership_com1, membership_com2, method="nmi")
print r

