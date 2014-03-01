import djvu_utils as du
import sys
import string_utils as su
from wikisource import get_page

def gen_html(book, page_number):
    doc = du.get_document("../" + book)
    page = doc.pages[int(page_number)-1]
    d = du.parse_page(page)
    corrected_text = get_page(book, int(page_number))
    corrected_words = su.simplify(corrected_text).split()
    if d:
        words, coords = zip(*d)
        C = su.align(corrected_words, list(words), list(coords))
        r = su.alignment_to_sexp(corrected_text.split(), words, coords, C[1])
        corrected_words, coords = zip(*r)
        coords_html = du.convert_to_htmlcoord(coords, page.size[1])
    return (list(enumerate(coords_html)), list(enumerate(corrected_words)))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
