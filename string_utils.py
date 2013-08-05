# -*- coding: utf-8 -*-
from Levenshtein import distance as levenshtein

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

def join_words(l):
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return l[0]
    else:
        if l[-2][-1] == "-":
            l[-2] = l[-2][:-1]
        return "".join(l)

def align(l1, l2):
    """Compute the optimal alignment between two list of words
    à la Needleman-Wunsch.

    The function returns a (score, alignment) pair. An alignment is simply
    a list of size len(l1) giving for each word in l1, the index of the word in
    l2 it maps to (or -1 if the word maps to nothing).

    Note that we also allow the index to be a tuple when a word in l1 maps to
    a sequence of words in l2. Conversly, consecutive words in l1 can map to
    the same word in l2.
    """

    # Throughout the function, l1 is to be thought of as the proofread text,
    # and l2 as the OCR text. The deletion costs are not symmetric: removing
    # junk from the OCR is frequent while removing a word from the proofread
    # text should be rare.
    del_cost1 = 20
    del_cost2 = 3
    w = 2 # multiplicative cost factor for the Levenshtein distance

    n, m = len(l1), len(l2)
    # a is the (score, alignment) matrix. a[i][j] is the (score, alignment)
    # pair of the first i words of l1 to the first j words of l2
    a = [[(0, [])] * (m + 1) for i in xrange(n + 1)]

    for j in xrange(1, m + 1):
        a[0][j] = del_cost2 * j, []

    for i in xrange(1, n + 1):
        a[i][0] = i * del_cost1, [-1] * i

        for j in xrange(1, m + 1):
            l = [] # contains the different options

            # mapping l1[i-1] to l2[j-1]
            s, b = a[i-1][j-1]
            d = levenshtein(l1[i-1], l2[j-1])
            l.append((s + w * d, b + [j-1]))

            # deleting l1[i-1]
            s, b = a[i-1][j]
            l.append((s + del_cost1, b + [-1]))

            # deleting l2[j-1]
            s, b = a[i][j-1]
            l.append((s + del_cost2, b))

            if (j >= 2): # mapping l1[i-1] to l2[j-2] + l2[j-1]
                s, b = a[i-1][j-2]
                d = levenshtein(l1[i-1], join_words(l2[j-2:j]))
                l.append((s + w * d, b + [(j-2, j-1)]))

            if (i >= 2): # mapping l1[i-2]+l1[i-1] to l2[j-1]
                s, b = a[i-2][j-1]
                d = levenshtein(join_words(l1[i-2:i]), l2[j-1])
                l.append((s + w * d, b + [j-1, j-1]))

            a[i][j] = min(l, key=lambda x: x[0])

    return a[n][m]

def print_alignment(l1, l2, alignment):
    """Given two list of words and an alignment (as defined in :func:`align`)
    print the two list of words side-by-side and aligned.
    """

    # collapse sequence of consecutive words in l1 which map to the same word
    # in l2
    def aux((l, m), (word, index)):
        if index == m[-1]:
            l[-1] += " " + word
        else:
            l.append(word)
            m.append(index)
        return l, m
    l1, alignment = reduce(aux, zip(l1, alignment), ([""],  [alignment[0]]))

    prev = 0
    for (i, word) in enumerate(l1):
        if alignment[i] == -1:
            print u"{0:>25} | ".format(word)
        else:
            if type(alignment[i]) == tuple:
                begin, end = alignment[i][0], alignment[i][-1]
            else:
                begin, end = alignment[i], alignment[i]
            while prev < begin - 1:
                prev += 1
                print u"{0:>25} | {1}".format("", l2[prev])
            prev = end

            if end > begin:
                if end == begin + 1:
                    l, r = cut(word, l2[begin], l2[end])
                    print u"(S) {0:>21} | {1:<25}".format(l, l2[begin])
                    print u"(S) {0:>21} | {1:<25}".format(r, l2[end])
                else:
                    print u"{0:>25} | {1:<25} (M)".format(word,
                                                          join_words(l2[begin:end+1]))
            else:
                print u"{0:>25} | {1:<25}".format(word, l2[begin])
