import csv
import difflib
import pandas as pd
from sklearn import preprocessing
from sklearn import tree
#import files

users = []
test_users = []
with open('../data/users/user_traj_form.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        users.append([int(x) for x in row])

#1001 companies
top_companies = []
with open('../data/users/fortune500.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        top_companies.append(row[2])

#819 schools
top_schools = []
with open('../data/users/best_schools.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        top_schools.append(row[1])

test_floor = 300
test_users = users[test_floor:]
users = users[:test_floor]
print(len(users), len(test_users))
# Main binning
#company_bins = [0, 50, 200, 500, len(top_companies), len(top_companies)+1, len(top_companies)+2]
#company_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']
#school_bins = [0, 50, 200, 500, len(top_schools), len(top_schools)+1, len(top_schools)+2]
#school_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']

# Alternate Binning
company_bins = [0, 50, 200, 500, len(top_companies), len(top_companies)+1, len(top_companies)+2]
company_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']
school_bins = [0, 50, 200, 500, len(top_schools), len(top_schools)+1, len(top_schools)+2]
school_bin_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'NONE']

def formatCompany(company):
    if company == 'N/A':
        return len(top_companies)+2
    best = difflib.get_close_matches(company, top_companies)
    if len(best) == 0:
        return len(top_companies)+1
    else:
        return top_companies.index(best[0])

def formatSchool(school):
    if school == 'N/A':
        return len(top_schools)+2
    best = difflib.get_close_matches(school, top_schools)
    if len(best) == 0:
        return len(top_schools)+1
    else:
        return top_schools.index(best[0])

def formatUser(user):
    return [formatSchool(user[0])] + [formatCompany(x) for x in user[1:]]

schools_lab = [x[0] for x in users]
companies1_lab= [x[1] for x in users]
companies2_lab= [x[2] for x in users]
companies3_lab= [x[3] for x in users]


#users = users[:10]
schools = [int(x[0]) for x in users]
companies1 = [int(x[1]) for x in users]
companies2 = [int(x[2]) for x in users]
companies3 = [int(x[3]) for x in users]

schools_bin = pd.cut(schools, school_bins, labels=school_bin_labels)
companies1_bin = pd.cut(companies1, company_bins, labels=company_bin_labels)
companies2_bin = pd.cut(companies2, company_bins, labels=company_bin_labels)
companies3_bin = pd.cut(companies3, company_bins, labels=company_bin_labels)

def binUser(user):
    return [pd.cut([user[0]], school_bins, labels=school_bin_labels)] + [pd.cut([x], company_bins, labels=company_bin_labels) for x in user[1:]]

#Preprocess data
school_pre = preprocessing.LabelEncoder()
school_pre.fit(school_bin_labels)
company_pre = preprocessing.LabelEncoder()
company_pre.fit(company_bin_labels)

schools_bin = school_pre.transform(schools_bin)
companies1_bin = company_pre.transform(companies1_bin)
companies2_bin = company_pre.transform(companies2_bin)
companies3_bin = company_pre.transform(companies3_bin)


#pre process single user
def ppUser(user):
     return [school_pre.transform(user[0])] + [company_pre.transform(x) for x in user[1:]]
    

def makeTestCase(user):
    #formatted_user = formatUser(user)
    formatted_user = user
    binned_user = binUser(formatted_user)
    pp_user = ppUser(binned_user)
    pp_user = [x[0] for x in pp_user]
    return [pp_user]

data = pd.DataFrame(data={'school': schools_bin,'company1': companies1_bin,'company2': companies3_bin,'company3': companies3_bin})

# create classifier
dtc = tree.DecisionTreeClassifier()
dtc = dtc.fit(data[['school','company1','company2']], data['company3'])

# Easy Predit Method
def predict(user):
    test = makeTestCase(user[:3])
    return dtc.predict(test)

# test a data set
# test = ['Binghamton University', 'Arity', 'Cisco']
# test_pre = makeTestCase(test)
# test_out = dtc.predict(test_pre)
# print(test_pre, test_out)
corrects = 0
for test in test_users:
    test_case = makeTestCase(test)
    test_result = predict(test)
    correct = test_case[0][3] == test_result[0]
    if correct:
        corrects += 1

print("Result: ", corrects*1.0/len(test_users))
