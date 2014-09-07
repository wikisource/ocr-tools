# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup, NavigableString
from itertools import takewhile, count
from types import SliceType
from string_utils import align

URL = "http://fr.wikisource.org/w/index.php"


def spanify(string, start=0):
    soup = BeautifulSoup()
    for i, word in enumerate(string.split()):
        span = soup.new_tag("span", id="word-" + str(start + i))
        span.string = word
        string.insert_before(span)
        string.insert_before(" ")
    string.replace_with("")
    return start + i + 1


class HtmlText():

    def __init__(self, elem):
        self.elem = elem
        start = 0
        strings = list(string for string in self.elem.strings
                       if string.strip())

        for string in strings:
            start = spanify(string, start)
        self.length = start

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if type(key) is SliceType:
            return [self[w] for w in range(*key.indices(self.length))]
        if key >= self.length:
            raise IndexError
        if key < 0:
            key = self.length - key
        return self.elem.find("span", {"id": "word-" + str(key)}).text

    def __str__(self):
        return str(self.elem)


def get_page(title, page):
    params = {"action": "render", "title": "Page:" + title + "/" + str(page)}
    r = requests.get(URL, params=params)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "lxml")
        return soup.select("div.pagetext")[0].text
    else:
        return None


def get_page2(text):
    soup = BeautifulSoup(text, "lxml")
    elem = soup.select("div.pagetext")[0]
    return HtmlText(elem), elem.text


def get_pages(title, begin=1, end=None):
    if end:
        return (get_page(title, i) for i in xrange(begin, end + 1))
    else:
        return takewhile(lambda x: x is not None,
                         (get_page(title, i) for i in count(begin)))


if __name__ == "__main__":
    b = BeautifulSoup("<a>asd</a>")
    c = HtmlText(b)
    print type(c[0])
    print align(c, [u"asd"], None)
    print c[0:1]
