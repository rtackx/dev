import sys, numpy

list_files = sys.argv[1:]

values = {}
for filename in list_files:

	with open(filename, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			id = line[0]
			value = float(line[1])

			values.setdefault(id, [])
			values[id].append(value)

average_values = {}
for id in values:
	average_values[id] = numpy.mean(values[id])
	print id + ' ' + str(average_values[id])

'''f = open("avg_values", 't')
for id in average_values:
	f.write(id + ' ' + str(average_values[id]))
f.close()'''