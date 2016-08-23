import sys

def load_corresp(filename_corresp):
	cat = {}

	with open(filename_corresp, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()
			
			cat[line[0]] = line[1]

	return cat


filename = sys.argv[1]
filename_index_corresp1 = sys.argv[2]
filename_index_corresp2 = sys.argv[3]

if len(sys.argv) == 5:
	sep = sys.argv[4]
else:
	sep = " "

cat1 = load_corresp(filename_index_corresp1)
cat2 = load_corresp(filename_index_corresp2)

filename_corresp = filename + ".indexed"
file_corresp = open(filename_corresp, 'w')

with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split(sep)

		error = False
		if line[0] not in cat1:
			error = True
			#print line[0] + " doesn't exist (" + filename_index_corresp1 + ")"
		if line[1] not in cat2:
			error = True
			#print line[1] + " doesn't exist (" + filename_index_corresp2 + ")"

		if not error:
			file_corresp.write(cat1[line[0]] + " " + cat2[line[1]])
			if len(line) == 3:
				file_corresp.write(" " + line[2])
			file_corresp.write('\n')
file_corresp.close()