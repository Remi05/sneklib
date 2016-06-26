
#Binary search tree implemented using a zero-indexed dynamic array (list).
class ArrayBST:
    #Attributes
    __elements = []
    __cur_size = 0
    __cur_max_size = 0


    #Constructor
    def __init__(self, size = 0):
        if size > 0:
            self.__elements = [None] * size
            self.__cur_max_size = size


    #"Private" methods
    def __getParent(self, index):
        return (index - 1) // 2

    def __getLeftChild(self, root):
        return root * 2 + 1

    def __getRightChild(self, root):
        return root * 2 + 2


    def __hasLeftChild(self, root):
        left_child_index = self.__getLeftChild(root)
        return left_child_index < self.__cur_size and self.__elements[left_child_index] != None

    def __hasRightChild(self, root):
        right_child_index = self.__getRightChild(root)
        return right_child_index < self.__cur_size and self.__elements[right_child_index] != None


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
        while pos < self.__cur_max_size and self.__elements[pos] != None and self.__elements[pos] != val:
            pos = self.__getLeftChild(pos) if val < self.__elements[pos] else self.__getRightChild(pos)
        return None if pos >= self.__cur_max_size or self.__elements[pos] == None else pos


    def __enlarge(self, new_size):
        if new_size > self.__cur_max_size:
            self.__elements.extend([None] * (new_size - self.__cur_max_size))
            self.__cur_max_size = new_size


    def __printInOrder(self, root):
        if self.__cur_size > 0 and root < self.__cur_max_size and self.__elements[root] != None:
            self.__printInOrder(self.__getLeftChild(root))
            print(self.__elements[root])
            self.__printInOrder(self.__getRightChild(root))

    def __printReverseOrder(self, root):
        if self.__cur_size > 0 and root < self.__cur_max_size and self.__elements[root] != None:
            self.__printReverseOrder(self.__getRightChild(root))
            print(self.__elements[root])
            self.__printReverseOrder(self.__getLeftChild(root))

    def __printPreOrder(self, root):
        if self.__cur_size > 0 and root < self.__cur_max_size and self.__elements[root] != None:
            print(self.__elements[root])
            self.__printPreOrder(self.__getLeftChild(root))
            self.__printPreOrder(self.__getRightChild(root))

    def __printPostOrder(self, root):
        if self.__cur_size > 0 and root < self.__cur_max_size and self.__elements[root] != None:    
            self.__printPostOrder(self.__getLeftChild(root))
            self.__printPostOrder(self.__getRightChild(root))
            print(self.__elements[root])


    #Public methods
    def size(self):
        return self.__cur_size

    def isEmpty(self):
        return self.size() == 0

    def contains(self, val):
        return self.__getIndex(val) != None


    def insert(self, val):
        if self.__cur_size == self.__cur_max_size:
            self.__enlarge(2 * self.__cur_max_size + 1)

        pos = 0
        while pos < self.__cur_max_size and self.__elements[pos] != None:
            if self.__elements[pos] == val:
                return #No duplicates
            pos = self.__getLeftChild(pos) if val < self.__elements[pos] else  self.__getRightChild(pos)

        if pos >= self.__cur_max_size:
            self.__enlarge(2 * self.__cur_max_size + 1)

        self.__elements[pos] = val
        self.__cur_size += 1


    def remove(self, val):
        index = self.__getIndex(val)
        if index != None:
            if not self.__hasLeftChild(index) and not self.__hasRightChild(index):
                self.__elements[index] = None
            elif self.__hasLeftChild(index) and not self.__hasRightChild(index):
                left_child_index = self.__getLeftChild(index)
                self.__elements[index] = self.__elements[left_child_index]
                self.__elements[left_child_index] = None
            elif self.__hasRightChild(index) and not self.__hasLeftChild(index):
                right_child_index = self.__getRightChild(index)
                self.__elements[index] = self.__elements[right_child_index]
                self.__elements[right_child_index] = None
            else:
                new_root_index = self.__getLeftMost(self.__getRightChild(index))
                self.__elements[index] = self.__elements[new_root_index]
                self.__elements[new_root_index] = None
            self.__cur_size -= 1


    def getMax(self):
        return self.__elements[self.__getRightMost(0)] if not self.isEmpty() else None

    def getMin(self):
        return self.__elements[self.__getLeftMost(0)] if not self.isEmpty() else None


    def printInOrder(self):
        self.__printInOrder(0)

    def printReverseOrder(self):
        self.__printReverseOrder(0)

    def printPreOrder(self):
        self.__printPreOrder(0)

    def printPostOrder(self):
        self.__printPostOrder(0)



bst = ArrayBST()
array = [3,34,6,8,2,3,1,9,67]
for a in array:
    bst.insert(a)
bst.printInOrder()
print('')