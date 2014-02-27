import sys
from bs4 import BeautifulSoup
import subprocess
import djvu
from djvu.decode import Context
from itertools import chain
import collections

def parse_page(page, html=False):
    s, page_size = page.text.sexpr, page.size[1]

    def aux(s, html):
        if type(s) is djvu.sexpr.ListExpression:
            if len(s) == 0:
                pass
            if str(s[0].value) == "word":
                if html:
                    coords = (s[1].value, page_size - s[2].value,
                              s[3].value, page_size - s[4].value)
                    coords = ",".join(map(str,coords))
                else:
                    coords = [s[i].value for i in xrange(1, 5)]
                word = s[5].value
                yield (word, coords)
            else:
                for c in chain.from_iterable(aux(child, html) for child in s[5:]):
                    yield c
        else:
            pass
    return aux(s, html)


def parse_book(djvubook, page=None, html=False):
    """
    returns the list of words and coordinates from a djvu book.
    if page is None, returns the whole book.
    if html is True, coordinates are computed from the bottom of the page
    """
    c = Context()
    document = c.new_document(djvu.decode.FileURI(djvubook))
    document.decoding_job.wait()
    if type(page) is int:
        toparse = [document.pages[page - 1]]
    elif isinstance(page, collections.Iterable):
        toparse = page
    else:
        toparse = document.pages

    return list(zip(*parse_page(page, html=html)) for page in toparse
                if page.text.sexpr)

if __name__ == "__main__":
    book = parse_book(sys.argv[1])
