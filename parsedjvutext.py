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
        coords.append([tuple(map(int, word["coords"].split(","))) \
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
    coords = [tuple(map(int, word["coords"].split(","))) \
                for word in all_words]
    return {"words": words, "coords": coords}

def parse_wordline(line):
    line = line.lstrip(" (").rstrip(")").split(" ")
    word = line[5]
    word = word[1:-1].decode("string_escape").decode("utf-8")
    coords = map(int, line[1:5])
    return word, coords

def page_sexp(djvubook, pagenumber):
    args = ["djvused", "-e", "select {0};print-txt".format(pagenumber),
            djvubook]
    return subprocess.check_output(args).split("\n")

def parse_page_sexp(djvubook, pagenumber):
    page = [parse_wordline(line) for line in page_sexp(djvubook, pagenumber) \
            if "word" in line]
    return {"words": [a for a, b in page], "coords": [b for a, b in page]}

def parse_sexp(s):
    if type(s) is djvu.sexpr.ListExpression:
        if len(s) == 0:
            return []
        if str(s[0].value) == "word":
            coords = [s[i].value for i in xrange(1, 5)]
            word = s[5].value
            return [(word, coords)]
        else:
            gen = chain.from_iterable(parse_sexp(child) for child in s[5:])
            return list(gen)
    else:
        return []

def parse_book_sexp(djvubook, page=None, html=False):
    """
    returns the list of words and coordinates from a djvu book.
    if page is None, returns the whole book.
    if html is True, coordinates are computed from the bottom of the page
    """
    book = {"words": [], "coords": []}
    c = Context()
    document = c.new_document(djvu.decode.FileURI(djvubook))
    document.decoding_job.wait()
    if page:
        toparse = [document.pages[page-1]]
    else:
        toparse = document.pages
    for page in toparse:
        gen = parse_sexp(page.text.sexpr)
        word_coords = zip(*gen)
        book["words"].append(word_coords[0])
        book["coords"].append(word_coords[1])
    return book

if __name__=="__main__":
    book_sexp = parse_book_sexp(sys.argv[1])
