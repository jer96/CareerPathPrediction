from indeed_res_url_scraper import add_resume_urls, init_csv

popular_jobs = ['software engineer' ,'sales associate', 'account manager', 'corporate recruiter', 'teacher',
				'electrical engineer',  'financial analyst', 'ux designer', 'registered nurse', 'occupational therapist']

init_csv()

for job in popular_jobs:
	i = 0
	while(i != 500):
		print('job: ' + job + ' iteration: ' + str(i))
		if (i == 0 ):
			add_resume_urls(job)
		else:
			add_resume_urls(job, start=i)
		i += 50
	print()