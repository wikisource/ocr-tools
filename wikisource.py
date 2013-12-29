# -*- coding: utf-8 -*-
import requests
import lxml
import sys
from bs4 import BeautifulSoup
from itertools import takewhile, count

URL = "http://fr.wikisource.org/w/index.php"

def get_page(title, page):
    params = { "action": "render", "title": "Page:" + title + "/" + str(page) }
    r = requests.get(URL, params=params)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "lxml")
        return soup.select("div.pagetext")[0].text
    else:
        return None

def get_pages(title, begin=1, end=None):
    if end:
        return (get_page(title, i) for i in xrange(begin, end+1))
    else:
        return takewhile(lambda x: x is not None,
                         (get_page(title, i) for i in count(begin)))


if __name__ == "__main__":
    title = sys.argv[1]
    for page in get_pages(title):
        print page


def f(i):
    if i <=10:
        return i**2
