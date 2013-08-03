import pdb
from wikisource import get_page
from parsedjvutext import parse_book
import lcs

wikibook = "Villiers de L'Isle-Adam - Tribulat Bonhomet, 1908.djvu"
ocrbook = "Tribulat Bonhomet.xml"

ocrbook = parse_book(ocrbook)

n = 14
l1 = ocrbook['words'][n]
l2 = get_page(wikibook, n+1).split()
C = lcs.LCS(l1, l2)
lcs.printDiff(C, l1, l2, len(l1), len(l2))
