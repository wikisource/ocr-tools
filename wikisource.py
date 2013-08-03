# -*- coding: utf-8 -*-
import requests
import lxml
import sys
from bs4 import BeautifulSoup

URL="http://fr.wikisource.org/w/index.php"

def get_page(title, page):
    params = { "action": "render", "title": "Page:" + title + "/" + str(page) }
    r = requests.get(URL, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    return "".join(soup.select("div.pagetext")[0].findAll(text=True))

def get_pages(title, begin=1, end=None):
    if not end:
        end = 100
    for page in xrange(begin, end+1):
        yield get_page(title, page)

if __name__ == "__main__":
    title = sys.argv[1]
    for page in get_pages(title):
        print page
