import sys, math

filename_ground_truth_partition = sys.argv[1]
filename_calculted_partition = sys.argv[2]

def binomial_coeff(n, k):
	return 1.0 * math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


gt_part = {}
list_elements = []
with open(filename_ground_truth_partition, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_part = line.pop(0)
		gt_part[id_part] = set(line)
		for e in line:
			list_elements.append(e)

cal_part = {}
with open(filename_calculted_partition, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_part = line.pop(0)
		cal_part[id_part] = set(line)

confusion_matrix = {}
for id_part1 in gt_part:
	confusion_matrix[id_part1] = {}
	for id_part2 in cal_part:
		inter = gt_part[id_part1].intersection(cal_part[id_part2])
		confusion_matrix[id_part1][id_part2] = len(inter)

t1 = 0
for id_part1 in gt_part:
	if len(gt_part[id_part1]) > 1:
		t1 += binomial_coeff(len(gt_part[id_part1]), 2)

t2 = 0
for id_part2 in cal_part:
	if len(cal_part[id_part2]) > 1:
		t2 += binomial_coeff(len(cal_part[id_part2]), 2)

t3 = (2.0*t1*t2) / (len(list_elements) * (len(list_elements) - 1))

sum_binomial = 0
for id_part1 in gt_part:
	for id_part2 in cal_part:
		if confusion_matrix[id_part1][id_part2] > 1:
			sum_binomial += binomial_coeff(confusion_matrix[id_part1][id_part2], 2)

adjusted_rand_index = 1.0 * (sum_binomial - t3) / ((0.5 * (t1 + t2)) - t3)

print adjusted_rand_index