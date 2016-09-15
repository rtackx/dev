import sys, os

dir_dest = sys.argv[1]
list_subs = ["GPS", "CM", "Shuffle_coms", "Louvain", "Infomap"]
list_att = ["genres", "languages", "years", "countries"]
files_att = ["IMDB_movies-actors_1980-2010.bipartite.genres", "IMDB_movies-actors_1980-2010.bipartite.languages", "IMDB_movies-actors_1980-2010.bipartite.years", "IMDB_movies-actors_1980-2010.bipartite.countries"]
system_lib = ""

for i in range(0, len(list_subs)):
	if i < 3:
		name_coms = dir_dest + "/" + list_subs[i] + "/GPS_communities_top"
	elif i == 3:
		name_coms = dir_dest + "/" + list_subs[i] + "/IMDB_movies-actors_1980-2010.bipartite_num.adjacency.tree_lvl1"
	elif i == 4:
		name_coms = dir_dest + "/" + list_subs[i] + "/IMDB_movies-actors_1980-2010.bipartite_num.clu.coms"

	print "> " + list_subs[i]

	for j in range(0, len(list_att)):
		path_att = dir_dest + "/" + list_subs[i] + "/" + list_att[j]
		os.system("mkdir " + path_att + " 2>> /dev/null")
		print "\t>> " + list_att[j]

		os.system("python /data2/tackx/py_scripts/IMDB/herfindahl.py " + name_coms + " " + files_att[j] + " && mv *.data " + path_att)
		os.system("python /data2/tackx/py_scripts/draw_distribution.py -f " + path_att + "/herf_all.data")
		os.system("python /data2/tackx/py_scripts/draw_distribution.py -f " + path_att + "/herf_multi.data")
		os.system("python /data2/tackx/py_scripts/draw_distribution.py -f " + path_att + "/herf_maj.data")

		'''print "\t\t[Drawing common teta...]"
		os.system("python /data2/tackx/py_scripts/IMDB/common_teta.py " + name_coms + " " + files_att[j])
		os.system("mv " + files_att[j] + "_common_teta* " + dir_dest + "/" + list_subs[i])

		print "\t\t[Drawing attributes herf_all...]"
		os.system("python /data2/tackx/py_scripts/IMDB/plot_herf_attribute.py " + path_att + "/herf_all.data " + files_att[j] + " " + name_coms)
		os.system("mv " + files_att[j] + "_scatter.png " + path_att + "/herf_" + list_att[j] + "_all_plot.png")
		print "\t\t[Drawing attributes herf_multi...]"
		os.system("python /data2/tackx/py_scripts/IMDB/plot_herf_attribute.py " + path_att + "/herf_multi.data " + files_att[j] + " " + name_coms)
		os.system("mv " + files_att[j] + "_scatter.png " + path_att + "/herf_" + list_att[j] + "_multi_plot.png")
		print "\t\t[Drawing attributes herf_maj...]"
		os.system("python /data2/tackx/py_scripts/IMDB/plot_herf_attribute.py " + path_att + "/herf_maj.data " + files_att[j] + " " + name_coms)
		os.system("mv " + files_att[j] + "_scatter.png " + path_att + "/herf_" + list_att[j] + "_maj_plot.png")'''