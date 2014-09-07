# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup, NavigableString
from itertools import takewhile, count
from types import SliceType
import string_utils as su
import djvu_utils as du

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
            return [unicode(self[w]) for w in range(*key.indices(self.length))]
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
        return HtmlText(soup.select("div.pagetext")[0])
    else:
        return None

def get_pages(title, begin=1, end=None):
    if end:
        return (get_page(title, i) for i in xrange(begin, end + 1))
    else:
        return takewhile(lambda x: x is not None,
                         (get_page(title, i) for i in count(begin)))

def gen_html(book, page_number):
    doc = du.get_document(book)
    page = doc.pages[int(page_number)-1]
    d = du.parse_page(page)
    corrected_text = get_page(book, int(page_number))
    corrected_words = su.simplify(corrected_text.elem.text).split()
    if d:
        orig_words, orig_coords = zip(*d)
        C = su.align(corrected_words, list(orig_words), list(orig_coords))
        corr_words = corrected_text
        orig_coords_html = du.convert_to_htmlcoord(orig_coords, page.size[1])
    return orig_coords_html, orig_words, corr_words, C[1]

if __name__ == "__main__":
    wikibook = "Bloy - Le Sang du pauvre, Stock, 1932.djvu".replace(" ", "_")
    test = get_page(wikibook, 28)
    # print type(c[0])
    # print su.align(c, [u"asd"], None)
    # print c[0:1]
