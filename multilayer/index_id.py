import sys

filename = sys.argv[1]
index1 = int(sys.argv[2])

if len(sys.argv) == 4:
	sep = sys.argv[3]
else:
	sep = " "

cat1 = {}
#index1 = 0
#index1 = 77670

#sep = ' '
prefix = ""
with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split(sep)

		id1 = line[0]
		id2 = line[1]

		if id1 not in cat1:
			cat1[id1] = prefix + str(index1)
			index1 += 1
		if id2 not in cat1:
			cat1[id2] = prefix + str(index1)
			index1 += 1
print index1

filename_corresp1 = filename + ".index1"
file_corresp1 = open(filename_corresp1, 'w')
for id1 in cat1:
	file_corresp1.write(id1 + " " + cat1[id1] + " \n")
file_corresp1.close()

filename_indexed = filename + ".indexed"
file_indexed = open(filename_indexed, 'w')
with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split(sep)

		file_indexed.write(cat1[line[0]] + " " + cat1[line[1]])
		if len(line) == 3:
			file_indexed.write(" " + line[2])
		file_indexed.write('\n')

file_indexed.close()