import sys

def search_user_common_item(user_id, users, coms):
	if len(users[user_id]) == 0:
		return 0

	id_com_user = -1
	for com_id in coms:
		if user_id in coms[com_id]:
			id_com_user = com_id
			break

	if id_com_user == -1:
		return 0

	nb_common_item = 0
	for id_item in users[user_id]:
		if id_item in coms[id_com_user]:
			nb_common_item += 1

	return nb_common_item

filename_user_items = sys.argv[1]
filename_community = sys.argv[2]

users = {}
with open(filename_user_items, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			user_id = line.pop(0)

			users[user_id] = line

coms = {}
with open(filename_community, 'r') as file:
		for line in file:
			line = line.replace("\n", "").split()

			com_id = line.pop(0)

			coms[com_id] = line

prop_common_item = {}
for user_id in users:
	nb_common_item = search_user_common_item(user_id, users, coms)
	if nb_common_item == 0:
		prop_common_item[user_id] = -1.0
	else:
		prop_common_item[user_id] = 1.0 * nb_common_item / len(users[user_id])

f = open("prop_items", 'w')
for user_id in prop_common_item:
	f.write(user_id + " " + str(prop_common_item[user_id]) + "\n")
f.close()