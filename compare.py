from wikisource import get_page
from parsedjvutext import parse_page_sexp
from string_utils import LCS, printDiff

wikibook = "Villiers de L'Isle-Adam - Tribulat Bonhomet, 1908.djvu"

n = 42
ocrpage = parse_page_sexp(wikibook, n)
l1 = ocrpage['words']
l2 = get_page(wikibook, n).split()
C = LCS(l1, l2)
printDiff(C, l1, l2, len(l1), len(l2))
