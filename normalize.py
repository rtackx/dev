import sys
import numpy as np

filename = sys.argv[1]

weights = []

with open(filename, 'r') as file:
	for line in file:
			line = line.replace('\n', '').split()
			weights.append(float(line[2]))

np_weights = np.array(weights)
mean = np.mean(np_weights)
var = np.var(np_weights)
std = np.std(np_weights)
#min = np.min(np_weights)
min = 0
max = np.max(np_weights)

outfile = open(filename + "_norm", 'w')
with open(filename, 'r') as file:
	for line in file:
			line = line.replace('\n', '').split()
			#norm = abs(float(line[2]) - mean) / (1.0 * std)
			norm = (float(line[2]) - min) / (max - min)
			outfile.write(line[0] + " " + line[1] + " " + str(norm) + "\n")

outfile.close()