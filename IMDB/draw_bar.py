#!/usr/bin/python

import matplotlib, numpy
matplotlib.use("Agg")
import os, ast, operator, sys, pylab

filename = sys.argv[1]
attribute = {}

with open(filename, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		film = line.pop(0)

		for att in line:
			attribute.setdefault(att, 0)
			attribute[att] += 1

file = open(filename + ".distrib", 'w')
for att in attribute:
	file.write(att + " " + str(attribute[att]) + '\n')
file.close()

data = attribute.values()
atts = attribute.keys()

margin = 1.0

y_pos = numpy.arange(0, len(attribute) * margin, margin)

fig, ax = pylab.subplots(figsize=(13,10), dpi=80)


ax.barh(y_pos, data, align='center', alpha=0.8)
pylab.yticks(y_pos, atts)

for tick in ax.yaxis.get_major_ticks():
	tick.label.set_fontsize(8)

fig.savefig(filename + "_distribution.png")
pylab.close(fig)