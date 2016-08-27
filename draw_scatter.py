#!/usr/bin/python

import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab, math

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

def mean(dico_x, dico_y):
        dico_avg = {}
        sum_values = {}
        count_values = {}

        for (k1,v1) in dico_x.items():
                if k1 in dico_y:
                        if v1 not in sum_values:
                                sum_values[v1] = pow(float(dico_y[k1]), 2)
                                count_values[v1] = 1
                        else:
                                sum_values[v1] += pow(float(dico_y[k1]), 2)
                                count_values[v1] += 1

        for v1,sum_v2 in sum_values.items():
                dico_avg[v1] = math.sqrt(1.0 * sum_v2 / count_values[v1])

        return dico_avg

def root_mean_square(dico_x, dico_y):
        dico_avg = {}
        sum_values = {}
        count_values = {}

        for (k1,v1) in dico_x.items():
                if k1 in dico_y:
                        if v1 not in sum_values:
                                sum_values[v1] = float(dico_y[k1])
                                count_values[v1] = 1
                        else:
                                sum_values[v1] += float(dico_y[k1])
                                count_values[v1] += 1

        for v1,sum_v2 in sum_values.items():
                dico_avg[v1] = 1.0 * sum_v2 / count_values[v1]  

        return dico_avg

def harmonic_mean(dico_x, dico_y):
        dico_avg = {}
        sum_values = {}
        count_values = {}

        for (k1,v1) in dico_x.items():
                if k1 in dico_y and float(dico_y[k1]) > 0.0:
                        if v1 not in sum_values:
                                sum_values[v1] = 1.0 / float(dico_y[k1])
                                count_values[v1] = 1
                        else:
                                sum_values[v1] += 1.0 / float(dico_y[k1])
                                count_values[v1] += 1

        for v1,sum_v2 in sum_values.items():
                dico_avg[v1] = 1.0 * count_values[v1] / sum_v2

        return dico_avg

def draw_avg(datafile, dico_x, dico_y):
        figure = pylab.figure(figsize=(13,10), dpi=80)
        
        pylab.xscale("log")
        #pylab.yscale("log")
        pylab.ylim([0.0, 1.0])

        #dico_avg = mean(dico_x, dico_y)
        dico_avg = root_mean_square(dico_x, dico_y)
        #dico_avg = harmonic_mean(dico_x, dico_y)

        plot_parameters = dict(linestyle="", marker="s", markersize=8, linewidth=2.5, color="red")
        pylab.plot(dico_avg.keys(), dico_avg.values(), **plot_parameters)
        figure.savefig(datafile + "_avg_scatter.png")
        pylab.close(figure)


def main(argv):
        file_x = argv[0]
        file_y = argv[1]

        dico_x = load_dico(file_x)
        dico_y = load_dico(file_y)

        #draw(file_y, dico_x, dico_y)
        draw_avg(file_y, dico_x, dico_y)

if __name__  == "__main__":
        main(sys.argv[1:])
