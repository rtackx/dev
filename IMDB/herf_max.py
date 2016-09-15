import matplotlib
matplotlib.use("Agg")
import os, ast, operator, sys, pylab, numpy

display_number = 26

def load_files(label, filename_herf, filename_attr, filename_coms):

	coms = {}
	with open(filename_coms, 'r') as file:
			for line in file:
				line = line.replace("\n", "").split()
				
				com_id = line.pop(0)
				if len(line) == 1:
					continue
				coms[com_id] = line

	herfs = {}
	with open(filename_herf, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			com_id = line[0]
			herfs[com_id] = float(line[1])

	attrs = {}
	attrs_numbered = {}
	rank_attr = {}
	number = 1
	with open(filename_attr, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			film_name = line.pop(0)
			
			attrs[film_name] = line
			for attr in line:
				if attr not in attrs_numbered:
					attrs_numbered[attr] = number
					rank_attr[attr] = 1
					number += 1
				else:
					rank_attr[attr] += 1


	max_attr_coms = {}
	coms_max_attr = {}
	for id_com in coms:
		attrs_com = {}
		
		for film_name in coms[id_com]:
			if film_name in attrs:
				for attr in attrs[film_name]:
					attrs_com.setdefault(attr, 0)
					attrs_com[attr] += 1

		max_attr = []
		m = 0
		for attr in attrs_com:
			if attrs_com[attr] >= m:
				if attrs_com[attr] == m:
					max_attr.append(attr)
				else:
					max_attr = []
					max_attr.append(attr)

				m = attrs_com[attr]
		
		for attr in max_attr:
			max_attr_coms.setdefault(attr, [])
			max_attr_coms[attr].append(id_com)
			coms_max_attr.setdefault(id_com, [])
			coms_max_attr[id_com].append(attr)


	'''herf_max_attr = {}
	for attr in max_attr_coms:
		herf_max_attr[attr] = []

		for id_com in max_attr_coms[attr]:
			herf_max_attr[attr].append(herfs[id_com])

	herf_max_attr_mean = {}
	for attr in herf_max_attr:
		herf_max_attr_mean[attr] = numpy.mean(herf_max_attr[attr])
		#print attr + ' ' + str(herf_max_attr_mean[attr])

	sorted_rank_attr = sorted(rank_attr.items(), key=operator.itemgetter(1), reverse=True)[:display_number]

	data = []
	list_attr_names = []

	i = 1
	for k,v in sorted_rank_attr:
		if k in herf_max_attr_mean:
			data.append((i, herf_max_attr_mean[k]))
		else:
			data.append((i, 0.0))

		list_attr_names.append(k)
		i += 1'''

	movie_attr_inside_com = {}
	count_attr = {}
	set_attrs = set()
	movies_attr = {}
	for id_com in coms_max_attr:
		for film_name in coms[id_com]:
			movie_attr_inside_com.setdefault(film_name, {})

			if film_name in attrs:
				for attr in attrs[film_name]:
					set_attrs.add(attr)
					movies_attr.setdefault(film_name, 0)

					if attr in coms_max_attr[id_com]:
						movie_attr_inside_com[film_name][attr] = 1
						movies_attr[film_name] = 1
					else:
						movie_attr_inside_com[film_name][attr] = 0
					count_attr.setdefault(attr, 0)
					count_attr[attr] += 1
	
	attr_movies = {}
	for attr in set_attrs:
		attr_movies[attr] = 0
		for film_name in movie_attr_inside_com:
			if attr in movie_attr_inside_com[film_name]:
				attr_movies[attr] += movie_attr_inside_com[film_name][attr]

	attr_movies_mean = {}
	for attr in attr_movies:
		attr_movies_mean[attr] = 1.0 * attr_movies[attr] / count_attr[attr]

	f = open(label + '_max_attr_coms', 'w')
	for id_com in coms:
		count = 0
		over = 0
		for film_name in coms[id_com]:
			if film_name in attrs:
				count += movies_attr[film_name]
				over += 1

		'''if over == 0:
			print id_com + ' ' + str(0.0)'''

		if over:
			f.write(id_com + ' ' + str(1.0 * count / over) + '\n')
	f.close()

	f = open(label + '_movies_good_atrr', 'w')
	for film_name in movies_attr:
		f.write(film_name + ' ' + str(movies_attr[film_name]) + '\n')
	f.close()


	sorted_rank_attr = sorted(rank_attr.items(), key=operator.itemgetter(1), reverse=True)[:display_number]
	
	data = []
	list_attr_names = []

	i = 1
	for k,v in sorted_rank_attr:
		if k in attr_movies_mean:
			data.append((i, attr_movies_mean[k]))
		else:
			data.append((i, 0.0))

		list_attr_names.append(k)
		i += 1

	
	return data, list_attr_names


def plot(list_data):
	colors = ["red", "green", "blue", "cyan"]
	markers = ["s", "v", "o"]

	fig, ax = pylab.subplots(figsize=(13,10), dpi=80)
	#pylab.xscale("log")
	#pylab.ylabel("Herfindahl index")
	pylab.ylabel("Goodness score", fontsize=16)
	pylab.ylim([0.0, 1.0])
	pylab.xlim([0.0, display_number+1])	
	pylab.grid(True)

	for i in range(0, len(list_data)):
		data = list_data[i][0]
		
		plot_parameters = dict(linestyle="", marker=markers[i], markersize=13, linewidth=2.5, color=colors[i])

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
	ax.tick_params(labelbottom='off', labeltop='on', labelsize=11)
	pylab.xticks(rotation=45)
	ax.legend(loc=1)

	fig.savefig("herf_max_scatter.png")
	pylab.close(fig)

labels = ["Louvain", "Infomap", "GPS"]

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

		list_data.append(load_files(labels[i], herf_filename, attr_filename, coms_filename))

	plot(list_data)


if __name__  == "__main__":
	main(sys.argv[1:])