from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ConfigParser
import time


links = []
with open('links.txt', 'rb') as f:
	links = [line.rstrip('\n') for line in f]

print(links)
config = ConfigParser.ConfigParser()
config.read("../../../config.ini")
file = open('links.txt','a')
username = config.get("vars", "user")
password = config.get("vars", "passw")

driver = webdriver.Firefox()
driver.get("https://www.linkedin.com/uas/login")
username_field = driver.find_element_by_name("session_key")
password_field = driver.find_element_by_name("session_password")
username_field.send_keys(username)
password_field.send_keys(password)
driver.find_element_by_name("signin").click()

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ember973")))
driver.get('https://www.linkedin.com/search/results/people/?keywords=Software%20Engineer&origin=SUGGESTION')
while True:
	time.sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	for e in driver.find_elements_by_class_name('search-result__wrapper'):
		data = e.find_element_by_class_name('search-result__info').find_element_by_tag_name('a')
		link = data.get_attribute("href")
		if link not in links:
			file.write('\n' + link)
			print(link)
			file.flush()
	driver.find_element_by_class_name('next').click()
	

driver.close()
