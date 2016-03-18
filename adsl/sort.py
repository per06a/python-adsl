
"""
Various sorting algorithms

"""

##### STDLIB
from random import randint

##### 3RD PARTY

##### PROJECT

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

def quicksort(array, left=None, right=None):
    
    if left is None:
        left = 0

    if right is None:
        right = len(array) - 1

    if left < right:
        pivot = mo3(left, right)
        
        pivot = partition(array, left, right, pivot)

        quicksort(array, left, pivot - 1)
        quicksort(array, pivot + 1, right)

    return array

def merge(llist, rlist):
    
    res = []
    lpos = 0
    rpos = 0
    lln = len(llist)
    rln = len(rlist)

    while lpos < lln or rpos < rln:

        if lpos < lln and rpos < rln:
            if llist[lpos] <= rlist[rpos]:
                res.append(llist[lpos])
                lpos += 1

            else:
                res.append(rlist[rpos])
                rpos += 1

        elif lpos < lln:
            res.append(llist[lpos])
            lpos += 1

        else:
            res.append(rlist[rpos])
            rpos += 1

    return res

def mergesort(llist):

    if len(llist) <= 1:
        return llist

    pivot = int((0 + len(llist))/2.0)
    
    return merge(mergesort(llist[:pivot]),
                 mergesort(llist[pivot:]))


def insertsort(array):
    # Loop up, loop down

    ln = len(array)

    i = 0

    while i < ln:

        j = ln - 1

        while j > i:
            if array[j] < array[j-1]:
                tmp = array[j]
                array[j] = array[j-1]
                array[j-1] = tmp

            j -= 1
        
        i += 1

    return array
