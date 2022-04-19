import os
import re
import json
from prometheus_client import Summary
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
driver = webdriver.Chrome(service=service, options=options)


def summary_formatter(summary):
    joined_summary = "|".join(str(e) for e in summary)
    return joined_summary


def content_scraping(link):
    blog_summary = []
    page = f"{link}"
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html5lib")
    for para in soup.find_all("div", class_="entry-content clearfix"):
        text = para.get_text()
        break
    text = text.rsplit(".")
    text.pop(-1)
    blog = ".".join(str(e) for e in text)
    summary_lines = soup.find("div", class_="single-post-summary")
    for lines in summary_lines.find_all("p"):
        lines = lines.get_text()
        blog_summary.append(lines)
    return blog, blog_summary


def home_page_scrapper(count):
    links = []
    titles = []
    blogs = []
    summaries = []
    page = f"https://inc42.com/buzz/page/{count}"
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html5lib")
    news_cards = soup.find_all("div", class_="card-content")
    for cards in news_cards:
        headline = cards.h2.text
        headline = headline.strip("\n")
        link = cards.h2.a["href"]
        blog, blog_summary = content_scraping(link)
        blog = blog.replace("\n", "")
        blog = blog.replace("\xa0", " ")
        links.append(link)
        titles.append(headline)
        blogs.append(blog)
        summary = summary_formatter(blog_summary)
        summaries.append(summary)
        # print(blog)
    return titles, links, blogs, summaries


def main():
    count = 0
    while count < 10:
        titles, links, blogs, summaries = home_page_scrapper(count)
        # print(titles)
        # print(links)
        # print(blogs)
        # print(summaries)
        rows = pd.DataFrame(
            {"Title": titles, "Link": links, "Blog": blogs, "Summary": summaries}
        )
        # rows = pd.DataFrame({'Title':titles,'Link':links,'Summary':summaries})
        rows.to_csv("inc42/blogs_new.csv", index=False, mode="a", header=False)
        print("page ", count)
        count += 1


if __name__ == "__main__":
    main()
