import sys
from bs4 import BeautifulSoup
import subprocess

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

def parse_page_sexp(djvubook, pagenumber):
    args = ["djvused", "-e", "select {0};print-txt".format(pagenumber),
            djvubook]
    page = [parse_wordline(line) for line in \
            subprocess.check_output(args).split("\n") if "word" in line]
    return {"words": [a for a, b in page], "coords": [b for a, b in page]}

def parse_book_sexp(djvubook):
    book = {"words": [], "coords": []}
    page_coords = []
    page_words = []
    firstpage = True
    args = ["djvused", "-e", "print-txt", djvubook]
    for line in subprocess.check_output(args).split("\n"):
        if "page" in line:
            if firstpage:
                firstpage = False
            else:
                book["words"].append(page_words)
                book["coords"].append(page_coords)
                page_coords = []
                page_words = []
        if "word" in line:
            word, coords = parse_wordline(line)
            page_words.append(word)
            page_coords.append(coords)
    return book

if __name__=="__main__":
    book_sexp = parse_book_sexp(sys.argv[1])
