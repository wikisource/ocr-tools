from parsedjvutext import parse_book
import sys


def gen_html(book, page_number):
    book = "../Villiers_de_L\'Isle-Adam_-_Tribulat_Bonhomet,_1908.djvu"
    d = parse_book(book, page=int(page_number), html=True)
    coords, words = d["coords"][0], d["words"][0]

    def get_areas():
        for i, coord in enumerate(coords):
            coord_str = ",".join(map(str, coord))
            yield i, coord_str

    return list(get_areas()), list(enumerate(words))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
