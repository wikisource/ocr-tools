from parsedjvutext import parse_book
import sys


def gen_html(book, page_number):
    book = "../Bloy_-_Le_Sang_du_pauvre,_Stock,_1932.djvu"
    d = parse_book(book, page=int(page_number), html=True)
    words, coords = d[0]

    return (list(enumerate(coords)), list(enumerate(words)))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
