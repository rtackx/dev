import sys, os

def build_network_typeA(dir_dest, base_filename1, base_filename2, base_filename_coupling):
	if not os.path.exists(dir_dest + "/networks"):
		os.mkdir(dir_dest + "/networks")

	indexed_filename1 = dir_dest + "/indexed/" + base_filename1 + ".indexed"
	indexed_filename2 = dir_dest + "/indexed/" + base_filename2 + ".indexed"
	indexed_filename_coupling = dir_dest + "/indexed/" + base_filename_coupling + ".indexed"

	cmd = "cat " + indexed_filename1 + "| awk '{print $1,$2}' > " + dir_dest + "/networks/multilayer"
	os.popen(cmd)
	cmd = "cat " + indexed_filename2 + "| awk '{print $1,$2}' >> " + dir_dest + "/networks/multilayer"
	os.popen(cmd)
	cmd = "cat " + indexed_filename_coupling + "| awk '{print $1,$2}' >> " + dir_dest + "/networks/multilayer"
	os.popen(cmd)

	'''cmd = "cat " + indexed_filename1 + " > " + dir_dest_networks_typeA + "/networks/multilayer.weights"
	os.popen(cmd)
	cmd = "cat " + indexed_filename2 + " >> " + dir_dest_networks_typeA + "/networks/multilayer.weights"
	os.popen(cmd)
	cmd = "cat " + indexed_filename_coupling + " >> " + dir_dest_networks_typeA + "/networks/multilayer.weights"
	os.popen(cmd)'''

def renumbered(dir_dest, filename_layer1, sep_filename1, filename_layer2, sep_filename2, filename_coupling, sep_filename_coupling):
	if not os.path.exists(dir_dest + "/index1"):
		os.mkdir(dir_dest + "/index1")
	if not os.path.exists(dir_dest + "/indexed"):
		os.mkdir(dir_dest + "/indexed")

	base_filename1 = filename_layer1.split('/')[-1]
	base_filename2 = filename_layer2.split('/')[-1]
	base_filename_coupling = filename_coupling.split('/')[-1]

	print "--> Renumbered layer 1 : " + filename_layer1
	cmd_renumbered = "python " + base_scripts + "index_id.py " + filename_layer1 + " 0 " + sep_filename1
	index1_max = os.popen(cmd_renumbered).read()[:-1]
	os.rename(filename_layer1 + ".index1", dir_dest + "/index1/" + base_filename1 + ".index1")
	os.rename(filename_layer1 + ".indexed", dir_dest + "/indexed/" + base_filename1 + ".indexed")
	index1_filename1 = dir_dest + "/index1/" + base_filename1 + ".index1"

	print "--> Renumbered layer 2 : " + filename_layer2
	cmd_renumbered = "python " + base_scripts + "index_id.py " + filename_layer2 + " " + index1_max + " " + sep_filename2
	index2_max = os.popen(cmd_renumbered).read()[:-1]
	os.rename(filename_layer2 + ".index1", dir_dest + "/index1/" + base_filename2 + ".index1")
	os.rename(filename_layer2 + ".indexed", dir_dest + "/indexed/" + base_filename2 + ".indexed")
	index1_filename2 = dir_dest + "/index1/" + base_filename2 + ".index1"

	print "--> Renumbered coupling : " + filename_coupling
	cmd_renumbered = "python " + base_scripts + "index_id_coupling.py " + filename_coupling + " " + index1_filename1 + " " + index1_filename2 + " " + sep_filename_coupling
	os.popen(cmd_renumbered)
	os.rename(filename_coupling + ".indexed", dir_dest + "/indexed/" + base_filename_coupling + ".indexed")

	print "Range of index nodes : [0 ; " + index2_max + "["
	print "Range layer 1 : [0 ; " + index1_max + "["
	print "Range layer 2 : [" + index1_max + " ; " +  index2_max + "["

### Global vars
sep_filename1 = " "
sep_filename2 = ","
sep_filename_coupling = ","
base_scripts = "/home/n3/Desktop/multilayers/scripts/"

if __name__  == "__main__":
	filename_layer1 = sys.argv[1]
	filename_layer2 = sys.argv[2]
	filename_coupling = sys.argv[3]

	base_filename1 = filename_layer1.split('/')[-1]
	base_filename2 = filename_layer2.split('/')[-1]
	base_filename_coupling = filename_coupling.split('/')[-1]

	dir_dest = sys.argv[4]

	'''dir_dest = dir_dest + "/typeA"
	if not os.path.exists(dir_dest):
		os.mkdir(dir_dest)'''
	print "-> Base directory : " + dir_dest

	##### 1) Renumbered
	print "-> Renumbered orginal layers"
	renumbered(dir_dest, filename_layer1, sep_filename1, filename_layer2, sep_filename2, filename_coupling, sep_filename_coupling)
	
	### 2) Build typeA network
	print "-> Build network"
	build_network_typeA(dir_dest, base_filename1, base_filename2, base_filename_coupling)

	### 3) Get giant component network
	print "-> Get giant component of layers"
	dir_dest_giant = dir_dest + "/giant_component"
	if not os.path.exists(dir_dest_giant):
		os.mkdir(dir_dest_giant)

	filename_giant_layer1 = dir_dest_giant + "/" + base_filename1 + "_giant"
	filename_giant_layer2 = dir_dest_giant + "/" + base_filename2 + "_giant"

	cmd_giant = "python " + base_scripts + "/connected_components.py " + filename_layer1 + " " + sep_filename1 + " > " + dir_dest_giant + "/giant_" + base_filename1 + ".run"
	print "--> Layers 1..."
	os.popen(cmd_giant)
	os.rename(filename_layer1 + "_giant", filename_giant_layer1)
	
	cmd_giant = "python " + base_scripts + "/connected_components.py " + filename_layer2 + " " + sep_filename2 + " > " + dir_dest_giant + "/giant_" + base_filename2 + ".run"
	print "--> Layers 2..."
	os.popen(cmd_giant)
	os.rename(filename_layer2 + "_giant", filename_giant_layer2)

	### 4) Renumbered giant component
	print "-> Renumbered layers of giant component network"
	renumbered(dir_dest_giant, filename_giant_layer1, " ", filename_giant_layer2, " ", filename_coupling, sep_filename_coupling)

	### 5) Build typeA giant component network
	print "-> Build giant component network"
	build_network_typeA(dir_dest_giant, base_filename1 + "_giant", base_filename2 + "_giant", base_filename_coupling)