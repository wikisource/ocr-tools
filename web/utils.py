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
        orig_words, orig_coords = zip(*d)
        C = su.align(corrected_words, list(orig_words), list(orig_coords))
        corr_words = corrected_text.split()
        orig_coords_html = du.convert_to_htmlcoord(orig_coords, page.size[1])
    return orig_coords_html, orig_words, corr_words, C[1]

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
