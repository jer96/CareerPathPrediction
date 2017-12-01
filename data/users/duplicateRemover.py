import csv

with open('users.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	users = []
	for row in csvreader:
		if row not in users:
			users.append(row)
	
	print(len(users))
	with open('users_no_dupe.csv', 'w+') as csvout:
		csvwriter = csv.writer(csvout, delimiter=',', quotechar='|')
		for row in users:
			csvwriter.writerow(row)
		csvout.flush()
