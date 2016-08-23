import sys

com_top_films_file = sys.argv[1]
films_genres_file = sys.argv[2]

coms = {}
films_genres = {}

with open(com_top_films_file, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		id_com = line.pop(0)
		if len(line) == 1:
			continue
		
		coms[id_com] = line

with open(films_genres_file, 'r') as file:
	for line in file:
		line = line.replace("\n", "").split()

		film = line.pop(0)

		films_genres[film] = sorted(line)


def herfindahl_multi():
	herf_index = {}

	for id_com in coms:
		genres_com = {}
		total = 0

		for film in coms[id_com]:
			if film not in films_genres:
				#print "Pas de genre pour " + film
				continue

			joint_genres = "_".join(films_genres[film])
			genres_com.setdefault(joint_genres, 0)
			genres_com[joint_genres] += 1
			total += 1

		herf_index[id_com] = 0.0

		for joint_genres in genres_com:
			herf_index[id_com] += pow(1.0 * genres_com[joint_genres] / total, 2)

	#print herf_index

	file = open("herf_multi.data", 'w')
	for id_com in herf_index:
		file.write(id_com + " " + str(herf_index[id_com]) + '\n')
	file.close()


def herfindahl_maj():
	herf_index = {}

	for id_com in coms:
		distrib_genre = {}
		total = 0

		for film in coms[id_com]:
			if film not in films_genres:
				#print "Pas de genre pour " + film
				continue

			for genre in films_genres[film]:
				distrib_genre.setdefault(genre, 0)
				distrib_genre[genre] += 1
				total += 1

		list_genre_max = {}

		for film in coms[id_com]:
			if film not in films_genres:
				continue

			gmax = 0
			genre_max = ""

			for genre in films_genres[film]:
				if distrib_genre[genre] > gmax:
					gmax = distrib_genre[genre]
					genre_max = genre

			list_genre_max[film] = genre_max

		genres_com = {}
		total = 0

		for film in list_genre_max:
			genres_com.setdefault(list_genre_max[film], 0)
			genres_com[list_genre_max[film]] += 1
			total += 1

		herf_index[id_com] = 0.0

		for genre in genres_com:
			herf_index[id_com] += pow(1.0 * genres_com[genre] / total, 2)
	
	file = open("herf_maj.data", 'w')
	for id_com in herf_index:
		file.write(id_com + " " + str(herf_index[id_com]) + '\n')
	file.close()

def herfindahl_all():
	herf_index = {}

	for id_com in coms:
		genres_com = {}
		total = 0

		for film in coms[id_com]:
			if film not in films_genres:
				#print "Pas de genre pour " + film
				continue

			for genre in films_genres[film]:
				genres_com.setdefault(genre, 0)
				genres_com[genre] += 1
				total += 1

		herf_index[id_com] = 0.0

		for genre in genres_com:
			herf_index[id_com] += pow(1.0 * genres_com[genre] / total, 2)

	#print herf_index

	file = open("herf_all.data", 'w')
	for id_com in herf_index:
		file.write(id_com + " " + str(herf_index[id_com]) + '\n')
	file.close()


herfindahl_all()
herfindahl_maj()
herfindahl_multi()