# -*- coding: utf-8 -*-

from wikisource import get_page
from parsedjvutext import parse_page_sexp
import string_utils as su

wikibook = "Bloy - Le Sang du pauvre, Stock, 1932.djvu".replace(" ", "_")
# wikibook = "Villiers de L'Isle-Adam - Tribulat Bonhomet, 1908.djvu".replace(" ", "_")

n = 79
ocrpage = parse_page_sexp(wikibook, n)
l1 = ocrpage['words']
l2 = get_page(wikibook, n).replace(u"’", u"'").split()
C = su.align(l2, l1)
su.print_alignment(l2, l1, C[1])
