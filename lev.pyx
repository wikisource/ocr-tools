from libc.stdlib cimport malloc, free
from Levenshtein import distance as levenshtein

cdef unicode join_words(list l):
    if len(l) >= 2 and l[-2][-1] == "-":
        l[-2] = l[-2][:-1]

    return "".join(l)

def align(list l1, list l2):
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
    cdef int del_cost1, del_cost2, n, m, i, j, k, l, s, d, min_s, w
    cdef list b, temp
    del_cost1 = 30
    del_cost2 = 2
    w = 1 # multiplicative cost factor for the Levenshtein distance

    n, m = len(l1), len(l2)
    # a is the (score, alignment) matrix. a[i][j] is the (score, alignment)
    # pair of the first i words of l1 to the first j words of l2
    a = [[(0, [])] * (m + 1) for i in xrange(n + 1)]

    for j in xrange(1, m + 1):
        a[0][j] = 0, []

    for i in xrange(1, n + 1):
        a[i][0] = del_cost1 * i, [-1] * i

        for j in xrange(1, m + 1):

            s, b = a[i-1][j-1]
            d = levenshtein(l1[i-1], l2[j-1])
            min_s = s + w * d
            min_b  = b + [j-1]

            s, b = a[i-1][j]
            if s + del_cost1 < min_s:
                min_s = s + del_cost1
                min_b = b + [-1]

            s, b = a[i][j-1]
            if s + del_cost2 < min_s:
                min_s = s + del_cost2
                min_b = b

            for k in xrange(1, 5):
                for l in xrange(1, 5):
                    if k + l <= 2:
                        continue
                    if k+l > 6:
                        break
                    if j < l or i < k:
                        break
                    s, b = a[i-k][j-l]
                    d = levenshtein(join_words(l1[i-k:i]),
                                    join_words(l2[j-l:j]))
                    if s + w * d < min_s:
                        temp = [j-1] if l == 1 else [tuple(range(j-l, j))]
                        min_s = s + w *d
                        min_b =  b + temp*k

            a[i][j] = min_s, min_b

    return a[n][m]
