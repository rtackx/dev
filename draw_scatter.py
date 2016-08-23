#!/usr/bin/python

import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab

def load_dico(file):
        dico = {}

        with open(file, 'r') as file:
                for line in file:
                        line = line.replace("\n", "").split()

                        dico[line[0]] = line[1]

        return dico

def draw(datafile, dico_x, dico_y):
        figure = pylab.figure(figsize=(13,10), dpi=80)
        
        #pylab.xscale("log")
        #pylab.ylim([0.0, 1.0])

        plot_parameters = dict(linestyle="", marker="s", markersize=8, linewidth=2.5, color="red")

        data_x = zip(*sorted(dico_x.iteritems(), key=operator.itemgetter(0), reverse=False))
        data_y = zip(*sorted(dico_y.iteritems(), key=operator.itemgetter(0), reverse=False))

        pylab.plot(data_x[1], data_y[1], **plot_parameters)

        figure.savefig(datafile + "_scatter.png")
        pylab.close(figure)

def main(argv):
        file_x = argv[0]
        file_y = argv[1]

        dico_x = load_dico(file_x)
        dico_y = load_dico(file_y)

        draw(file_y, dico_x, dico_y)

if __name__  == "__main__":
        main(sys.argv[1:])
