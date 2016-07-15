#Author: Rémi Pelletier
#File:   rp_data_structures.py
#Desc.:  A module containing my implementation of various data structures.


#Binary search tree implemented using a zero-indexed dynamic array (list).
class ArrayBST:
    DEFAULT_SIZE = 10 #Default initial size of the underlying array.
    DEFAULT_GROWTH_RATE = 2 #Default rate at which the underlying array's size increases when resized.

    def __init__(self, initial_size = DEFAULT_SIZE, growth_rate = DEFAULT_GROWTH_RATE):
        self.__cur_size = 0
        self.__max_size = max(initial_size, 0)
        self.__growth_rate = growth_rate if growth_rate > 1 else self.DEFAULT_GROWTH_RATE
        self.__entries = [None for i in range(self.__max_size)]


    def __getParent(self, index):
        return (index - 1) // 2

    def __getLeftChild(self, root):
        return root * 2 + 1

    def __getRightChild(self, root):
        return root * 2 + 2

    def __hasLeftChild(self, root):
        left_child_index = self.__getLeftChild(root)
        return left_child_index < self.__cur_size and self.__entries[left_child_index] != None

    def __hasRightChild(self, root):
        right_child_index = self.__getRightChild(root)
        return right_child_index < self.__cur_size and self.__entries[right_child_index] != None

    def __getLeftMost(self, root):
        pos = root
        while self.__hasLeftChild(pos):
            pos = self.__getLeftChild(pos)
        return pos

    def __getRightMost(self, root):
        pos = root
        while self.__hasRightChild(pos):
            pos = self.__getRightChild(pos)
        return pos

    def __getIndex(self, val):
        pos = 0
        while pos < self.__max_size and self.__entries[pos] != None and self.__entries[pos] != val:
            pos = self.__getLeftChild(pos) if val < self.__entries[pos] else self.__getRightChild(pos)
        return None if pos >= self.__max_size or self.__entries[pos] == None else pos

    def __enlarge(self):
        new_size = self.__max_size * self.__growth_rate + 1
        delta =  new_size - self.__cur_size #+1 is to insure the size doesn't get stuck at 0.
        self.__entries.extend([None for i in range(delta)])
        self.__max_size = new_size

    def __getSortedArray(self, root, array):
        if self.__cur_size > 0 and root < self.__max_size and self.__entries[root] != None:
            self.__getSortedArray(self.__getLeftChild(root), array)
            array.append(self.__entries[root])
            self.__getSortedArray(self.__getRightChild(root), array)

    def __getReverseArray(self, root, array):
        if self.__cur_size > 0 and root < self.__max_size and self.__entries[root] != None:
            self.__getReverseArray(self.__getRightChild(root), array)
            array.append(self.__entries[root])
            self.__getReverseArray(self.__getLeftChild(root), array)

    def __getPreOrderArray(self, root, array):
        if self.__cur_size > 0 and root < self.__max_size and self.__entries[root] != None:
            array.append(self.__entries[root])
            self.__getPreOrderArray(self.__getLeftChild(root), array)
            self.__getPreOrderArray(self.__getRightChild(root), array)

    def __getPostOrderArray(self, root, array):
        if self.__cur_size > 0 and root < self.__max_size and self.__entries[root] != None:    
            self.__getPostOrderArray(self.__getLeftChild(root), array)
            self.__getPostOrderArray(self.__getRightChild(root), array)
            array.append(self.__entries[root])


    def size(self):
        return self.__cur_size

    def isEmpty(self):
        return self.size() == 0

    def contains(self, val):
        return self.__getIndex(val) != None

    def insert(self, val):
        if self.__cur_size == self.__max_size:
            self.__enlarge()

        pos = 0
        while pos < self.__max_size and self.__entries[pos] != None:
            if self.__entries[pos] == val:
                return #No duplicates
            pos = self.__getLeftChild(pos) if val < self.__entries[pos] else  self.__getRightChild(pos)

        if pos >= self.__max_size:
            self.__enlarge()

        self.__entries[pos] = val
        self.__cur_size += 1

    def insertArray(self, array):
        for a in array:
            self.insert(a)

    def remove(self, val):
        index = self.__getIndex(val)
        if index != None:
            if not self.__hasLeftChild(index) and not self.__hasRightChild(index):
                self.__entries[index] = None
            elif self.__hasLeftChild(index) and not self.__hasRightChild(index):
                left_child_index = self.__getLeftChild(index)
                self.__entries[index] = self.__entries[left_child_index]
                self.__entries[left_child_index] = None
            elif self.__hasRightChild(index) and not self.__hasLeftChild(index):
                right_child_index = self.__getRightChild(index)
                self.__entries[index] = self.__entries[right_child_index]
                self.__entries[right_child_index] = None
            else:
                new_root_index = self.__getLeftMost(self.__getRightChild(index))
                self.__entries[index] = self.__entries[new_root_index]
                self.__entries[new_root_index] = None
            self.__cur_size -= 1

    def getMax(self):
        return self.__entries[self.__getRightMost(0)] if not self.isEmpty() else None

    def getMin(self):
        return self.__entries[self.__getLeftMost(0)] if not self.isEmpty() else None

    def getSortedArray(self):
        array = []
        self.__getSortedArray(0, array)
        return array

    def getReverseArray(self, array):
        array = []
        self.__getReverseArray(0)
        return array

    def getPreOrderArray(self, array):
        array = []
        self.__getPreOrderArray(0)
        return array

    def getPostOrderArray(self, array):
        array = []
        self.__getPostOrderArray(0)
        return array



#Class used to represent an entry in the binary heap.
class HeapEntry:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority


#Binary heap implemeneted using a dynamic array (list).
class BinaryHeap:
    DEFAULT_SIZE = 10 #Default initial size of the underlying array.
    DEFAULT_GROWTH_RATE = 2 #Default rate at which the underlying array's size increases when resized.

    def __init__(self, initial_size = DEFAULT_SIZE, growth_rate = DEFAULT_GROWTH_RATE):
        self.__cur_size = 0
        self.__max_size = max(initial_size + 1, 1)
        self.__growth_rate = growth_rate if growth_rate > 1 else self.DEFAULT_GROWTH_RATE
        self.__entries = [None for i in range(self.__max_size)]


    #Resizes the underlying array according to the set growth rate.
    def __enlarge(self):
        new_size = self.__max_size * self.__growth_rate + 1
        delta =  new_size - self.__cur_size #+1 is to insure the size doesn't get stuck at 0.
        self.__entries.extend([None for i in range(delta)])
        self.__max_size = new_size

    #Percolates an entry down to it's right position.
    def __percolateDown(self, hole):
        tmp = HeapEntry(self.__entries[hole].value, self.__entries[hole].priority)
        while hole * 2 <= self.__cur_size:
            child = hole * 2
            if child != self.__cur_size and self.__entries[child+1].priority < self.__entries[child].priority:
                child += 1
            if self.__entries[child].priority < tmp.priority:
                self.__entries[hole] = self.__entries[child]
            else:
                break
            hole = child
        self.__entries[hole] = tmp

    #Percolates an entry up to it's right position.
    def __percolateUp(self, hole, entry):
        while hole > 1 and entry.priority < self.__entries[hole//2].priority:
            self.__entries[hole] = HeapEntry(self.__entries[hole//2].value, self.__entries[hole//2].priority)
            hole //= 2
        self.__entries[hole] = entry

    #Returns the number of entries in the heap.
    def size(self):
        return self.__cur_size

    #Returns a boolean indicating if the heap is empty.
    def isEmpty(self):
        return self.size() == 0

    #Returns the value at the top of the heap without removing it.
    def peek(self):
        if self.isEmpty():
            return None
        return entries[1].value

    #Returns the value at the top of the heap and removes it.
    def pop(self):
        if self.isEmpty():
            return None
        val = self.__entries[1].value
        self.__entries[1] = self.__entries[self.__cur_size]
        self.__cur_size -= 1
        self.__percolateDown(1)
        return val

    #Inserts an new entry in the heap (the value is considered as being the priority as well).
    def insert(self, value):
        self.insertPair(value, value)

    #Inserts an new entry in the heap.
    def insertPair(self, value, priority):
        if self.__cur_size == self.__max_size:
            self.__enlarge()
        hole = self.__cur_size + 1
        self.__cur_size += 1
        new_entry = HeapEntry(value, priority)
        self.__percolateUp(hole, new_entry)

    #Inserts every element of the array in the heap (the value is considered as being the priority as well).
    def insertArray(self, array):
        for e in array:
            self.insert(e)

    #Inserts every element of the array, given as (value, priority) tuples/lists, in the heap.
    def insertPairArray(self, array):
        for e in array:
            self.insertPair(e[0], e[1])




#Test
array = [3,34,6,8,2,3,1,9,67]

#bst = ArrayBST()
#bst.insertArray(array)
#print(bst.getSortedArray())

heap = BinaryHeap()
heap.insertArray(array)
while not heap.isEmpty():
    print(heap.pop())