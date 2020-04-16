# Jack Goon
# ECS 32B A06
#
# Homework 2

# QUESTION 1 - Chapter 3 Exercise 5
# Rather than use python insert method, I decided to use front and rear pointers and indexing
# since indexing is O(1)

class QueueX():
# initialize python list, front and rear pointers
    def __init__(self):
        self.itemList = [] # list to store items
        self.front = 0 # pointer to front of queue
        self.rear = 0 # pointer to back of queue
# method to add item to rear of queue
    def enqueue(self,item):
        self.itemList.append(item)
        self.rear += 1
# method to remove item from front of queue, return item. If no dequeue-ing is possible, return None.
    def dequeue(self):
        if self.isEmpty(): # do not dequeue if the queue is empty
            dequeueItem = None # method will return None if dequeue-ing is not possible
        else:
            dequeueItem = self.itemList[self.front]
            self.front += 1 # move front pointer forward to account for item being removed
        return dequeueItem # one return statement at the end, for simplicity
# method returns True if empty, else False
    def isEmpty(self):
        return (self.size() == 0)
# method returns length of queue
    def size(self):
        return self.rear - self.front # size of queue is the difference between the two pointers
# test code
"""
sample = QueueX()
print("empty:", sample.isEmpty())
print("enqueue-ing: A")
sample.enqueue('A')
print("enqueue-ing: B")
sample.enqueue('B')
print("enqueue-ing: C")
sample.enqueue('C')
print("empty:", sample.isEmpty())
print("length:", sample.size())
print("dequeue-ing:", sample.dequeue())
print("length:", sample.size())
print("dequeue-ing:", sample.dequeue())
print("length:", sample.size())
print("dequeue-ing:", sample.dequeue())
print("length:", sample.size())
print("dequeue-ing:", sample.dequeue())
print("empty:", sample.isEmpty())
print("length:", sample.size())
"""

# QUESTION 2 - Chapter 3 Exercise 19
# Note - indexing done in the same way Python List's are indexed (starting at 0)

# NODE CLASS FROM TEXTBOOK, ADDED FOR REFERENCE
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

class UnorderedList():

    # __INIT__ METHOD FROM TEXTBOOK, ADDED FOR REFERENCE
    def __init__(self):
            self.head = None

    # SLICE CLASS - READ THIS FOR ACTUAL HOMEWORK ANSWER
    def slice(self, start, stop):
        index = -1
        sliceList = []  # List to store sliced items
        temp = self.head  # temp variable stores each item from list temporarily
        # Move through list to get to start position
        while index < start:
            temp = temp.getNext()  # moves through list
            index += 1  # keeps track of how many items have been moved through
        # Continue to move through list until you reach the stop position, adding each item into list
        while index < stop:  # all items in this loop are to be added to list
            sliceList.append(temp.getData())  # use getData() to access each item, add to sliceList
            temp = temp.getNext()  # move onto the next item
            index += 1
        # Return list containing sliced items
        return sliceList

    # ALL FOLLOWING UNORDERED LIST METHODS ARE FROM TEXTBOOK - ADDED FOR REFERENCE / TESTING
    def add(self, item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp
    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()
        return count
    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found
    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
    def isEmpty(self):
        return self.head == None

# test code
"""
sample2 = UnorderedList()
sample2.add('A')
print("adding A")
sample2.add('B')
print("adding B")
sample2.add('C')
print("adding C")
sample2.add('D')
print("adding D")
sample2.add('E')
print("adding E")
print("slice 1:3 -")
print(sample2.slice(1,3))
"""

# QUESTION 3 - Chapter 3 Exercise 22 - Linked List Stack

class LLStack():
# __init__ creates unordered list
    def __init__(self):
        self.items = UnorderedList() # creates UnorderedList object for stack
# add an item to the front of the unordered list
    def push(self,item):
        self.items.add(item) # use add method from UnorderedList class
# return the first item from the list, then redirect the head to the second item to exclude the first item
    def pop(self):
        popNode = self.items.head
        popData = popNode.getData() # stores the item that will be popped
        nextNode = popNode.getNext()
        self.items.head = nextNode # modifies stack, head now points towards the temp node
        return popData
# return the first item from the list
    def peek(self):
        return self.items.head.getData() # returns first item using getData method from UnorderedList class
# if empty, True; else, False
    def isEmpty(self):
        return self.items.isEmpty() # use isEmpty method from UnorderedList class
# return size of list
    def size(self):
        return self.items.size() # use size method from UnorderedList class
# test code
"""
sample3 = LLStack()
print('empty:',sample3.isEmpty())
print('size:',sample3.size())
print('push A')
sample3.push('A')
print('push B')
sample3.push('B')
print('push C')
sample3.push('C')
print('push D')
sample3.push('D')
print('empty:',sample3.isEmpty())
print('size:',sample3.size())
print('peeking:',sample3.peek())
print('popping:',sample3.pop())
print('peeking:',sample3.peek())
print('popping:',sample3.pop())
print('peeking:',sample3.peek())
print('empty:',sample3.isEmpty())
print('size:',sample3.size())
"""

# QUESTION 4 - Chapter 3 Exercise 23 - Linked List Queue
# My implementation enqueue's items to the front, dequeue's items from back

class LLQueue:

    def __init__(self):
        self.items = UnorderedList()
    def enqueue(self,item):
        self.items.add(item)

    def dequeue(self):
        temp = self.items.head # temp variable stores nodes as we loop through list
        size = self.items.size()
        if size == 0: # If there are no items in queue, return None
            returnItem = None
        elif size == 1: # If there is just one item, return that item.
            self.items.head = None
            returnItem =temp.getData()
        else: # for 2+ items, go to second to last item, and move from there.
            for i in range(size-2): # at the end of this loop, temp is the second to last item in list
                temp = temp.getNext()
            secondToLastNode = temp
            lastNode = secondToLastNode.getNext() # variable holds the last node
            secondToLastNode.setNext(None) # second to last node now points to None
            returnItem = lastNode.getData() # return data from last node
        return returnItem
        # When all is done, the secondToLastNode is now the last node of list.

    def isEmpty(self):
        return self.items.isEmpty() # use method from UnorderedList class

    def size(self):
        return self.items.size() # use method from Unordered List class
'''
sample4 = LLQueue()
print("empty:", sample4.isEmpty())
print("enqueue-ing: A")
sample4.enqueue('A')
print("enqueue-ing: B")
sample4.enqueue('B')
print("enqueue-ing: C")
sample4.enqueue('C')
print("empty:", sample4.isEmpty())
print("length:", sample4.size())
print("dequeue-ing:", sample4.dequeue())
print("length:", sample4.size())
print("dequeue-ing:", sample4.dequeue())
print("length:", sample4.size())
print("dequeue-ing:", sample4.dequeue())
print("length:", sample4.size())
'''


# QUESTION 5 - Chapter 3 Exercise 24 - Linked List Deque

class LLDeque():

    def __init__(self):
        self.items = UnorderedList()

    def addFront(self,item):
        self.items.add(item) # Use UnorderedList add method

    def addRear(self,item):
        size = self.items.size()
        temp = self.items.head
        for i in range(size-1):
            temp = temp.getNext()
        newNode = Node()
        newNode.setData(item)
        temp.setNext(newNode)

    def removeFront(self): # return head item. Redirect head to the second item.
        returnItem = self.items.head.getData()
        secondItem = self.items.head.getNext()
        self.items.head = secondItem
        return returnItem

    def removeRear(self): # Similar code to LLQueue dequeue method
        temp = self.items.head # temp variable stores nodes as we loop through list
        size = self.items.size()
        if size == 0:
            returnItem = None
        elif size == 1:
            self.items.head = None
            returnItem =temp.getData()
        else:
            for i in range(size-2): # at the end of this loop, temp is the second to last item in list
                temp = temp.getNext()
            secondToLastNode = temp
            lastNode = secondToLastNode.getNext() # variable holds the last node
            secondToLastNode.setNext(None) # second to last node now points to None
            returnItem = lastNode.getData() # return data from last node
        return returnItem
        # When all is done, the secondToLastNode is now the last node of list.

    def isEmpty(self):
        return self.items.isEmpty() # use method from UnorderedList class

    def size(self):
        return self.items.size() # use method from Unordered List class

#  QUESTION 6 - Chapter 3 Exercise 27 Adapted - Deque with doubly linked list

class Deque2():

    def __init__(self):
        self.items = DoublyLinkedList() # I am using an imaginary class called DoublyLinkedList

    def addFront(self,item):
        self.items.add(item)

    def addRear(self,item):
        lastItem = self.items.head.getLast()
        lastItem.setNext(item)

    def removeFront(self):
        returnItem = self.items.head.getData()
        secondItem = self.items.head.getNext()
        self.items.head = secondItem
        return returnItem

    def removeRear(self):
        lastItem = self.items.head.last() # "last" is the method for node "head" to link the last item of the list
        returnLastItem = lastItem.getData()
        secondToLastItem = lastItem.getBack() # "getBack" method returns the previous item in list
        secondToLastItem.setNext(None) # Last item of the list points to None
        self.items.head.setLast(secondToLastItem) # "setLast" method sets the "last" pointer from head to last list item
        return returnLastItem()

    def isEmpty(self):
        return self.items.isEmpty() # use method from UnorderedList class

    def size(self):
        return self.items.size() # use method from Unordered List class