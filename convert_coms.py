import sys

filename_coms = sys.argv[1]
filename_table_num = sys.argv[2]

coms_indexed = False

table_nums = {}
with open(filename_table_num, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		table_nums[line[1]] = line[0]


f = open(filename_coms + "_labeled", 'w')

index_com = 1

with open(filename_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		for i in range(0, len(line)):
			if i == 0:
				if coms_indexed:					
					f.write(line[0])
				else:
					f.write(str(index_com))
					index_com += 1
			else:
				f.write(' ' + table_nums[line[i]])
		f.write('\n')

f.close()



