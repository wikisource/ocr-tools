import djvu_utils as du
import sys
import string_utils as su
from wikisource import get_page2


def gen_html(book, page_number):
    doc = du.get_document("../" + book)
    page = doc.pages[int(page_number) - 1]
    d = du.parse_page(page)
    elem, corrected_text = get_page2(open("test.txt").read())
    if d:
        words, coords = zip(*d)
        C = su.align(corrected_text.split(), list(words), list(coords))
        coords = [coords[e[0]] for e in C[1]]
        coords_html = du.convert_to_htmlcoord(coords, page.size[1])
    return (list(enumerate(coords_html)), str(elem))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
