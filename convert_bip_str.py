import sys

filename_bip = sys.argv[1]

top_nodes = {}
str_top_nodes = {}
str_bot_nodes = {}

louvain = False

index = 0
index_bot = 0

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
				else:
					str_bot_nodes[bot] = index_bot
					index_bot += 1

			top_nodes[index_top].append(str_bot_nodes[bot])

		index += 1

f = open(filename_bip + '_num', 'w')
for top in top_nodes:
	f.write(str(top))
	for bot in top_nodes[top]:
		f.write(' ' + str(bot))
	f.write('\n')
f.close()

f = open(filename_bip + '_num.adjency', 'w')
for i in range(0, len(top_nodes)):
	for bot in top_nodes[i]:
		f.write("f" + str(i) + ' ' + "n" + str(bot) + '\n')
f.close()


f = open(filename_bip + '_table_num', 'w')
for top in str_top_nodes:
	f.write(top + " " + str(str_top_nodes[top]) + '\n')
"""for bot in str_bot_nodes:
	f.write(bot + " " + str(str_bot_nodes[bot]) + '\n')"""
f.close()