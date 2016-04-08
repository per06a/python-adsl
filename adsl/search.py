
"""
Various searching, selecting and finding algorithms

"""

##### STDLIB
import sys

##### 3RD PARTY

##### PROJECT
import adsl.common

##### INIT AND DECLARATIONS
if sys.version_info.major >= 3:
    xrange = range

##### CLASSES AND FUNCTIONS

def binsearch(array, elem, left=None, right=None, cmp_func=cmp):

    """
    Classic binary search algorithm.

    Args:
    array (sequence): the sequence of elements that we are searching

    elem (object): the element that we are searching for

    left (int): the lower bound index of the sub-sequence to
    search for the element. Default is None, in which case it will
    start at position 0.

    right (int): the upper bound index of the sub-sequence to
    search for the element. Default is None, in which case it will
    start at len(array) - 1.

    cmp_func (function): function to compare two arbitrary
    elements. Must conform to the "negative for e1 < e2, 0 for e1 ==
    e2, positive for e1 > e2" comparison conventions. Default is the
    build-in Python 'cmp' function.

    Returns: 
    int: If the element is found in the sequence, the first
    position that it was found at. Else, None.

    """
    res = None

    if left is None:
        left = 0

    if right is None:
        right = len(array) - 1

    while left <= right:
        pivot = int((left+right)/2.0)

        pval = array[pivot]

        if cmp_func(elem, pval) == 0:
            # This is a position of the element in the array
            res = pivot
            break

        elif cmp_func(elem, pval) < 0:
            # The element must be in the lower half of the range if it
            # exists
            right = pivot - 1

        else:
            # The element must be in the upper half of the range if it
            # exists
            left = pivot + 1

    return res

def quickselect(array, K):
    """
    Find the K-th most element in the sequence.

    If we take an unordered sequence of elements and sorted them,
    which element would occupy position K (ie position 0, or 5, or
    19)?

    quickselect answers the above question in expected linear
    time. This is less than the usual N*lg(N) time we get for
    comparison-based sorting algorithms.

    quickselect works by repeatedly partioning sequences to establish
    'some element occupies the K+X or X-Y position'. Since we know the
    fixed position of one element, we can use that to determine which
    sub-range must contain the K-th element (if any).

    NOTE: this is essentially a neat combination of ideas from binary
    search and quicksort. It is a destructive search in that it
    partially sorts the sequence.

    """

    res = None
    left = 0
    right = len(array) - 1

    while left <= right:

        pivot = adsl.common.mo3(left, right)
        pivot = adsl.common.partition(array, left, right, pivot)

        # The pivot is now a fixed position of some element. We KNOW
        # that all elements <= array[pivot] are located in the lower
        # half, and all elements > array[pivot] are located in the
        # upper.

        if K == pivot:
            res = array[pivot]
            break

        elif K < pivot:
            # The K-th element must be in the lower range relative to pivot
            right = pivot - 1

        else:
            # The K-th element must be in the upper range relative to pivot
            left = pivot + 1

    return res

def find_all_N(string, words, N, res_list=None):
    
    """
    Find all words of some fixed length N using Rabin-Karp.

    TODO: implement Rolling Hash to get expected running time of O(M+N)

    """
    for word in words:
        if len(word) != N:
            raise ValueError("{} with length = {} is not of required length = {}".format(word,
                                                                                         len(word),
                                                                                         N))
    
    if res_list is None:
        res = []
    else:
        res = res_list

    M = len(string)

    # Table of hashes to words
    table = {hash(word): word for word in words}

    # NOTE: using xrange (for Python2) for this since M can be larger,
    # and xrange is an iterator. For Python3, xrange is defined in this module as range
    for i in xrange(0, M - N + 1):
        
        sub = string[i:i+N]

        hash_sub = hash(sub)
        
        if hash_sub in table:
            word = table[hash_sub]

            # Compare the words char-by-char
            match = True

            # Use range since N is typically small
            for j in range(0, N):
                if sub[j] != word[j]:
                    match = False
                    break

            if match:
                # (word, start, end)
                res.append((word, i, i+N))
        
    return res

def find_all(string, words):
    """
    Find all matching words in some string by bucket-sorting them by
    size and running all strings of the same length through
    Rabin-Karp.

    Let:
    M = len(string)
    N = the longest length of any word in words
    K = the total number of different word lengths

    The expected/best-case running time of Rabin-Karp is O(M+N). We
    call it at most K times. This gives us an expected running time of
    O(K*(M+N)).

    We can usually treat K as a constant. This reduces the expected
    running time back down to O(C*(M+N)) = O(M+N). For example, for
    the English dictionary locatd at /usr/shard/dict/words, K = 23.

    """

    res = []

    # Do a bucket sort of words by their length.
    table = {}
    
    for word in words:
        ln = len(word)
        if ln not in table:
            table[ln] = []

        table[ln].append(word)

    # Now use find_all_N with the same result list
    for N in table:
        # These are all the words of length N
        words_N = table[N]

        find_all_N(string, words_N, N, res_list=res)

    return res
