import sys, numpy

def get_herf_by_movie(filename_herf, filename_attr, filename_coms):
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
	with open(filename_attr, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			film_name = line.pop(0)
			
			attrs[film_name] = line

	herf_movies = {}
	for id_com in coms:
		for film_name in coms[id_com]:
			herf_movies[film_name] = herfs[id_com]


	return herf_movies

def main(argv):
	number_of_elements = int(argv[0])
	coms_filename = argv[1]
	list_herf_movies = []

	a = 2
	for i in range(0, number_of_elements):
		attr_filename = argv[a]
		herf_filename = argv[a+1]		
		a += 2

		list_herf_movies.append(get_herf_by_movie(herf_filename, attr_filename, coms_filename))

	herf_movies_all = {}		
	for herf_movies in list_herf_movies:
		for film_name in herf_movies:
			herf_movies_all.setdefault(film_name, [])
			herf_movies_all[film_name].append(herf_movies[film_name])

	herf_movies_all_mean = {}
	for film_name in herf_movies_all:
		herf_movies_all_mean[film_name] = numpy.mean(herf_movies_all[film_name])
		print film_name + ' ' + str(herf_movies_all_mean[film_name])


if __name__  == "__main__":
	main(sys.argv[1:])

