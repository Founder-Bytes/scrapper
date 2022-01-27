import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = True
driver = webdriver.Chrome("C:/chrome_driver/chromedriver", options=options) 
links = [] 
names = []
for i in range(18587):
    driver.get(f"https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page={i}")
    content = driver.page_source
    soup = BeautifulSoup(content)    
    startup_cards = soup.find_all('div', class_= 'category-card search-card new-eco-card')
    for cards in startup_cards:  
        name = cards.h3.text
        names.append(name)
        link = cards.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'] 
        link = "https://www.startupindia.gov.in" + link
        links.append(link)

rows = pd.DataFrame({'Name of Startup':names,'Link':links}) 
rows.to_csv("links.csv")

