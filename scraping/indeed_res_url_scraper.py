from bs4 import BeautifulSoup
import requests
import re
import csv

base_url = 'https://www.indeed.com/'
base_res_url = base_url + 'resumes'

def init_csv():
	resume_urls = open('resume_urls.csv', 'a') 
	with resume_urls:  
	   writer = csv.writer(resume_urls)
	   writer.writerows([['url', 'job_query']])

def add_resume_urls(job_query, start=None):
	if (start):
		query_url = base_res_url + '?q=%s&l=united+states&cb=jt' + '&start=' + str(start)	
	else:
		query_url = base_res_url + '?q=%s&l=united+states&cb=jt'
	
	query_url = query_url % job_query

	req = requests.get(query_url)

	data = req.text

	soup = BeautifulSoup(data, 'lxml')
	url_list = []
	ol = soup.find('ol', id='results')
	for li in ol.find_all('li',class_='sre'):
		job_id_query = 'r/' + li['id']
		job_id_query = base_url + job_id_query
		job_id_query_list = [job_id_query, job_query]
		url_list.append(job_id_query_list)

	resume_urls = open('resume_urls.csv', 'a') 
	with resume_urls:  
	   writer = csv.writer(resume_urls)
	   writer.writerows(url_list)


