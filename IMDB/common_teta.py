import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab, numpy

file_coms = sys.argv[1]
file_attr = sys.argv[2]

coms = {}
with open(file_coms, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()
		
		com_id = line.pop(0)
		'''if len(line) == 1:
			continue'''
		coms[com_id] = line

attr = {}
with open(file_attr, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		film_name = line.pop(0)
		attr[film_name] = line


herf_common_teta = {}
herf_multi_common_teta = {}
herf_maj_common_teta = {}

for common_teta in numpy.arange(0.0, 1.0, 0.01):
	herf_common_teta[common_teta] = {}
	herf_multi_common_teta[common_teta] = {}
	herf_maj_common_teta[common_teta] = {}

	for id_com in coms:
		herf_common_teta[common_teta][id_com] = 0.0
		herf_multi_common_teta[common_teta][id_com] = 0.0
		herf_maj_common_teta[common_teta][id_com] = 0.0

		if len(coms[id_com]) == 1:
			continue

		distrib_attr = {}
		total = 0

		for film_name in coms[id_com]:
			if film_name not in attr:
				continue

			for att in attr[film_name]:
				distrib_attr.setdefault(att, 0)
				distrib_attr[att] += 1
				total += 1

		list_eligible = []
		total_common = 0

		for att in distrib_attr:
			common = 1.0 * distrib_attr[att] / total# len(distrib_attr)
			
			if common >= common_teta:
				total_common += distrib_attr[att]
				list_eligible.append(att)

		''' classic herfindhal value '''
		
		'''for att in list_eligible:
			herf_common_teta[common_teta][id_com] += pow(1.0 * distrib_attr[att] / total_common, 2)'''
		
		for att in list_eligible:
			herf_common_teta[common_teta][id_com] += pow(1.0 * distrib_attr[att] / len(coms[id_com]), 2)

		if herf_common_teta[common_teta][id_com]:
			herf_common_teta[common_teta][id_com] /= len(list_eligible)

		''' herfindhal value with multi attributes '''
		'''multi_att = {}
		total_multi = 0
		for film_name in coms[id_com]:
			if film_name not in attr:
				continue

			list_att = []
			for att in attr[film_name]:
				if att in list_eligible:
					list_att.append(att)
			if len(list_att) == 0:
				continue
			joint_att = "_".join(list_att)

			if joint_att not in multi_att:
				multi_att[joint_att] = 0				
			multi_att[joint_att] += 1
			total_multi += 1

		for joint_att in multi_att:
			herf_multi_common_teta[common_teta][id_com] += pow(1.0 * multi_att[joint_att] / total_multi, 2)'''

		''' herfindhal value with major attributes '''
		'''list_attr_max = {}
		for film_name in coms[id_com]:
			if film_name not in attr:
				continue

			n_max = 0
			att_max = ""
			for att in attr[film_name]:
				if att not in list_eligible:
					continue

				if distrib_attr[att] > n_max:
					n_max = distrib_attr[att]
					att_max = att

			if n_max > 0:
				list_attr_max[film_name] = att_max

		attr_com = {}
		total_maj = 0

		for film_name in list_attr_max:
			attr_com.setdefault(list_attr_max[film_name], 0)
			attr_com[list_attr_max[film_name]] += 1
			total_maj += 1

		for att in attr_com:
			herf_maj_common_teta[common_teta][id_com] += pow(1.0 * attr_com[att] / total_maj, 2)'''


list_mean = []
f = open(file_attr + ".common_teta", 'w')
for common_teta in herf_common_teta:
	mean = numpy.mean(herf_common_teta[common_teta].values())
	f.write(str(common_teta) + " " + str(mean) + "\n")
	list_mean.append((common_teta, mean))
f.close()

'''list_mean_multi = []
for common_teta in herf_multi_common_teta:
	mean = numpy.mean(herf_multi_common_teta[common_teta].values())
	list_mean_multi.append((common_teta, mean))

list_mean_maj = []
for common_teta in herf_maj_common_teta:
	mean = numpy.mean(herf_maj_common_teta[common_teta].values())
	list_mean_maj.append((common_teta, mean))'''

figure = pylab.figure(figsize=(13,10), dpi=80)
#pylab.xscale("log")
#pylab.ylim([0.0, 1.0])
pylab.xlabel('Common teta')
pylab.ylabel('Herfindahl')

data = zip(*list_mean)
data_x = data[0]
data_y = data[1]
plot_parameters = dict(linestyle="", marker="s", markersize=8, linewidth=2.5, color="red")
pylab.plot(data_x, data_y, **plot_parameters)

'''data = zip(*list_mean_multi)
data_x = data[0]
data_y = data[1]
plot_parameters = dict(linestyle="", marker="s", markersize=6, linewidth=1.5, color="green")
pylab.plot(data_x, data_y, **plot_parameters)

data = zip(*list_mean_maj)
data_x = data[0]
data_y = data[1]
plot_parameters = dict(linestyle="", marker="s", markersize=4, linewidth=1.3, color="yellow")
pylab.plot(data_x, data_y, **plot_parameters)'''

figure.savefig(file_attr + "_common_teta_plot.png")
pylab.close(figure)