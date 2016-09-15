import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab, numpy

display_number = 26

def load_files(herf_filename, attr_filename, coms_filename):
	# load files
	coms = {}
	movies = {}
	with open(coms_filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()
			
			com_id = line.pop(0)
			if len(line) == 1:
				continue
			coms[com_id] = line
			for film_name in line:
				movies[film_name] = com_id

	herfs = {}
	with open(herf_filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			com_id = line[0]
			herfs[com_id] = float(line[1])

	# create a dict of attributes containing values of herf for every films 
	attrs = {}
	all_attrs = {}
	corr_att = {}
	corr_att_bis = {}
	rank_corr = {}
	corr = 1
	with open(attr_filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			film_name = line.pop(0)
			
			attrs[film_name] = []
			for att in line:

				if att not in corr_att:
					corr_att[att] = corr
					corr_att_bis[corr] = att
					rank_corr[corr] = 1 
					all_attrs[corr] = []
					corr += 1
				else:
					rank_corr[corr_att[att]] += 1

				attrs[film_name].append(corr_att[att])
	

	for film_name in attrs:
		if film_name in movies:
			com_id_film = movies[film_name]
			for corr_att in attrs[film_name]:
				all_attrs[corr_att].append(herfs[com_id_film])


	sorted_rank_corr = sorted(rank_corr.items(), key=operator.itemgetter(1), reverse=True)[:display_number]

	# mean
	all_attrs_mean = {}
	for corr in all_attrs:
		all_attrs_mean[corr] = numpy.mean(all_attrs[corr])

	data = []
	data_att_name = []
	i = 1
	for k,v in sorted_rank_corr:
		data.append((i, all_attrs_mean[k]))
		data_att_name.append(corr_att_bis[k])
		i += 1

	return data, data_att_name

def plot(list_data):
	colors = ["red", "green", "blue", "cyan"]
	labels = ["Louvain", "Infomap", "GPS"]
	markers = ["s", "v", "o"]

	fig, ax = pylab.subplots(figsize=(13,10), dpi=80)
	#pylab.xscale("log")
	pylab.ylabel("Herfindahl index")
	pylab.ylim([0.0, 1.0])
	pylab.xlim([0.0, display_number+1])	
	pylab.grid(True)

	for i in range(0, len(list_data)):
		data = list_data[i][0]
		
		plot_parameters = dict(linestyle="", marker=markers[i], markersize=8, linewidth=2.5, color=colors[i])

		'''for film_name in attrs:
			if film_name in movies:
				com_id_film = movies[film_name]
				if com_id_film == "59264":
					print film_name, herfs[com_id_film]
					for att in attrs[film_name]:
						print data_att_name[att]'''

		data = zip(*data)
		data_x = data[0]
		data_y = data[1]

		for j in range(0, display_number):
			ax.plot((data_x[j], data_x[j]), (data_y[j] + 0.001, 1.0), '--', color="grey", alpha=0.5)

		ax.plot(data_x, data_y, label=labels[i], **plot_parameters)

	data_att_name = list_data[0][1]
	pylab.xticks(data_x, data_att_name)
	ax.tick_params(labelbottom='off', labeltop='on', labelsize=9)
	pylab.xticks(rotation=45)
	ax.legend(loc=3)

	fig.savefig("multiple_scatter.png")
	pylab.close(fig)

def main(argv):
	number_of_elements = int(argv[0])
	attr_filename = argv[1]

	list_data = []

	a = 2
	for i in range(0, number_of_elements):
		l = []
		herf_filename = argv[a]
		coms_filename = argv[a+1]
		a += 2

		list_data.append(load_files(herf_filename, attr_filename, coms_filename))

	plot(list_data)


if __name__  == "__main__":
	main(sys.argv[1:])
