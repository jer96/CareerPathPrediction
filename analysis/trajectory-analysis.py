import csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

users = []
with open('../data/users/user_traj_data.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in csvreader:
            users.append(row)
            
schools = [x[0] for x in users]
c1 = [x[1] for x in users]
c2 = [x[2] for x in users]
c3 = [x[3] for x in users]

companies = c1+c2+c3
companies = list(set(companies))
 
school_pre = preprocessing.LabelEncoder()
school_pre.fit(list(set(schools)))
company_pre = preprocessing.LabelEncoder()
company_pre.fit(companies)

d = {'school': schools,'company1': c1,'company2': c2,'company3': c3}
data = pd.DataFrame(data=d)

data['school'] = school_pre.transform(data['school'])
data['company1'] = company_pre.transform(data['company1'])
data['company2'] = company_pre.transform(data['company2'])
data['company3'] = company_pre.transform(data['company3'])

tree = DecisionTreeClassifier()
tree = tree.fit(data[['school','company1','company2']], data['company3'])

def test_transform(test_data):
        return [school_pre.transform([test_data[0]])[0], 
                company_pre.transform([test_data[1]])[0], 
                company_pre.transform([test_data[2]])[0]]


def test_inverse_transform(test_data):
        return [school_pre.inverse_transform([test_data[0]]), 
                company_pre.inverse_transform([test_data[1]]), 
                company_pre.inverse_transform([test_data[2]])]

test = ['Binghamton University', 'Arity', 'Cisco']
test_pre = test_transform(test)
test_out = tree.predict([test_pre])
