import os
import re
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

load_dotenv()
options = Options()
options.headless = True
options.add_argument("--log-level=3")
service = Service(os.getenv("CHROME_DRIVER"))
print(os.getenv("CHROME_DRIVER"))
driver = webdriver.Chrome(service=service, options=options)


def startup_india_scraping():
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
            soup = BeautifulSoup(content, features="html5lib")
            startup_cards = soup.find_all(
                "div", class_="category-card search-card new-eco-card"
            )
            for cards in startup_cards:
                name = cards.h3.text
                names.append(name)
                link = cards.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs[
                    "href"
                ]
                link = "https://www.startupindia.gov.in" + link
                links.append(link)
                if name not in mapping.keys():
                    mapping[name] = link
            count += 1
        except:
            pass

    with open("data/startup_india/links.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)

    rows = pd.DataFrame({"Name": names, "Link": links})
    rows.to_csv("data/startup_india/test_links.csv", index=False)


def startup1000():
    city = []
    links = []
    name = []
    page = f"https://10000startups.com/our-startups"
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html5lib")
    startup_cards = soup.find("div", class_="container startup-d")
    list_of_cities = startup_cards.find_all("ul")
    for cities in list_of_cities:
        list_of_startups = cities.find_all("li")
        for startups in list_of_startups:
            city.append(cities.span.text)
            name.append(startups.h3.text)
            links.append(startups.a["href"])
    rows = pd.DataFrame({"Name": name, "Link": links, "City": city})
    rows.to_csv("data/10000_startups/info.csv", index=False)


def industry_filter_scrape():
    industry = []
    values = []
    page = f"https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page=0"
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html5lib")
    div_sector = soup.find("div", class_="mCSB_container")
    list_of_cards = div_sector.find_all("li")
    for cards in list_of_cards:
        input = cards.find("input")
        value = input.get("value")
        industry.append(cards.find("span").text)
        values.append(value)
    rows = pd.DataFrame({"industry_name": industry, "value": values})
    rows.to_csv("startup_india/industry_links.csv", index=False)


def sector_filter_scrape():
    print("sector scraping")
    df = pd.read_csv("startup_india/industry_links.csv")
    for index, row in df.iterrows():
        industry_value = row["value"]
        page = f"https://www.startupindia.gov.in/content/sih/en/search.html?industries={industry_value}&roles=Startup&page=0"
        print(page)
        driver.get(page)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html5lib")
        div_sector = soup.find("div", class_="filter-new")
        print(div_sector)
        # print(soup)
        # div_sector = soup.find('div', _class='accordion-section acc-2')
        val = soup.find("div", id_="mCSB_2_container")
        print(val)


def main():
    scrapingsite = sys.argv[1]
    if scrapingsite == "startup-india":
        startup_india_scraping()
    elif scrapingsite == "1000startups":
        startup1000()
    elif scrapingsite == "industry_scrape":
        industry_filter_scrape()
    elif scrapingsite == "sector_scraping":
        sector_filter_scrape()


if __name__ == "__main__":
    main()
