import sys
from bs4 import BeautifulSoup

def parse_book(book):
    words = []
    coords = []
    with open(book) as fh:
        soup = BeautifulSoup(fh, "lxml")
        for page in soup.find_all("hiddentext"):
            words.append([word.text for word in page.find_all("word")])
            coords.append([tuple(map(int, word["coords"].split(","))) \
                           for word in page.find_all("word")])
    return {"words": words, "coords": coords}

if __name__=="__main__":
    book = parse_book(sys.argv[1])
