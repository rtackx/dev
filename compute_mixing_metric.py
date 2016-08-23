import sys, math

filename_community = sys.argv[1]

# indexes of type1 nodes ranged from [0;80165]
# whole network : yelp
index_type1 = 80165
# giant comp : yelp
#index_type1 = 77670

com_similarity_distance = {}

with open(filename_community, 'r') as file:
	for line in file:
			line = line.replace('\n', '').split()

			id_com = line.pop(0)

			nb_type1 = 0
			nb_type2 = 0

			for index in line:
				if int(index) > index_type1:
					nb_type2 += 1
				else:
					nb_type1 += 1

			size = nb_type1 + nb_type2
			m = max(nb_type1, nb_type2)

			sim_dist = 1.0 - (m / (1.0 * size))
			sim_dist = sim_dist / 0.5

			'''if nb_type1 == nb_type2:
				sim_dist = 1.0
			else:
				sim_dist = 1.0 - (math.sqrt(nb_type1**2 + nb_type2**2) / size)'''

			com_similarity_distance[id_com] = (sim_dist, size)

file_out = open(filename_community + ".sim_dist", 'w')
file_out.write("#ID_COM   SIM_DIST   SIZE_COM\n")
for id_com in com_similarity_distance:
	file_out.write(id_com + " " + str(com_similarity_distance[id_com][0]) + " " + str(com_similarity_distance[id_com][1]) + "\n")
file_out.close()