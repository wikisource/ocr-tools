# -*- coding: utf-8 -*-

def levenshtein(word1, word2):
    """Return triplet of number of (substitutions, insertions, deletions) to
    transform word1 into word2.

    Dynamic programming implementation storing only two rows of the full matrix
    at a time.

    TODO: write this in a Cython module.
    """

    s, t = len(word1), len(word2)
    if word1 == word2:
        return 0
    if not min(s, t):
        return max(s, t)

    v0 = [i for i in xrange(t + 1)] # v0[i] is d(0, i)
    v1 = [0] * (t + 1)
    for i in xrange(s):
        # v0[j] = d(i, j) for all j and we compute v1[j] = d(i+1, j) for all j
        v1[0] = i + 1

        for j in xrange(t):
            diff = int(word1[i] != word2[j])
            v1[j+1] = min(v1[j] + 1, v0[j+1] + 1, v0[j] + diff)

        v0 = list(v1) # copy v1 into v0 for the next iteration

    return v1[t]

def cut(word, left, right):
    """Return pair of strings (p + "-", s) such that p+s == word and
    L(p + "-", left) + L(s, right) is minimal, where L is the levenshtein
    distance.

    Implementation is suboptimal since the computation of the Levenshtein
    distances will involve comparing the same segments repeatedly.

    TODO: handle the case when word contains an hyphen (e.g. c'est-à-dire)
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
