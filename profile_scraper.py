import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json

options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Chrome("C:/chrome_driver/chromedriver", options=options)

df = pd.read_csv("startup_india/all_links_combined.csv")
details_dict = {}
list_details = []

for index, row in df.iterrows():
    profile_link = row["Link"]
    driver.get(profile_link)
    content = driver.page_source
    soup = BeautifulSoup(content)
    details_dict = {}
    basic_details = soup.find("div", class_="company-name")
    details_dict["Name"] = basic_details.p.text
    portal_active_date = basic_details.find("span", class_="orglevel active-since")
    portal_active_date = portal_active_date.strong.text
    details_dict["Portal Active Date"] = portal_active_date
    website = basic_details.find("a", class_="website")
    if website:
        details_dict["Website"] = website.text
    description = soup.find("div", class_="read margin-t20")
    description = description.text
    cards = soup.find_all("div", class_="bottom-content clearfix startup-grid")
    for card in cards:
        stage = card.find("span", class_="title")
        content = card.find("span", class_="content")
        details_dict[stage.text] = content.text
    cards = soup.find_all("span", class_="content-section focusSection")
    for card in cards:
        title = card.find("span", class_="title")
        content = card.find("span", class_="content")
        details_dict[title.text] = content.text
    desc = soup.find("div", class_="read margin-t20")
    desc = desc.find("p")
    details_dict["description"] = desc.getText()
    list_details.append(details_dict)
    with open("result.json", "w") as fp:
        json.dump(list_details, fp)
    print(list_details)
