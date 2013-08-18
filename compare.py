# -*- coding: utf-8 -*-

from wikisource import get_page
from parsedjvutext import page_sexp, parse_page_sexp
import string_utils as su
import pdb

wikibook = "Bloy - Le Sang du pauvre, Stock, 1932.djvu".replace(" ", "_")
#wikibook = "Villiers de L'Isle-Adam - Tribulat Bonhomet, 1908.djvu".replace(" ", "_")

n = 88
ocrpage = parse_page_sexp(wikibook, n)
l1, c1 = ocrpage['words'], ocrpage["coords"]
l2 = get_page(wikibook, n)
print len(l2.split())
l3 = su.simplify(l2)
C = su.align(l3.split(), l1, c1)
pdb.set_trace()
sexp = page_sexp(wikibook, n)
su.alignment_to_sexp(C[1], sexp, l2.split())
su.print_alignment(l2.split(), l1, c1, C[1])
