import matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def read_datafile(filename):
	labels = []
	lines = []
	
	with open(filename, 'r') as file:
		for line in file:
				line = line.replace('\n', '').split()

				if line[0] not in labels:
					labels.append(line[0])
				if line[1] not in labels:
					labels.append(line[1])
				lines.append(line)

	column_labels = []
	row_labels = []
	list_id_column = {}
	list_id_row = {}
	id_column = 0
	id_row = 0

	for l in labels:
		if "louvain" in l:
			column_labels.append(l)
			list_id_column[l] = id_column
			id_column += 1
		else:
			row_labels.append(l)
			list_id_row[l] = id_row
			id_row += 1

	data = [[] for x in xrange(id_row)]
	for i in range(0, id_row):
		for j in range(0, id_column):
			for line in lines:
					if (line[0] == row_labels[i] and line[1] == column_labels[j]) or (line[1] == row_labels[i] and line[0] == column_labels[j]):
					   data[i].append(float(line[2]))


	'''column_labels = row_labels = labels

	data = []
	for i in range(len(labels)):
		row = []
		for y in range(len(labels)):
			if i == y:
				row.append(1.0)
			else:
				for line in lines:
					if (line[0] == labels[i] and line[1] == labels[y]) or (line[1] == labels[i] and line[0] == labels[y]):
						row.append(float(line[2]))
						break

		data.append(row)'''

	return column_labels, row_labels, np.array(data)

def draw(column_labels, row_labels, data, filename):
	fig, ax = plt.subplots()
	heatmap = ax.pcolor(data, cmap=plt.cm.jet)

	# put the major ticks at the middle of each cell
	ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

	# want a more natural, table-like display
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	ax.set_xticklabels(row_labels, minor=False, fontsize=9, rotation=45)
	ax.set_yticklabels(column_labels, minor=False, fontsize=9)

	cb = plt.colorbar(heatmap)
	cb.set_label('NMI value')
	#cb.set_label('Jaccard mean value')
	cb.set_clim(0.0,1.0)
	
	fig.savefig(filename + "_heatmap.png", bbox_inches='tight')

def main(argv):
	filename = argv[0]
	column_labels, row_labels, data = read_datafile(filename)

	draw(column_labels, row_labels, data, filename)

if __name__  == "__main__":
	main(sys.argv[1:])