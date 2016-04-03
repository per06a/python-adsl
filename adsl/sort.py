
"""
Various sorting algorithms

"""

##### STDLIB

##### 3RD PARTY

##### PROJECT
import adsl.common
import adsl.heap

##### INIT AND DECLARATIONS

##### CLASSES AND FUNCTIONS

def quicksort(array, left=None, right=None):
    
    if left is None:
        left = 0

    if right is None:
        right = len(array) - 1

    if left < right:
        pivot = adsl.common.mo3(left, right)
        
        pivot = adsl.common.partition(array, left, right, pivot)

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

def heapsort(array):
    return BinaryHeap.heapsort(array)
