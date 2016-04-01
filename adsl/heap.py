
"""

"""

__author__ = 'prussell'

def default_compare(e1, e2):
    if e1 < e2:
        return -1
    elif e1 == e2:
        return 0
    else:
        return 1

class BinaryHeap(object):
    """

    """

    def __init__(self, comp_func=None):
        self.array = []
        if comp_func is None:
            self.compare = default_compare
        else:
            self.compare = comp_func
        
    def bubble_up(self, pos):
        
        cpos = pos

        while cpos > 0:
            
            ppos = int((cpos-1)/2.0)
            cval = self.array[cpos]
            pval = self.array[ppos]

            if cval < pval:
            #if self.compare(cval, pval) < 0:
                self.array[cpos] = pval
                self.array[ppos] = cval
                cpos = ppos

            else:
                break

    def push(self, elem):
        self.array.append(elem)
        self.bubble_up(len(self.array) - 1)

    def empty(self):
        return len(self.array) < 1

    def pop(self):
        
        if self.empty():
            raise IndexError("Can't pop an empty heap")

        res = self.array[0]
        
        ln = len(self.array)
        i = 0
        lpos = 2*i + 1
        rpos = 2*i + 2

        while lpos < ln:

            # if rpos >= ln or self.compare(self.array[lpos],
            #                               self.array[rpos]) < 0:
            if rpos >= ln or self.array[lpos] < self.array[rpos]:
                # Go down the left branch
                self.array[i] = self.array[lpos]
                i = lpos

            else:
                # Go down the right branch
                self.array[i] = self.array[rpos]
                i = rpos

            # Reset the left and right child positions
            lpos = 2*i + 1
            rpos = 2*i + 2
            
        # We've reached the bottom of the tree. This means we have an
        # extra element in the tree, so we need to remove it while
        # maintaining the heap properties.

        # Move the last element to the ith position, since it now
        # holds a copy of the parent
        self.array[i] = self.array[ln - 1]
        # Reset the heap property
        self.bubble_up(i)
        # Pop the array to get rid of the extra element
        self.array.pop()

        return res

    @classmethod
    def heapsort(cls, array, comp_func=None):
        
        heap = BinaryHeap(comp_func=comp_func)

        for elem in array:
            heap.push(elem)

        i = 0
        ln = len(array)

        while i < ln:
            array[i] = heap.pop()
            i += 1

        return array
