from parsedjvutext import parse_book
import sys


def gen_html(book, page_number):
    book = "../Villiers_de_L'Isle-Adam_-_Tribulat_Bonhomet,_1908.djvu"
    d = parse_book(book, page=int(page_number), html=True)
    if d[0]:
        words, coords = zip(*d[0])

    return (list(enumerate(coords)), list(enumerate(words)))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
