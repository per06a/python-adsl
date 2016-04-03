
"""
Common data, functions and classes shared between at least two
modules.

"""

__author__ = 'prussell'

##### STDLIB
from random import randint

##### 3RD PARTY

##### PROJECT

##### INIT AND DECLARATIONS

##### CLASSES AND FUNCTIONS

def swap(array, i, j):
    # x = x ^ y, y = y ^ x, x = x ^ y doesn't work for pointers...
    tmp = array[i]
    array[i] = array[j]
    array[j] = tmp

def partition(array, left, right, pivot):
    
    pivot_val = array[pivot]

    # Move pivot to right
    swap(array, pivot, right)

    store = left

    for i in range(left, right):
        # left <= i < right
        if array[i] <= pivot_val:
            swap(array, i, store)
            store += 1

    # Move the pivot_val back to the store location
    swap(array, right, store)

    return store

def mo3(left, right):
    
    """
    Constant-time Median-Of-Three function

    """
    v1 = randint(left, right)
    v2 = randint(left, right)
    v3 = randint(left, right)

    if v1 <= v2 <= v3:
        return v2

    elif v1 <= v3 <= v2:
        return v3

    elif v2 <= v1 <= v3:
        return v1

    elif v2 <= v3 <= v1:
        return v3

    elif v3 <= v1 <= v2:
        return v1

    else:
    #v3 <= v2 <= v1:
        return v2
