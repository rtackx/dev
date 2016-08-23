#!/usr/bin/python

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
	data = {}
	with open(datafile, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()
			if "-1.0" not in line[1]:
				data[line[0]] = num(line[1])

	return data

def get_distribution(data):
	distribution = {}
	for (id_node, value) in data.iteritems():
		if value in distribution:
			distribution[value] += 1
		else:
			distribution[value] = 1

	return distribution

def get_inverse_distribution(distribution, total):
	sorted_distribution = sorted(distribution.iteritems(), key=operator.itemgetter(0), reverse=True)
	cumulative = 0

	inverse_distribution = {}
	for (value, count) in sorted_distribution:
		cumulative += count
		inverse_distribution[value] = cumulative / float(total)

	return inverse_distribution

def draw(datafile, dictionnary):
	datafile = datafile.replace(".data", "")

	figure = pylab.figure(figsize=(13,10), dpi=80)
	fct_formatter = matplotlib.ticker.FuncFormatter(to_percent)
	pylab.gca().yaxis.set_major_formatter(fct_formatter)
	#pylab.xscale("log")
	pylab.ylim([0.0, 1.0])
	plot_parameters = dict(linestyle="-", marker="s", markersize=8, linewidth=2.5, color="red")

	data = zip(*sorted(dictionnary.iteritems(), key=operator.itemgetter(0), reverse=False))
	pylab.plot(data[0], data[1], **plot_parameters)

	figure.savefig(datafile + "_distribution.png")
	pylab.close(figure)

def usage():
	usage = "Usage : draw_distribution.py <OPTION> <FILE>\n"
	usage += "Option\tDescription\n"
	usage += "-h\tDisplay this message\n"
	usage += "-f\tDraw distribution for data file (.data) <FILE>\n"
	usage += "-d\tDraw distribution for each data file (.data) in <FILE> directory\n"
	print usage

def treat_file(datafile):
	#if not datafile.endswith(".data"):
	#	return

	print "\t\t[Drawing distribution " + datafile + "]"
	
	data = read_datafile(datafile)
	if len(data) == 0:
		return

	distribution = get_distribution(data)
	inverse_distribution = get_inverse_distribution(distribution, len(data))
	draw(datafile, inverse_distribution)

def main(argv):
	if "-f" == argv[0]:
		treat_file(argv[1])
	elif "-d" == argv[0]:
		if os.path.isdir(argv[1]):			
			for f in os.listdir(argv[1]):
				treat_file(argv[1] + "/" + f)
		else:
			print "'" + argv[1] + "' is not a directory"
			usage()
	else:
		usage()

if __name__  == "__main__":
	main(sys.argv[1:])
