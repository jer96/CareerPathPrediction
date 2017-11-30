from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ConfigParser
import time
import itertools
import csv
import re


links = []
with open('links.txt', 'rb') as f:
	links = [line.rstrip('\n') for line in f]

config = ConfigParser.ConfigParser()
config.read("../../../config.ini")

users = open('users.txt','a')
cwriter = csv.writer(users, delimiter=',', quotechar='|')

username = config.get("vars", "user") 
password = config.get("vars", "passw")

driver = webdriver.Firefox()
driver.get("https://www.linkedin.com/uas/login")
username_field = driver.find_element_by_name("session_key")
password_field = driver.find_element_by_name("session_password")
username_field.send_keys(username)
password_field.send_keys(password)
driver.find_element_by_name("signin").click()




for link in links:
	time.sleep(1)
	driver.get(link)
	time.sleep(0.5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	companies = driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")
	schools = driver.find_elements_by_xpath("//a[@data-control-name='background_details_school']")
	 
	user = []
	if len(schools) > 0:	
		data = schools[0].text.split('\n')
		data = [x.encode('utf-8') for x in data]
		data = [re.sub(r'[^\x00-\x7f]',r'', x) for x in data]
		school = dict(itertools.izip_longest(*[iter(data[1:])] * 2, fillvalue=""))
		school['School'] = data[0]
		school_rev = {}
		school_rev['grade'] = school.get('Grade', 0)
		school_rev['dates'] = school.get('Dates attended or expected graduation', '')
		school_rev['degree'] = school.get('Degree Name', '')
		school_rev['field'] = school.get('Field of Study', '')
		school_rev['school'] = school.get('School', '')
		user.append(school_rev['grade'])
		user.append(school_rev['dates'])
		user.append(school_rev['degree'])
		user.append(school_rev['field'])
		user.append(school_rev['school'])
	
	count = 1
	for thing in reversed(companies[0:3]):
		data = thing.text.split('\n')
		data = [x.encode('utf-8') for x in data]
		data = [re.sub(r'[^\x00-\x7f]',r'', x) for x in data]
		company = {'title': '', 'company': '', 'employment_dates': '', 'employment_duration': ''}
		if len(data) > 0:
			company['title'] = data[0]
			company['company'] = data[2]
			if len(data) > 4:
				company['employment_dates'] = data[4]
				company['employment_duration'] = data[6]
		
		user.append(company['title'])
		user.append(company['company'])
		user.append(company['employment_dates'])
		user.append(company['employment_duration'])
	
	print(user)
	cwriter.writerow(user)
	users.flush()

	
	

driver.close()
