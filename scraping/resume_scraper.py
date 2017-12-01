import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import csv

'''
functions for parsing resume
'''

# parse basic info section
def parse_basic_info(basic_div):
	if(basic_div != None):
		for val in basic_div:
			job_name = error_handle(val.find('h1', id='resume-contact'))
			location = error_handle(val.find('p', id='headline_location'))
		return [job_name, location]
	else:
		return ['']*2

# parse work experience section
def parse_work_experience(work_div):
	if(work_div != None):
		work_items = work_div.find_all('div', class_=re.compile('work-experience-section*'))
		work_items_length = len(work_items)
		work_list = []
		for i in range(3):
			if (i >= work_items_length):
				work_list.append(['']*3)
			else:
				section = work_items[i]
				title = error_handle(section.find('p', class_='work_title title'))
				company = error_handle(section.find('div', class_='work_company'))
				description = error_handle(section.find('p', class_='work_description'))
				work_list.append([title, company, description])
		return np.hstack(work_list)
	else:
		return ['']*3

# parse education section
def parse_education(education_div):
	if(education_div != None):
		education_items = education_div.find_all('div', class_='education-section')
		section_length = len(education_items)
		education_list = []

		for i in range(2):
			if(i >= section_length):
				education_list.append(['']*2)
			else:
				section = education_items[i]
				edu_title = error_handle(section.find('p', class_='edu_title'))
				school = error_handle(section.find('div', class_='edu_school'))
				education_list.append([edu_title, school])
		return np.hstack(education_list)
	else:
		return ['']*2

def error_handle(obj):
	return obj.text if obj != None else ''
'''
control flow of script
'''
try:
	df_urls = pd.read_pickle('resume_urls.pickle')
except FileNotFoundException:
	df_urls = pd.read_csv('resume_urls.csv')
	df_urls.to_pickle('resume_urls.pickle')


length = len(df_urls)
url_col = df_urls['url']
job_query_col = df_urls['job_query']

columns = ['job_query', 'job_name', 'location', 
			'school_name_1','school_1',
			'school_name_2', 'school_2',
			'job_title_1', 'company_1', 'description_1',
			'job_title_2', 'company_2', 'description_2',
			'job_title_3', 'company_3', 'description_3']

parsed_resume_data = []
parsed_resume_data.append(columns)

for i in range(length):
	url = str(url_col[i])

	req = requests.get(url)
	data = req.text
	soup = BeautifulSoup(data, 'lxml')

	basic_info_div = soup.find('div', class_='last basicInfo-content')
	work_experience_div = soup.find('div', class_='section-item workExperience-content')
	education_div = soup.find('div', class_='section-item education-content')

	basic_info_list = parse_basic_info(basic_info_div)
	#print(basic_info_list)
	education_list = parse_education(education_div)
	# print(education_list)
	work_experience_list = parse_work_experience(work_experience_div)
	#print(work_experience_list)
	row = [job_query[i]] + list(basic_info_list) + list(education_list) + list(work_experience_list)
	parsed_resume_data.append(row)
	print('finished row: ' + str(i))

parsed_resume_file = open('parsed_resumes1.csv', 'a')
with parsed_resume_file:
	writer = csv.writer(parsed_resume_file)
	writer.writerows(parsed_resume_data)





