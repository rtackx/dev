import sys

filename_bip = sys.argv[1]

top_nodes = {}
str_top_nodes = {}
str_bot_nodes = {}

louvain = False
bisbm = False
infomap = True

if bisbm:
	index = 1
	index_bot = 0
else:
	index = 0
	index_bot = 0

if louvain or infomap:
	with open(filename_bip, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			top = line.pop(0)		
			index_top = index

			top_nodes[index_top] = []
			
			str_top_nodes[top] = index_top

			for bot in line:			
				if bot not in str_bot_nodes:
					if louvain:
						index += 1
						str_bot_nodes[bot] = index
					elif infomap:
						str_bot_nodes[bot] = index_bot
						index_bot += 1

				top_nodes[index_top].append(str_bot_nodes[bot])

			index += 1
elif bisbm:
	with open(filename_bip, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			top_nodes[index] = []
			top = line[0]
			str_top_nodes[top] = index

			index += 1

	index_bot = index
	with open(filename_bip, 'r') as file:
		for line in file:

			line = line.replace("\n", "").split()
			top = line.pop(0)
			index_top = str_top_nodes[top]

			for bot in line:
				if bot not in str_bot_nodes:
					str_bot_nodes[bot] = index_bot
					index_bot += 1

				top_nodes[index_top].append(str_bot_nodes[bot])



f = open(filename_bip + '_num', 'w')
for top in top_nodes:
	f.write(str(top))
	for bot in top_nodes[top]:
		f.write(' ' + str(bot))
	f.write('\n')
f.close()


if louvain or bisbm:
	f = open(filename_bip + '_num.adjency', 'w')
	for top in str_top_nodes:
		index_top = str_top_nodes[top]
		for index_bot in top_nodes[index_top]:
			f.write(str(index_top) + " " + str(index_bot) + "\n")
	f.close()
elif infomap:
	f = open(filename_bip + '_num.adjency', 'w')
	for i in range(0, len(top_nodes)):
		for bot in top_nodes[i]:
			f.write("f" + str(i) + ' ' + "n" + str(bot) + '\n')
	f.close()

if bisbm:
	# type file for biSBM algo)
	f = open(filename_bip + '_num.vertexType', 'w')
	for i in range(0, index_top):
		f.write("1\n")
	for i in range(0, index_bot):
		f.write("2\n")
	f.close()

f = open(filename_bip + '_table_num', 'w')
for top in str_top_nodes:
	f.write(top + " " + str(str_top_nodes[top]) + '\n')
"""for bot in str_bot_nodes:
	f.write(bot + " " + str(str_bot_nodes[bot]) + '\n')"""
f.close()