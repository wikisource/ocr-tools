# -*- coding: utf-8 -*-

from wikisource import get_page
from parsedjvutext import parse_book
import string_utils as su

wikibook = "Bloy - Le Sang du pauvre, Stock, 1932.djvu".replace(" ", "_")
#wikibook = "Villiers de L'Isle-Adam - Tribulat Bonhomet, 1908.djvu".replace(" ", "_")

n = 88
ocrpage = parse_book(wikibook, n)
l1, c1 = zip(*ocrpage[0])
l1 = list(l1)
c1 = list(c1)
l2 = get_page(wikibook, n)
l3 = su.simplify(l2)
C = su.align(l3.split(), l1, c1)
su.print_alignment(l2.split(), l1, c1, C[1])
