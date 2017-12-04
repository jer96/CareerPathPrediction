import csv

with open('users.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	users = []
	for row in csvreader:
            users.append(row)
	
	print(len(users))
	with open('user_traj_data.csv', 'w+') as csvout:
            csvwriter = csv.writer(csvout, delimiter=',', quotechar='|')
            for row in users:
                new_row = ['N/A', 'N/A', 'N/A', 'N/A']
                if(len(row) > 4):
                    new_row[0] = row[4]
                    if(len(row) > 6):
                        new_row[1] = row[6]
                        if(len(row) > 10):
                            new_row[2] = row[10]
                            if(len(row) > 14):
                                new_row[3] = row[14]
                    csvwriter.writerow(new_row)
            csvout.flush()
