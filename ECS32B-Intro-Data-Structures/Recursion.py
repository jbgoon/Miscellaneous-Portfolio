# Jack Goon
# 914628387
# ECS 32B A06
# TA Jackson
# Homework Assignment 3

# Problem 1 --------------------------------------------------------------------------------------

def kleinfeldt(n):
    if n == 1: # base case
        return 1
    else:
        return 1/(n**2) + kleinfeldt(n-1) # reduction + recursion steps

# Problem 2 --------------------------------------------------------------------------------------

def ladder(n): # n is number of rungs on ladder

    # multiple base cases because recursion step calls function twice.
    if n <= 0: # Not a ladder
        return None
    if n == 1: # If initial n is 1, return 1
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 3

    # this is the pattern for sequence. It took me an hour and multiple pages of binder paper to figure this out. SMH.
    else:
        return ladder(n-1) + ladder(n-2)

# Problem 3 --------------------------------------------------------------------------------------

def findLargest(alist):
    return findLargestAux(alist,0,alist[0])

def findLargestAux(alist,pointer,largest):
    if pointer == len(alist): # BASE CASE: if you've parsed through the entire list...
        return largest # ... return the largest number found
    else:
        if alist[pointer] > largest: # if the object is larger than largest
            return findLargestAux(alist,pointer+1,alist[pointer])
        else: # if the object is smaller than the largest
            return findLargestAux(alist,pointer+1,largest)

# Problem 4 --------------------------------------------------------------------------------------

# Step 1 - This program keeps running. Issue with base case, can't figure out what

def findPossibilities(listA):
    listB = [] # keeps track of potential majority items

    # Base case 1
    if len(listA) <= 2: # If listA has 2 or fewer items, return listA. This could be placed above other code
        return listA

    # if list has odd number of items, add last item to listB
    if len(listA)%2 != 0:
        listB.append( listA[-1] )

    # compare adjacent items, add to list if they are the same
    pointer = 0  # keeps track of which items of list are being compared
    while pointer < ( len(listA) - 1 ):
        if listA[pointer] == listA[pointer + 1]:
            listB.append( listA[pointer] )
        pointer += 2

    # Base case 2
    if len(listB) == 0: # Another base case - if listB has no items, return listA
        return listA

    return findPossibilities(listB) # if listA and listB aren't the final lists, recurse. listB --> listA, new listB

# Step 2 - This program works and is tested

def verifyPossibilities(list, possibilities):
    for possibility in possibilities: # Runs program for the possibilit(ies)
        possibilityCount = 0 # keeps track of how often each possibility occurs in the initial list
        for item in list:
            if item == possibility:
                possibilityCount += 1
        if possibilityCount > len(list)/2: # count of occurances must be greater than half of the list to make majority
            return possibility
    return None # return None if none of the possibilities constitute a majority


# Problem 5 --------------------------------------------------------------------------------------

# Node class from textbook

class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext

# My response to problem

def findValue(value,node):
    if value == node.getData(): # Base case, if item is found then return True
        return True
    elif node.getNext() == None: # Base case, if end of list is reached
        return False
    else: # Recursive step. getNext is incremental step.
        return findValue(value,node.getNext())

# Problem 6 --------------------------------------------------------------------------------------

def findLastValue(node):
    if node.getNext() == None: # Base case -- if last item reached, return data from last item
        return node.getData()
    else:
        return findLastValue(node.getNext()) # Recursive step, getNext is incremental step.








