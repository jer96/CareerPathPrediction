import csv

users = []
new_users = []
with open('../../../scraping/soft_eng_resumes.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        users.append(row)

    for i, x in enumerate(users[3]):
        print(i, x)

    with open('ser_min.csv', 'w+') as csvout:
        csvwriter = csv.writer(csvout, delimiter=',', quotechar='"')
        for row in users:
            new_row = ['N/A', 'N/A', 'N/A', 'N/A']
            row = [x.split(' - ')[0] for x in row]
            if(len(row) > 4):
                if(row[4] != ''):
                    new_row[0] = row[4]
                if(len(row) > 8):
                    if(row[8] != ''):
                        new_row[1] = row[8]
                    if(len(row) > 11):
                        if(row[11] != ''):
                            new_row[2] = row[11]
                        if(len(row) > 14):
                            if(row[14] != ''):
                                new_row[3] = row[14]
            if(new_row not in new_users):
                new_users.append(new_row)
                csvwriter.writerow(new_row)
        csvout.flush()
