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
        span = soup.new_tag("span")
        span["data-id"]=start + i
        span.string = word
        string.insert_before(span)
        string.insert_before(" ")
    string.replace_with("")
    return start + i + 1


class HtmlText(object):
    ## This class takes the corrected html from a wikisource page
    ## and adds extra information fo facilitate the mapping.
    ## At initialization, it wraps each word into a <span>
    ## with attribute data-id=i where i is the index of the corrected word.
    ## Once we set align, it adds to each span an id attribute
    ## of the form id="corr-x,y,z" where x, y, z are ids in
    ## the image map.
    def __init__(self, elem):
        self._elem = elem
        start = 0
        strings = list(string for string in self._elem.strings
                       if string.strip())

        for string in strings:
            start = spanify(string, start)
        self._length = start
        self._align = None

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        if type(key) is SliceType:
            return [unicode(self[w]) for w in range(*key.indices(self.length))]
        if key >= len(self):
            raise IndexError
        if key < 0:
            key = len(self) - key
        return self._elem.find("span", {"data-id": key}).text

    def __unicode__(self):
        return self._elem.text

    def __str__(self):
        return unicode(self).encode("utf-8")

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, val):
        self._align = val
        for i in range(len(self)):
            self._elem.find("span", {"data-id": i})['id']="corr-" + \
            ",".join(map(str, val[i]))

def get_page(title, page):
    title = title.split('/')[-1]
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
    d = du.parse_book(book, page_number)[0]
    corrected_text = get_page(book, int(page_number))
    corrected_words = su.simplify(unicode(corrected_text)).split()
    if d:
        orig_words, orig_coords = zip(*d)
        C = su.align(corrected_words, list(orig_words), list(orig_coords))
        corrected_text.align = C[1]
    return orig_coords, orig_words, corrected_text

if __name__ == "__main__":
    wikibook = sys.argv[1]
    test = gen_html(wikibook, 28)
    # print type(c[0])
    # print su.align(c, [u"asd"], None)
    # print c[0:1]
