# Jack Goon
# 914628387
# ECS 32B A06 Jackson
# Homework Assignment 5

### PROBLEM 1 - Pancake sort algorithm

### PART A - For each item to be sorted, two flips occur. The last pancake does not
# need to be flipped, so there are n-1 pancakes sorted. Therefore, T(n) = 2(n-1).

### PART B

# Function to perform pancake flip operation on a list, given a flip-point index (the index is included in the flip)
# Note: Indexing starts at 0
def flip(alist,index):
    temp = [None]*(index+1)
    count = 0
    for item in alist[0:index+1]:
        temp[index - count] = item
        count += 1
    return temp + alist[index+1:]

# Function to determine whether or not the list is in order. Return True if in order.
def inOrder(alist):
    for i in range(len(alist)-1):
        if alist[i] < alist[i+1]:
            continue
        else:
            return False
    return True

# Function to perform actual pancake sort.
def pancakeSort(alist):

    maximum = max(alist)
    maxPos = 0
    count = 0

    if len(alist) == 1:
        return [alist[0]]
    for item in alist: # keeps track of the index of the max item in the list
        if item == maximum:
            maxPos = count
        count += 1

    # For each item to be sorted, two flips happen. One to flip the largest item to the front, and one to the back.
    list = flip(alist,maxPos) # 1 - Flip largest item to the front
    list = flip(list,len(alist)-1) # 2 - Flip entire list, so largest item is at the back

    if inOrder(list): # If list is now sorted, return list
        return list
    else: # If list is still unsorted, continue flipping while ignoring the already-sorted items
        return pancakeSort(list[0:-1]) + [list[-1]]

        # NOTE: While the list is technically "broken up" with the splice method here, it essentially remains intact
        # because the broken-up items are immediately concatenated in the recursive call (in the same order as they were
        # in after the flips). This method is in-line with the prompt to not have "smaller, independent stacks" because
        # they are split only very temporarily and there is only ever one stack.

### Problem 2
# Note: I referenced the book's algorithm when making mine. I  changed the implementation to
# include the simultaneous assignment statement.

def bubbleSort(alist):

    # This loop runs once for each "pass", which sorts one item each time.
    for i in range(0,len(alist) - 1):

        # This loop runs once for each comparison. As each item is sorted, the number of comparisons decreases by 1
        # since more items are progressively sorted.
        # This way you don't sort already-sorted items.
        for j in range((len(alist)-1) -i):
            if alist[j] > alist[j+1]:

                # This is the simultaneous assignment statement, which bypasses a temporary variable.
                alist[j],alist[j+1] = alist[j+1],alist[j]

    return alist # Return the sorted list.



### Problem 3
# Note: Once again, I referenced the book's algorithm when making mine. I changed the implementation to
# exclude the splice operator.

def mergeSort(alist):
    print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2

# This is the part that avoids using the splice operator. As stated in class, the assignment only requires that we
# don't use splice. The professor clearly stated that we could use the append operator.

        # Initialize half lists
        lefthalf = []
        righthalf = []

        # Use for-loop to recreate lefthalf and righthalf without splice operator
        for i in range(mid):
            lefthalf.append(alist[i])
        for j in range(mid,len(alist)):
            righthalf.append(alist[j])

        # The rest of the algorithm is from the textbook
        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    print("Merging ",alist)







