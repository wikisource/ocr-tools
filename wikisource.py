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
    return soup.select("div.pagetext")[0]

def get_book(title):
    n_pages = 10
    return [get_page(title, page) for page in xrange(1, n_pages)]

if __name__ == "__main__":
    title = sys.argv[1]
    print get_book(title)
