
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

def hash_substr(string, i, j, prime=31):
    """
    Map a sub-sequence of characters to an integer. This works by
    mapping each individual character to an integer via ord(), then
    multiplying it by a prime number P raised to some power.

    Ex:
    Lets hash the string "cat"
    ord('t') = 116
    ord('a') = 97
    ord('c') = 99

    Let P = prime = 31. Then hash_substr("cat") is:
    ord('c')*pow(P, 2) + ord('a')*pow(P, 1) + ord('t')*pow(P, 0)

    Args:
    string (string): the sequence of characters containing some subsequence we want to hash

    i (int): the starting index of the subsequence to hash

    j (int): the ending index of the subsequence to hash

    prime (int): Optional. The prime number to multiply each ord(character) by

    Returns:

    (int) The integer representation of the character subsequence
    starting at string[i] and ending at string[j]

    """
    if i < 0:
        raise IndexError("i must be >= 0, is {}".format(i))

    if j >= len(string):
        raise IndexError("j must be < len(string), is {}".format(j))

    if i > j:
        raise IndexError("i must be <= j. (i = {}, j = {})".format(i, j))

    res = 0
    mult = 1
    N = j - i + 1
    i = N - 1

    while i >= 0:
        res += (mult * ord(string[i]))
        mult *= prime
        i -= 1

    return res

def hash_str(word, N, prime=31):
    return hash_substr(word, 0, N-1, prime=prime)

def find_all_N(string, words, N, res_list=None, P=31):
    
    """
    Find all words of some fixed length N using Rabin-Karp.

    """
    # NOTE: let's be thankful that ord() takes into account Unicode:
    # https://docs.python.org/2/library/functions.html#ord

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
    table = {hash_str(word, N): word for word in words}

    max_pow = pow(P, N-1)
    rhash = None
    ln = M - N + 1

    # Unroll the loop once so that we don't check conditionals inside
    # of the loop and compute the initial rolling hash
    i = 0
    rhash = hash_substr(string, i, i+N-1)
        
    if rhash in table:
        word = table[rhash]
        match = True

        j = 0
        while j < N:
            if string[j+i] != word[j]:
                match = False
                break
            j += 1

        if match:
            # (word, start, end)
            res.append((word, i, i+N))
    
    i = 1
    while i < ln:
        # Rolling hash function of Rabin-Karp. This is based on the
        # observation that H(i+1) can be computed from H(i) in
        # constant time.

        # Starting term of the previous hash value.
        # t1 = ord(string[i-1]) * max_pow

        # Ending term of the current hash value. It is multiplied
        # by P^0, which is always 1. So just omit for brevity.
        # t2 = ord(string[i+N-1])
        rhash = ((rhash - (ord(string[i-1]) * max_pow)) * P) + ord(string[i+N-1])
        
        if rhash in table:
            word = table[rhash]

            # We have a collision via hashing. By the Pigeonhole
            # principle, if we map a set of cardinality M to a set of
            # cardinality N and M > N, then there must exist at least
            # one bucket containing at least two elements. In other
            # words, two different strings can map to the same integer
            # via hashing. So compare the substring char-by-char to
            # make sure we have a match.
            match = True

            # Use range since N is typically small
            j = 0
            while j < N:
                if string[j+i] != word[j]:
                    match = False
                    break
                j += 1

            if match:
                # (word, start, end)
                res.append((word, i, i+N))

        i += 1
        
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
