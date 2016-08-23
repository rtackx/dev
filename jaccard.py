import sys

def jaccard(A, B):
	return 1.0 * len(A.intersection(B)) / len(A.union(B))

def load_com(filename):
	set_of_coms = {}

	with open(filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()
			
			id_com = line.pop(0)
			set_of_coms[id_com] = set(line)

	return set_of_coms

def compute_jaccard(set_of_coms1, set_of_coms2):
	list_jaccards = []
	for id_com1 in set_of_coms1:
		sum_jaccards = 0.0
		for id_com2 in set_of_coms2:
			sum_jaccards += jaccard(set_of_coms1[id_com1], set_of_coms2[id_com2])
		list_jaccards.append(sum_jaccards)

	return 1.0 * sum(list_jaccards) / len(list_jaccards)

def get_format_filename(filename):
	format = ""

	if "louvain" in filename:
		format += "louvain_"
	else:
		format += "infomap_"
	if "giant" in filename:
		format += "[G]"
	if "typeA" in filename:
		format += "TypeA"
	else:
		format += "TypeB"
	if "weighted" in filename:
		format += "-W"
	else:
		format += "-UW"

	return format

list_set_of_coms = []
list_filename = []

for i in range(1, len(sys.argv)-1):
	list_set_of_coms.append(load_com(sys.argv[i]))
	list_filename.append(sys.argv[i])

list_mean_jaccards = []
for i in range(0, len(list_set_of_coms)):
	for j in range(i+1, len(list_set_of_coms)):
		mean_jaccards = compute_jaccard(list_set_of_coms[i], list_set_of_coms[j])

		list_mean_jaccards.append([get_format_filename(list_filename[i]),
								   get_format_filename(list_filename[j]),
								   mean_jaccards])

f = open(sys.argv[-1], 'w')
for info in list_mean_jaccards:
	f.write(info[0] + ' ' + info[1] + ' ' + str(info[2]) + '\n')
f.close()





