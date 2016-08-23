import sys

coms_file = sys.argv[1]

distrib = {}
with open(coms_file, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		
		size = len(line) - 1
		if size in distrib:
			distrib[size] += 1
		else:
			distrib[size] = 1

f = open(coms_file + ".size_distrib", 'w')
for size in sorted(distrib):
	f.write(str(size) + " " + str(distrib[size]) + '\n')
f.close()