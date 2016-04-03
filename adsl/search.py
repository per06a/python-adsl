
"""
Various searching, selecting and finding algorithms

"""

##### STDLIB

##### 3RD PARTY

##### PROJECT
import adsl.common

##### INIT AND DECLARATIONS

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
