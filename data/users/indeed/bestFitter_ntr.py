import csv
import difflib
import pandas as pd
#import files

users = []
with open('ntr_min.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        users.append(row)

#1001 companies
top_companies = []
with open('../fortune500.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        top_companies.append(row[2])

#819 schools
top_schools = []
with open('../best_schools.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        top_schools.append(row[1])



# company_bins = [0, 50, 200, 500, len(top_companies), len(top_companies)+1, len(top_companies)+2]
# company_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']
# school_bins = [0, 50, 200, 500, len(top_schools), len(top_schools)+1, len(top_schools)+2]
# school_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']


#functions
def formatCompany(company):
    if company == 'N/A':
        return len(top_companies)+2
    best = difflib.get_close_matches(company, top_companies)
    if len(best) == 0:
        return len(top_companies)+1
    else:
        return top_companies.index(best[0])

#    else if top_companies.index(best[0]))
def formatSchool(school):
    if school == 'N/A':
        return len(top_schools)+2
    best = difflib.get_close_matches(school, top_schools)
    if len(best) == 0:
        return len(top_schools)+1
    else:
        return top_schools.index(best[0])

def formatUser(user):
    return [formatSchool(user[0])] + [formatCompany(x) for x in user[1:4]]

#test
#users = users[:10]
schools_lab = [x[0] for x in users]
companies1_lab= [x[1] for x in users]
companies2_lab= [x[2] for x in users]
companies3_lab= [x[3] for x in users]


formatted_users = [formatUser(x) for x in users]
schools = [x[0] for x in formatted_users]
companies1 = [x[1] for x in formatted_users]
companies2 = [x[2] for x in formatted_users]
companies3 = [x[3] for x in formatted_users]


with open('ntr_form.csv', 'w+') as csvout:
    csvwriter = csv.writer(csvout, delimiter=',', quotechar='"')
    for row in formatted_users:
        csvwriter.writerow(row)
    csvout.flush()
