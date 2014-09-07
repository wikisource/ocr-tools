import sys
from bs4 import BeautifulSoup
import djvu
from djvu.decode import Context
from itertools import chain
import collections
from PIL import Image

def parse_page(page):
    s = page.text.sexpr

    def aux(s):
        if type(s) is djvu.sexpr.ListExpression:
            if len(s) == 0:
                pass
            if str(s[0].value) == "word":
                coords = [s[i].value for i in xrange(1, 5)]
                word = s[5].value
                yield (word.decode("utf-8"), coords)
            else:
                for c in chain.from_iterable(aux(child) for child in s[5:]):
                    yield c
        else:
            pass
    return aux(s) if s else None

def convert_to_htmlcoord(coords, page_size):
    return [",".join(map(str, [c[0], page_size - c[3],
                               c[2], page_size - c[1]])) for c in coords]

def get_document(djvufile):
    c = Context()
    document = c.new_document(djvu.decode.FileURI(djvufile))
    document.decoding_job.wait()
    return document

def parse_book(djvubook, page=None):
    """
    returns the list of words and coordinates from a djvu book.
    if page is None, returns the whole book.
    """
    document = get_document(djvubook)

    if type(page) is int:
        toparse = [document.pages[page - 1]]
    elif isinstance(page, collections.Iterable):
        toparse = [document.pages[p - 1] for p in page]
    else:
        toparse = document.pages

    return [parse_page(page) for page in toparse]

def image_from_book(djvubook, page):
    document = get_document(djvubook)
    mode = djvu.decode.RENDER_COLOR
    djvu_pixel_format = djvu.decode.PixelFormatRgb()
    page = document.pages[page-1]
    page_job = page.decode(wait=True)
    width, height = page_job.size
    rect = (0, 0, width, height)
    buf = page_job.render(mode, rect, rect, djvu_pixel_format)
    return Image.frombuffer("RGB", (width, height), buf, 'raw', 'RGB', 0, -1)

if __name__ == "__main__":
    book = parse_book(sys.argv[1], page=[10,11], html=True)
    im = image_from_book(sys.argv[1], 11)
    im.save("test.jpeg")
