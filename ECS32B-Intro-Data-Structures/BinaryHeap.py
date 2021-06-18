# Jack Goon
# 914628387
# ECS 32B A06 Jackson
# Homework Assignment 6

# PROBLEM 1
# Using the buildHeap method, write a sorting function that can sort a list in O(nlogn) time.

# The following code is from the book. I use any applicable methods, as suggested in the homework assignment pdf
# where the professor says "Use the code given in the textbook as your foundation"
class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def percUp(self,i):
        while i // 2 > 0:
          if self.heapList[i] < self.heapList[i // 2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
          i = i//2


    def insert(self,k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self,alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while (i > 0):
            self.percDown(i)
            i = i - 1

# Function that combines methods from heap class to sort any given list (alist)
def heapSort(alist):

    # STEP 1 - Heapify
    x = BinHeap()
    x.buildHeap(alist)

    # STEP 2 - Sort
    while x.currentSize > 0:

        x.heapList[1], x.heapList[x.currentSize] = x.heapList[x.currentSize],x.heapList[1] # Swap first and last items

        x.currentSize -= 1 # reduce size of heap

        x.percUp(x.currentSize) # bring up any smaller items from bottom, if applicable

        x.percDown(1) # bring down any large items from top, if applicable

    return x.heapList[1:] # return heap, exclude the 0 added for convenience


# PROBLEM 2

# 2a
    # FORMAT:
    # City processed [queue, adding all adjacent to city processed]
    # Presented in order, top to bottom

    # [Frankfurt]
    # Frankfurt [Mannheim Wurzburg Kassel]
    # Mannheim [Wurzburg Kassel Karlsruhe]
    # Wurzburg [Kassel Karlsruhe Erfurt Nurnberg]
    # Kassel [Karlsruhe Erfurt Nurnberg Munchen]
    # Karlsruhe [Erfurt Nurnberg Munchen Augsburg]
    # Erfurt [Nurnberg Munchen Augsburg]
    # Nurnberg [Munchen Augsburg Stuttgart]
    # Munchen [Augsburg Stuttgart]
    # Augsburg [Stuttgart]
    # Stuttgart

    # Order: Frankfurt, Mannheim, Wurzburg, Kassel, Karlsruhe, Erfurt, Nurnberg, Munchen, Augsburg Stuttgart

# 2b

    # [Frankfurt]
    # Frankfurt [Mannheim, Wurzburg, Kassel]
    # Mannheim [Wurzburg, Kassel, Karlsruhe]
    # Wurzburg [Kassel, Karlsruhe, Nurnberg, Erfurt]
    # Kassel [Karlsruhe, Nurnberg, Erfurt, Munchen]
    # Karlsruhe [Nurnberg, Erfurt, Munchen, Augsburg]
    # Nurnberg [Erfurt, Munchen, Augsburg, Stuttgart]
    # Erfurt [Munchen, Augsburg, Stuttgart]
    # Munchen [Augsburg, Stuttgart]
    # Augsburg [Stuttgart]
    # Stuttgart

    # Order: Frankfurt, mannheim, Wurzburg, Kassel, Karsruhe, Nurnberg, Erfurt, Munchen, Augsburg, Stuttgart

# 2c - Using leftmost edge

    # City processed [stack, adding all adjacent to city processed]
    # Frankfurt [Mannheim, wurzburg, kassel]
    # Mannheim [Karsruhe wurzburg kassel]
    # Karlsruhe [Augsburg wurzburg kassel]
    # Augsburg [ Munchen Wurzburg kassel ]
    # Munchen [ Nurnberg Kassel Wurzburg kassel]
    # Nurnberg [Wurzburg Stuttgart Kassel Wurzburg kassel]
    # Wurzberg [Erfurt Stuttgart Kassel Wurzburg kassel]
    # Erfurt [Stuttgart Kassel Wurzburg kassel]
    # Stuttgart [Kassel Wurzburg kassel]
    # Kassel

    # Order: Frankfurt Mannheim Karlsruhe Augsburg Munchen Nurnberg Wurzberg Erfurt Stuttgart kassel


# 2d - Using the same process as in 2c

    # Order: Frankfurt Mannheim Karlsruhe Augsburg Wurzburg Nurnberg Stuttgart Erfurt Kassel Munchen
