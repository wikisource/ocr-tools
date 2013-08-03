import sys
from xml.etree import ElementTree as ET

def parse_coords(word):
    # coordinates are in dpi, and computed from the top left corner
    return tuple([word.attrib[c] for c in ['xMin', 'xMax', 'yMin', 'yMax']])

def parse_book(book):
    document = ET.parse(book)
    ns = 'http://www.w3.org/1999/xhtml'

    words = []
    coords = []
    for page in document.findall('.//{{{0}}}page'.format(ns)):
        words.append([word.text for word in page.getchildren()])
        coords.append([parse_coords(word) for word in page.getchildren()])
    return {"words": words, "coords": coords}

if __name__=="__main__":
    book = parse_book(sys.argv[1])
    print book['words'][14]
