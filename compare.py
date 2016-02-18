# -*- coding: utf-8 -*-

from utils.wikisource import get_page
from utils.djvu_utils import parse_book
import utils.string_utils as su
import sys

wikibook = sys.argv[1].replace(" ", "_")

n = 88
ocrpage = parse_book(wikibook, n)
l1, c1 = zip(*ocrpage[0])
l1 = list(l1)
c1 = list(c1)
l2 = get_page(wikibook, n)
l3 = su.simplify(unicode(l2))
C = su.align(l3.split(), l1, c1)
su.print_alignment(unicode(l2).split(), l1, c1, C[1])
