# -*- coding: utf-8 -*-
from Levenshtein import distance as levenshtein
import re
import itertools

def simplify(text):
    mapp = [(u"’", u"'"), (u"↑", u"."), (u"…", u"..."), (u"É", u"E"),
            (u"À", u"A"), (u"Ô", u"O"), (u"—", u"-")]

    for a, b in mapp:
        text = text.replace(a, b)

    return text

def cut(word, left, right):
    """Return pair of strings (p + "-", s) such that p+s == word and
    L(p + "-", left) + L(s, right) is minimal, where L is the levenshtein
    distance.

    Implementation is suboptimal since the computation of the Levenshtein
    distances will involve comparing the same segments repeatedly.

    TODO: handle the case when word contains an hyphen (e.g. c'est-a-dire)
    """

    def aux(i):
        leftw, rightw = word[:i] + "-", word[i:]
        return (leftw, rightw,
                levenshtein(leftw, left) + levenshtein(rightw, right))

    l = [aux(i) for i in xrange(len(word) + 1)]
    return min(l, key=lambda x: x[2])[:2]

def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n+1) for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def printDiff(C, X, Y, i, j):
    if i > 0 and j > 0 and X[i-1] == Y[j-1]:
        printDiff(C, X, Y, i-1, j-1)
        print "  " + X[i-1]
    else:
        if j > 0 and (i == 0 or C[i][j-1] >= C[i-1][j]):
            printDiff(C, X, Y, i, j-1)
            print "+ " + Y[j-1]
        elif i > 0 and (j == 0 or C[i][j-1] < C[i-1][j]):
            printDiff(C, X, Y, i-1, j)
            print "- " + X[i-1]

def join_ocr_words(l, c):
    m = list(l)
    if len(l) >= 2 and c[-2][2] > c[-1][0] and (not l[-2][-1].isalnum()):
        l[-2] = l[-2][:-1]
    return "".join(l)

def join_words(l):
    return "".join(l)

def align(l1, l2, c2):
    """Compute the optimal alignment between two list of words
    à la Needleman-Wunsch.

    The function returns a (score, alignment) pair. An alignment is simply
    a list of list of size len(l1) giving for each word in l1, the list of
    indices in l2 it maps to (the list is empty if the word maps to nothing).

    Note that if the list is of size>1, the word in l1 will map to a sequence
    of words in l2. Conversly, consecutive words in l1 can map to
    the same word in l2.
    """

    # Throughout the function, l1 is to be thought of as the proofread text,
    # and l2 as the OCR text. The deletion costs are not symmetric: removing
    # junk from the OCR is frequent while removing a word from the proofread
    # text should be rare.
    del_cost1 = 50
    def del_cost2(w):
        return 1+3*len([c for c in w if c.isalnum()])
    w = 3 # multiplicative cost factor for the Levenshtein distance

    n, m = len(l1), len(l2)
    # a is the (score, alignment) matrix. a[i][j] is the (score, alignment)
    # pair of the first i words of l1 to the first j words of l2
    a = [[(0, [])] * (m + 1) for i in xrange(n + 1)]

    for j in xrange(1, m + 1):
        a[0][j] = j, []

    for i in xrange(1, n + 1):
        a[i][0] = i * del_cost1, [[]] * i

        for j in xrange(1, m + 1):

            s, b = a[i-1][j-1]
            d = levenshtein(l1[i-1], l2[j-1])
            min_s, min_b  = s + w * d, b + [[j-1]]

            s, b = a[i-1][j]
            if s + del_cost1 < min_s:
                min_s, min_b = s + del_cost1, b + [[]]

            s, b = a[i][j-1]
            if s + del_cost2(l2[j-1]) < min_s:
                min_s, min_b = s + del_cost2(l2[j-1]), b

            for k in xrange(1, 8):
                for l in xrange(1, 5):
                    if k + l <= 2:
                        continue
                    if k+l > 7:
                        break
                    if j < l or i < k:
                        break
                    s, b = a[i-k][j-l]
                    d = levenshtein(join_words(l1[i-k:i]),
                                    join_ocr_words(l2[j-l:j], c2[j-l:j]))
                    if s + w * d < min_s:
                        temp = [[j-1]] if l == 1 else [range(j-l, j)]
                        min_s, min_b = s + w * d, b + temp * k

            a[i][j] = min_s, min_b

    return a[n][m]

def print_alignment(l1, l2, c2, alignment):
    """Given two list of words and an alignment (as defined in :func:`align`)
    print the two list of words side-by-side and aligned.
    """
    prev = 0
    for index, g in itertools.groupby(zip(l1, alignment), lambda x:x[1]):
        word = " ".join([a[0] for a in g])
        if not index:
            print u"{0:>25} | ".format(word)
        else:
            begin, end = index[0], index[-1]
            for i in range(prev, begin-1):
                print u"{0:>25} | {1}".format("", l2[i+1])
            prev = end

            if end > begin:
                print u"{0:>25} | {1:<25} (M)".format(word,
                                                      join_ocr_words(l2[begin:end+1], c2[begin:end+1]))
            else:
                print u"{0:>25} | {1:<25}".format(word, l2[begin])

    if not l1:
        for word in l2:
            print u"{0:>25} | {1}".format("", word)

def alignment_to_coord(l1, alignment):
    # l1 list of corrected words
    # alignment list of size len(l1) qui mappe mots dans l2
    # returns indices in l2

    r = []
    prev = 0
    for index, g in itertools.groupby(zip(l1, alignment), lambda x:x[1]):
        word = " ".join([a[0] for a in g])
        if not index:
            r.append([word, None])
        else:
            begin, end = index[0], index[-1]
            if end > begin:
                #need to find a better way to get the box coordinates
                r.append([word, begin])
            else:
                r.append([word, begin])
    return r
