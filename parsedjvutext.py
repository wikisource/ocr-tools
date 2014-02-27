import sys
from bs4 import BeautifulSoup
import subprocess
import djvu
from djvu.decode import Context
from itertools import chain


def parse_book_xml(djvubook):
    args = ["djvutoxml", djvubook]
    soup = BeautifulSoup(subprocess.check_output(args), "lxml")
    words = []
    coords = []
    for page in soup.find_all("hiddentext"):
        words.append([word.text for word in page.find_all("word")])
        coords.append([tuple(map(int, word["coords"].split(",")))
                       for word in page.find_all("word")])
    return {"words": words, "coords": coords}


def get_npages(djvubook):
    args = ["djvused", "-e", "n", djvubook]
    return int(subprocess.check_output(args))


def parse_page_xml(djvubook, pagenumber):
    args = ["djvutoxml", "--page", str(pagenumber), djvubook]
    soup = BeautifulSoup(subprocess.check_output(args), "lxml")
    all_words = soup.find_all("word")
    words = [word.text for word in all_words]
    coords = [tuple(map(int, word["coords"].split(",")))
              for word in all_words]
    return {"words": words, "coords": coords}


def parse_page(page, html=False):
    s, page_size = page.text.sexpr, page.size[1]

    def aux(s):
        if type(s) is djvu.sexpr.ListExpression:
            if len(s) == 0:
                pass
            if str(s[0].value) == "word":
                coords = [s[i].value for i in xrange(1, 5)]
                if html:
                    coords[1] = page_size - coords[1]
                    coords[3] = page_size - coords[3]
                word = s[5].value
                yield (word, coords)
            else:
                for c in chain.from_iterable(aux(child) for child in s[5:]):
                    yield c
        else:
            pass
    return aux(s)


def parse_book(djvubook, page=None, html=False):
    """
    returns the list of words and coordinates from a djvu book.
    if page is None, returns the whole book.
    if html is True, coordinates are computed from the bottom of the page
    """
    c = Context()
    document = c.new_document(djvu.decode.FileURI(djvubook))
    document.decoding_job.wait()
    if page:
        toparse = [document.pages[page - 1]]
    else:
        toparse = document.pages

    return list(zip(*parse_page(page, html=html)) for page in toparse
                if page.text.sexpr)

if __name__ == "__main__":
    book = parse_book(sys.argv[1])
