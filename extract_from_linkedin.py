import os
from dotenv import load_dotenv
from pathlib import Path
from decryption import decrypt
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=chrome_options)
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
dotenv_path = Path('/home/abdul/private/.env')
load_dotenv(dotenv_path=dotenv_path)

email = os.getenv('pata')
password = os.getenv('tala')
encoding_type = os.getenv('encoding_type')
key = os.getenv('chabi')
encoder = os.getenv('encoder')

email, password = decrypt(email,password, encoding_type, key, encoder)
#print(email,password)

actions.login(driver, str(email), str(password)) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/abdulrehman6498/",experiences=[], driver=driver)
#Person(linkedin_url=None, name=None, about=[], experiences=[], educations=[], interests=[], accomplishments=[], company=None, job_title=None, driver=None, scrape=True)
print("Person: " + person.name)
print("Person projects: ")
print(person.experiences)
# for contact in person.contacts:
# 	print("Contact: " + contact.name + " - " + contact.occupation + " -> " + contact.url)