import re
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = True
driver = webdriver.Chrome(
    "chromedriver/chromedriver", options=options)
links = []
names = []
count = 0
mapping = {}
print("Scrapping Starting...")
while count < 18587:
    try:
        page = f"https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page={count}"
        print(page)
        driver.get(page)
        content = driver.page_source
        soup = BeautifulSoup(content, features='html5lib')
        startup_cards = soup.find_all(
            'div', class_='category-card search-card new-eco-card')
        for cards in startup_cards:
            name = cards.h3.text
            names.append(name)
            link = cards.find('a', href=re.compile(
                r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            link = "https://www.startupindia.gov.in" + link
            links.append(link)
            if name not in mapping.keys():
                mapping[name] = link
        count += 1
    except:
        pass

with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=4)

rows = pd.DataFrame({'Name of Startup': names, 'Link': links})
rows.to_csv("test_links.csv")
