import sys, math
import numpy as np

file_coms = sys.argv[1]
file_years = sys.argv[2]

coms = {}
movies_year = {}
min_year = 1980
max_year = 2010

with open(file_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		com_id = line.pop(0)
		if len(line) == 1:
			continue

		coms[com_id] = line

with open(file_years, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		movies_year[line[0]] = line[1]

coms_years = {}

for com_id in coms:
	coms_years[com_id] = []
	for movie in coms[com_id]:
		coms_years[com_id].append(int(movies_year[movie]))

normalized_years = {}
#https://en.wikipedia.org/wiki/Coefficient_of_variation
coeff_variation_years = {}
quartile_coeff_variation_years = {}

for com_id in coms_years:
	normalized_years[com_id] = []

	#print coms_years[com_id]

	for year in coms_years[com_id]:
		norm_year = 1.0 * (year - min_year) + 1
		normalized_years[com_id].append(norm_year)

	#print normalized_years[com_id]
	if len(normalized_years[com_id]) > 1:
		mean = 1.0 * sum(normalized_years[com_id]) / len(normalized_years[com_id])
		
		variance = 0.0
		for y in normalized_years[com_id]:
			variance += (y - mean)**2
		variance /= 1.0 * len(normalized_years[com_id])
		std = math.sqrt(variance)

		coeff_variation_years[com_id] = 1.0 * std / mean

		q1 = np.percentile(np.array(normalized_years[com_id]), 25)
		q3 = np.percentile(np.array(normalized_years[com_id]), 75)
		# 1.0 - quart_coeff => value [0.0;1.0] 1.0 is good
		quartile_coeff_variation_years[com_id] = 1.0 - (1.0 * (q3 - q1) / (q3 + q1))
		
	else:
		coeff_variation_years[com_id] = 0.0
		quartile_coeff_variation_years[com_id] = 0.0

f1 = open(file_years + ".coeff_var", 'w')
f2 = open(file_years + ".quartile_coeff_var", 'w')

for com_id in coms_years:
	f1.write(com_id + ' ' + str(coeff_variation_years[com_id]) + '\n')
	f2.write(com_id + ' ' + str(quartile_coeff_variation_years[com_id]) + '\n')

f1.close()
f2.close()

