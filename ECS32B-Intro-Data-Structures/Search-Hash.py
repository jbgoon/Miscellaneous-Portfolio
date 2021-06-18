# Jack Goon
# ECS 32B A06
# SID 914628387
#
# Homework Assignment 4

# Problem 1

def ternarySearch(alist,item):

    first = 0
    last = len(alist) - 1
    found = False

    while first < last and not found:

        mid1 = first + (first+last)//3
        mid2 = last - (first+last)//3

        if item == alist[mid1]:
            found = True
        elif item == alist[mid2]:
            found = True
        else:
            if item < alist[mid1]:
                last = mid1
            elif item > alist[mid2]:
                first = mid2
            else:
                first = mid1
                last = mid2
    return found

print(ternarySearch([1,2,3,5,6,7,8],4))

# Problem 2

def ternarySearchRec(alist,item):

    first = 0
    last = len(alist) - 1
    mid1 = int((last+first)/3)
    mid2 = int(2*(last+first)/3)

    if item == alist[mid1]:
        return True

    if item == alist[mid2]:
        return True

    if len(alist) <= 1:
        return False

    else:
        if item < alist[mid1]:
            return ternarySearchRec(alist[:mid1],item)
        elif item > alist[mid2]:
            return ternarySearchRec(alist[mid2+1:],item)
        else:
            return ternarySearchRec(alist[mid1:mid2],item)

# Problem 3

# Class from the textbook, with added list of prime numbers in __init__
class HashTable:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.primeList = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,
                          127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,
                          251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                          389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,
                          541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,
                          677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,
                          839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,
                          1009]

    def hashfunction(self, key, size):
        return key % size

    def rehash(self, oldhash, size):
        return (oldhash + 1) % size

# Put method is altered to use "upSize," which I've written below
    def putNew(self, key, data):
        hashvalue = self.hashfunction(key, len(self.slots))

        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data  # replace
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))

                count = 0
                while (self.slots[nextslot] != None) and (self.slots[nextslot] != key):
                    count += 1
                    nextslot = self.rehash(nextslot, len(self.slots))
                    if count == self.size: # If you have gone through all slots, and none are available...
                        self.upSize()
                        print(count)
                        count = 0 # increase the size of the table and continue looping.

                if self.slots[nextslot] == None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data  # replace

# Helper method for upSize method
    def findPrime(self,startSize):
        for i in self.primeList: # parse through prime numbers
            if i < 2*startSize:
                continue
            return i # return the first number greater than twice the startSize

# Helper method for putNew method
    def upSize(self):
        startSize = self.size
        self.size = self.findPrime(startSize) # adjust self.size method for new size
        newSlots = self.size - startSize # total increase in size
        self.slots = self.slots + newSlots*[None] # append new slots
        self.data = self.data + newSlots*[None] # append new data slots






