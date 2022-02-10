import os
import re
import json
from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
load_dotenv()
options = Options()
options.headless = True
service = Service(os.getenv("CHROME_DRIVER"))
print(os.getenv("CHROME_DRIVER")) 
options.add_argument("--log-level=3")    
driver = webdriver.Chrome(
    service=service, options=options) 

links = []
titles = [] 
blogs = []
def content_scraping(link):
    page = f"{link}"  
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html5lib')   
    for para in soup.find_all('div',class_='entry-content clearfix'): 
        text = para.get_text()
        break 
    text = text.rsplit(".")
    text.pop(-1) 
    blog = ''.join(str(e) for e in text)  
    return blog 


def home_page_scrapper():   
    page = f"https://inc42.com/buzz/"
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html5lib') 
    news_cards = soup.find_all('div',class_='card-content') 
    for cards in news_cards: 
        headline = cards.h2.text 
        headline = headline.strip('\n')
        link = cards.h2.a['href']  
        blog = content_scraping(link)   
        blog = blog.strip()
        links.append(link)
        titles.append(headline) 
        blogs.append(blog) 
    rows = pd.DataFrame({'Title':titles,'Link':links,'Blog':blogs}) 
    rows.to_csv("scrapper/inc42/blogs.csv", index=False)
def main(): 
    home_page_scrapper()


if __name__ == "__main__":
    main()



