import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab

def to_percent(y, position):
	    s = str(100 * y)

	    if pylab.rcParams['text.usetex'] == True:
	        return s + r'$\%$'
	    else:
	        return s + '%'

def num(s):
	return ast.literal_eval(s)

def read_datafile(datafile):
	data1 = {}
	data2 = {}
	with open(datafile, 'r') as file:
		for line in file:
			if line[0] == '#':
				continue
			line = line.replace("\n", "").split()
			# sim dist
			data1[line[0]] = num(line[1])
			# size com
			data2[line[0]] = num(line[2])

	return data1, data2

def get_distribution(data):
	distribution = {}
	distribution_coms = {}
	for (id_node, value) in data.iteritems():
		if value in distribution:
			distribution[value] += 1
			distribution_coms[value].append(id_node)
		else:
			distribution[value] = 1
			distribution_coms[value] = [id_node]

	return distribution, distribution_coms

def get_inverse_distribution(distribution, total):
	sorted_distribution = sorted(distribution.iteritems(), key=operator.itemgetter(0), reverse=True)
	cumulative = 0
	
	inverse_distribution = {}
	for (value, count) in sorted_distribution:
		cumulative += count
		inverse_distribution[value] = cumulative / float(total)

	return inverse_distribution

def draw_dist(datafile, dictionnary, nb_element, distribution_coms, data_size_com):
	datafile = datafile.replace(".data", "")

	figure = pylab.figure(figsize=(13,10), dpi=80)
	fct_formatter = matplotlib.ticker.FuncFormatter(to_percent)
	pylab.gca().yaxis.set_major_formatter(fct_formatter)

	plot_parameters = dict(linestyle="--", linewidth=1.5, color="red")
	scatter_parameters = dict(marker="s", color="blue")
	data = zip(*sorted(dictionnary.iteritems(), key=operator.itemgetter(0), reverse=False))

	data3 = []
	for key in sorted(distribution_coms):
		nb = 0
		for id_com in distribution_coms[key]:
			nb += data_size_com[id_com]
		data3.append(nb)

	dmax = max(data3)
	dmin = min(data3)
	size_max = 70 
	size_min = 25
	size_norm = []

	if len(data3) == 1:
		size_norm.append(70)
	else:
		for size in data3:
			size_norm.append(size_min + (((size - dmin) * (size_max - size_min) / (dmax - dmin) * 1.0)))

	pylab.plot(data[0], data[1], **plot_parameters)
	pylab.scatter(data[0], data[1], s=size_norm, **scatter_parameters)

	pylab.annotate(str(data3[0]), xy=(data[0][0],data[1][0]), xytext=(data[0][0]+0.01,data[1][0]-0.03))
	for i in range(1,len(data[0])):
		pylab.annotate(str(data3[i]), xy=(data[0][i],data[1][i]), xytext=(data[0][i]+0.013,data[1][i]+0.01))

	pylab.ylabel('Percentage of community', fontsize=18)
	pylab.xlabel('Mixing similarity', fontsize=18)
	pylab.title('Nb of communites : ' + str(nb_element), fontsize=25)
	pylab.ylim([0.0, 1.0])
	pylab.xlim([0.0, 1.0])

	figure.savefig(datafile + "_distribution.png")
	pylab.close(figure)

def draw_scatter(datafile, data1, data2):
	datafile = datafile.replace(".data", "")
	figure = pylab.figure(figsize=(13,10), dpi=80)
	
	pylab.xscale("log")
	plot_parameters = dict(linestyle="", marker="s", markersize=8, linewidth=2.5, markeredgecolor="green", color="red")

	data_size = data2.values()
	data_coeff = data1.values()

	pylab.xlabel('Mixing similarity')
	pylab.ylabel('Size of community')
	pylab.title('Nb of communites : ' + str(len(data1)))

	pylab.plot(data_size, data_coeff, **plot_parameters)

	figure.savefig(datafile + "_scatter.png")
	pylab.close(figure)

def main(argv):
	filename = argv[0]
	data1, data2 = read_datafile(filename)

	data1_dist, distribution_coms = get_distribution(data1)
	data1_inv_dist = get_inverse_distribution(data1_dist, len(data1))
	draw_dist(filename, data1_inv_dist, len(data1), distribution_coms, data2)
	
	draw_scatter(filename, data1, data2)


if __name__  == "__main__":
	main(sys.argv[1:])
