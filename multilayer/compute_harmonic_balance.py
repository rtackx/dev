import sys, math

filename_community = sys.argv[1]

# indexes of type1 nodes ranged from [0;80165]
# whole network : yelp
#index_type1 = 80165
#index_type2 = 97520
# giant component : yelp
index_type1 = 77669
index_type2 = 95021

nb_total_type1 = index_type1 + 1
nb_total_type2 = index_type2 - index_type1

if nb_total_type1 > nb_total_type2:
	prop_total = 1.0 * nb_total_type2 / nb_total_type1
elif nb_total_type2 > nb_total_type1:
	prop_total = 1.0 * nb_total_type1 / nb_total_type2
else:
	prop_total = 1.0

print "Inde range type1 : [0 ; " + str(index_type1) + "]"
print "Inde range type1 : [" + str(index_type1 + 1) + " ; " + str(index_type2) + "]"
print "Nb type1 " + str(nb_total_type1)
print "Nb type2 " + str(nb_total_type2)

harmonic_balance = {}

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

			size_com = nb_type1 + nb_type2

			'''if nb_type1 > nb_type2:
				prop_1 = 1.0 * nb_type2 / nb_type1
				prop_2 = 1.0 * nb_total_type2 / nb_total_type1
				max_type = nb_type1
			elif nb_type2 > nb_type1:
				prop_1 = 1.0 * nb_type1 / nb_type2
				prop_2 = 1.0 * nb_total_type1 / nb_total_type2
				max_type = nb_type2
			else:
				prop_1 = 1.0
				prop_2 = prop_total
				max_type = nb_type1

			prop = 1.0 * prop_1 / prop_2
			balance = 1.0 * (max_type - prop) / size_com
			balance_norm = (1 - balance) / 0.5'''
			
			balance_norm = 1.0 * min(nb_type1, nb_type2) / max(nb_type1, nb_type2)

			harmonic_balance[id_com] = (balance_norm, size_com)

file_out = open(filename_community + ".harmonic_balance", 'w')
file_out.write("#ID_COM   HARM_BALANCE   SIZE_COM\n")
for id_com in harmonic_balance:
	file_out.write(id_com + " " + str(harmonic_balance[id_com][0]) + " " + str(harmonic_balance[id_com][1]) + "\n")
file_out.close()