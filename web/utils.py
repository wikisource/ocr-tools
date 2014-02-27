from parsedjvutext import parse_page_sexp
import sys


def gen_html(book, page_number):
    book = "../Villiers_de_L\'Isle-Adam_-_Tribulat_Bonhomet,_1908.djvu"
    d = parse_page_sexp(book, page_number)
    coords, words = d["coords"], d["words"]

    def get_areas():
        for i, coord in enumerate(coords):
            coord[1], coord[3] = 2764 - coord[3], 2764 - coord[1]
            coord_str = ",".join(map(str, coord))
            yield i, coord_str

    return list(get_areas()), list(enumerate(words))

if __name__ == "__main__":
    gen_html(*sys.argv[1:3])
