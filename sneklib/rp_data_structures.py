#Author: Rémi Pelletier
#File:   rp_data_structures.py
#Desc.:  A module containing my implementation of various data structures.


#TODO: Allow duplicate values in ArrayBST (should fix tree_sort in rp_sorting.py).
#TODO: Finish LinkedList (review __iter__() and next() + other stuff).
#TODO: PROPER TESTS

#----------------------------------Array BST-----------------------------------

#Binary search tree implemented using a zero-indexed dynamic array (list).
class ArrayBST:
    DEFAULT_SIZE = 10 #Default initial size of the underlying array.
    DEFAULT_GROWTH_RATE = 2 #Default rate at which the underlying array's size increases when resized.

    def __init__(self, initial_size = DEFAULT_SIZE, growth_rate = DEFAULT_GROWTH_RATE):
        self._cur_size = 0
        self._max_size = max(initial_size, 0)
        self._growth_rate = growth_rate if growth_rate > 1 else self.DEFAULT_GROWTH_RATE
        self._entries = [None for i in range(self._max_size)]


    #Returns the index of the parent of the
    #given node in the underlying array.
    def _get_parent(self, index):
        return (index - 1) // 2

    #Returns the index at which the left child of the
    #given node should be found in the underlying array.
    def _get_left_child(self, root):
        return root * 2 + 1

    #Returns the index at which the right child of the
    #given node should be found in the underlying array.
    def _get_right_child(self, root):
        return root * 2 + 2

    #Returns a boolean indicating whether or
    #not the given node has a left child.
    def _has_left_child(self, root):
        left_child_index = self._get_left_child(root)
        return left_child_index < self._cur_size and self._entries[left_child_index] != None

    #Returns a boolean indicating whether or
    #not the given node has a right child.
    def _has_right_child(self, root):
        right_child_index = self._get_right_child(root)
        return right_child_index < self._cur_size and self._entries[right_child_index] != None

    #Returns the leftmost element under the given root.
    def _get_leftmost(self, root):
        pos = root
        while self._has_left_child(pos):
            pos = self._get_left_child(pos)
        return pos

    #Returns the rightmost element under the given root.
    def _get_rightmost(self, root):
        pos = root
        while self._has_right_child(pos):
            pos = self._get_right_child(pos)
        return pos

    #Returns the index of the given value in the
    #underlying array or None if it is not present.
    def _get_index(self, val):
        pos = 0
        while pos < self._max_size and self._entries[pos] != None and self._entries[pos] != val:
            pos = self._get_left_child(pos) if val < self._entries[pos] else self._get_right_child(pos)
        return None if pos >= self._max_size or self._entries[pos] is None else pos

    #Enlarges the underlying array according to the set growth rate.
    def _enlarge(self):
        new_size = self._max_size * self._growth_rate + 1
        delta =  new_size - self._cur_size #+1 is to insure the size doesn't get stuck at 0.
        self._entries.extend([None for i in range(delta)])
        self._max_size = new_size

    #Recursive function used to build a sorted array from the tree.
    def _get_sorted_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            self._get_sorted_array(self._get_left_child(root), array)
            array.append(self._entries[root])
            self._get_sorted_array(self._get_right_child(root), array)

    #Recursive function used to build a reversly sorted array from the tree.
    def _get_reverse_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            self._get_reverse_array(self._get_right_child(root), array)
            array.append(self._entries[root])
            self._get_reverse_array(self._get_left_child(root), array)

    #Recursive function used to build an array where the elements'
    #order corresponds to the pre-order traversal of the tree.
    def _get_preorder_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            array.append(self._entries[root])
            self._get_preorder_array(self._get_left_child(root), array)
            self._get_preorder_array(self._get_right_child(root), array)

    #Recursive function used to build an array where the elements'
    #order corresponds to the post-order traversal of the tree.
    def _get_postorder_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:    
            self._get_postorder_array(self._get_left_child(root), array)
            self._get_postorder_array(self._get_right_child(root), array)
            array.append(self._entries[root])


    #Returns the number of elements in the tree.
    def size(self):
        return self._cur_size

    #Returns a boolean indicating if the tree is empty.
    def empty(self):
        return self.size() == 0

    #Returns a boolean indicating whether or not
    #the specified value is present in the tree.
    def contains(self, val):
        return self._get_index(val) != None

    #Inserts the given value into the tree.
    def insert(self, val):
        if self._cur_size == self._max_size:
            self._enlarge()

        pos = 0
        while pos < self._max_size and self._entries[pos] != None:
            if self._entries[pos] == val:
                return #No duplicates
            pos = self._get_left_child(pos) if val < self._entries[pos] else  self._get_right_child(pos)

        if pos >= self._max_size:
            self._enlarge()

        self._entries[pos] = val
        self._cur_size += 1

    #Inserts every element of the given array into the tree.
    def insert_array(self, array):
        for a in array:
            self.insert(a)

    #Removes the specified value from the tree if it is present.
    def remove(self, val):
        index = self._get_index(val)
        if index != None:
            if not self._has_left_child(index) and not self._has_right_child(index):
                self._entries[index] = None
            elif self._has_left_child(index) and not self._has_right_child(index):
                left_child_index = self._get_left_child(index)
                self._entries[index] = self._entries[left_child_index]
                self._entries[left_child_index] = None
            elif self._has_right_child(index) and not self._has_left_child(index):
                right_child_index = self._get_right_child(index)
                self._entries[index] = self._entries[right_child_index]
                self._entries[right_child_index] = None
            else:
                new_root_index = self._get_leftmost(self._get_right_child(index))
                self._entries[index] = self._entries[new_root_index]
                self._entries[new_root_index] = None
            self._cur_size -= 1

    #Returns the maximum value in the tree.
    def get_max(self):
        return self._entries[self._get_rightmost(0)] if not self.empty() else None

    #Returns the minimum value in the tree.
    def get_min(self):
        return self._entries[self._get_leftmost(0)] if not self.empty() else None

    #Returns a sorted array containing all the elements in the tree.
    def get_sorted_array(self):
        array = []
        self._get_sorted_array(0, array)
        return array

    #Returns a reversly sorted array containing all the elements in the tree.
    def get_reverse_array(self, array):
        array = []
        self._get_reverse_array(0)
        return array

    #Returns an array where the elements' order
    #corresponds to the pre-order traversal of the tree.
    def get_preorder_array(self, array):
        array = []
        self._get_preorder_array(0)
        return array

    #Returns an array where the elements' order
    #corresponds to the post-order traversal of the tree.
    def get_postorder_array(self, array):
        array = []
        self._get_postorder_array(0)
        return array



#---------------------------------Binary heap----------------------------------

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
        self._cur_size = 0
        self._max_size = max(initial_size + 1, 1)
        self._growth_rate = growth_rate if growth_rate > 1 else self.DEFAULT_GROWTH_RATE
        self._entries = [None for i in range(self._max_size)]

    #Resizes the underlying array according to the set growth rate.
    def _enlarge(self):
        new_size = self._max_size * self._growth_rate + 1
        delta =  new_size - self._cur_size #+1 is to insure the size doesn't get stuck at 0.
        self._entries.extend([None for i in range(delta)])
        self._max_size = new_size

    #Percolates an entry down to it's right position.
    def _percolate_down(self, hole):
        tmp = HeapEntry(self._entries[hole].value, self._entries[hole].priority)
        while hole * 2 <= self._cur_size:
            child = hole * 2
            if child != self._cur_size and self._entries[child+1].priority < self._entries[child].priority:
                child += 1
            if self._entries[child].priority < tmp.priority:
                self._entries[hole] = self._entries[child]
            else:
                break
            hole = child
        self._entries[hole] = tmp

    #Percolates an entry up to it's right position.
    def _percolate_up(self, hole, entry):
        while hole > 1 and entry.priority < self._entries[hole//2].priority:
            self._entries[hole] = HeapEntry(self._entries[hole//2].value, self._entries[hole//2].priority)
            hole //= 2
        self._entries[hole] = entry

    #Returns the number of entries in the heap.
    def size(self):
        return self._cur_size

    #Returns a boolean indicating if the heap is empty.
    def empty(self):
        return self.size() == 0

    #Returns the value at the top of the heap without removing it.
    def peek(self):
        if self.empty():
            return None
        return entries[1].value

    #Returns the value at the top of the heap and removes it.
    def pop(self):
        if self.empty():
            return None
        val = self._entries[1].value
        self._entries[1] = self._entries[self._cur_size]
        self._cur_size -= 1
        self._percolate_down(1)
        return val

    #Inserts an new entry in the heap (the value is considered as being the priority as well).
    def insert(self, value):
        self.insert_pair(value, value)

    #Inserts an new entry in the heap.
    def insert_pair(self, value, priority):
        if self._cur_size == self._max_size-1:
            self._enlarge()
        hole = self._cur_size + 1
        self._cur_size += 1
        new_entry = HeapEntry(value, priority)
        self._percolate_up(hole, new_entry)

    #Inserts every element of the array in the heap (the value is considered as being the priority as well).
    def insert_array(self, array):
        for e in array:
            self.insert(e)

    #Inserts every element of the array, given as (value, priority) tuples/lists, in the heap.
    def insert_pair_array(self, array):
        for e in array:
            self.insert_pair(e[0], e[1])



#----------------------------------Hash map------------------------------------

class HashMap:
    DEFAULT_INITIAL_SIZE = 10

    def __init__(self, initial_size = DEFAULT_INITIAL_SIZE): 
        self._max_size = max(initial_size, 0)
        self._cur_size = 0
        self._array = [None for _ in range(self._max_size)]

    def _enlarge(self):
        pass



#-----------------------------Doubly linked list-------------------------------

#Class used to represent an entry in the doubly linked list.
class ListNode:
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = prev
        self.next = next


#Doubly linked list data structure.
class LinkedList:
    def __init__(self):
        self._front = None
        self._back = None
        self._current = None
        self._size = 0

    #Returns the value of the element at the
    #given index or None if the list is empty.
    def __getitem__(self, index):
        return self.at(index)

    def __iter__(self):
        self._current = self._front
        return self

    #Returns the number of elements present in the list.
    def __len__(self):
        return self.size()

    def __next__(self):
        if self._current is None:
            raise StopIteration
        val = self._current.value
        self._current = self._current.next
        return val
      
    #Builds and returns the string representing the list.      
    def __str__(self):
        result = '['
        cur_node = self._front
        if self._front is not None:
            result += str(self._front.value)
            cur_node = self._front.next
        while cur_node is not None:
            result += ', ' + str(cur_node.value)
            cur_node = cur_node.next
        result += ']'
        return result

    #Returns the node at the given index or None if the list is empty.
    def _get_node(self, index):
        if self.empty():
            return None
        index %= self.size() #Python-style indexing.
        if self.size() - index < index:
            cur_node = self._back
            i = self.size() - 1
            while i > index:
                cur_node = cur_node.prev
                i -= 1
        else:
            cur_node = self._front
            i = 0
            while i < index: 
                cur_node = cur_node.next
                i += 1
        return cur_node

    #Removes the given node from the list.
    def _remove_node(self, node):
        if node is not None:
            if node == self._front:
                self.pop_front()
            elif node == self._back:
                self.pop_back()
            else:
                if node.prev is not None:
                    node.prev.next = node.next
                if node.next is not None:
                    node.next.prev = node.prev
                self._size -= 1

    #Returns the value of the node at the given
    #index or None if the list is empty. 
    def at(self, index):
        print('at : ' + str(index)) #Debug
        if self.empty():
            return None
        return self._get_node(index).value

    #Returns the value of the last entry
    #in the list or None if the list is empty.
    def back(self):
        return None if self._back is None else self._back.value

    #Removes every entry in the list.
    def clear(self):
        self._front = None
        self._back = None
        self._current = None
        self._size = 0

    #Returns a boolean indicating whether or
    #not the given value is present in the list.
    def contains(self, value):
        print('contains : ' + str(value)) #Debug
        return self.find(value) is not None

    #Returns a boolean indicating if the list is empty.
    def empty(self):
        return self.size() == 0   

    #Finds and returns the index of the given
    #value in the list or None if it is not found.
    def find(self, value):
        print('find : ' + str(value)) #Debug
        if self.empty():
            return None
        i = 0
        cur_node = self._front
        while cur_node is not None and cur_node.value != value:
            cur_node = cur_node.next
            i += 1
        return None if cur_node is None else i

    #Returns the value of the first entry
    #in the list or None if the list is empty.
    def front(self):
        return None if self._front is None else self._front.value

    #Inserts the given element in the list at the specified index.
    def insert(self, value, index):
        print('insert : ' + str(value) + ' , ' + str(index)) #Debug
        if self.empty():
            self.push_front(value)
            return

        index %= self.size() #Python-style indexing.

        if index == 0:
            self.push_front(value)
            return

        cur_node = self._get_node(index)      
        prev_node = cur_node.prev  
        new_node = ListNode(value, prev_node, cur_node)
        prev_node.next = new_node
        cur_node.prev = new_node
        self._size += 1
    
    #Removes the last entry in the list but does not return it.
    def pop_back(self):
        print('pop_back') #Debug
        if not self.empty():
            if self._current == self._back:
                self._current = None
            self._back = self._back.prev
            if self._back is not None:
                self._back.next = None
            self._size -= 1

    #Removes the first entry in the list but does not return it.
    def pop_front(self):
        print('pop_front') #Debug
        if not self.empty():
            if self._current == self._front:
                self._current = self._front.next
            self._front = self._front.next   
            if self._front is not None:  
                self._front.prev = None 
            self._size -= 1

    #Appends the given element at the end of the list.
    def push_back(self, value):
        print('push_back : ' + str(value)) #Debug
        new_node = ListNode(value, prev=self._back)
        if self.empty():
            self._front = new_node
            self._current = new_node
        else:
            self._back.next = new_node
        self._back = new_node
        self._size += 1

    #Appends the given element at the start of the list.
    def push_front(self, value):
        print('push_front : ' + str(value)) #Debug
        new_node = ListNode(value, next=self._front)
        if self.empty():    
            self._back = new_node
            self._current = new_node
        else:
            self._front.prev = new_node
        self._front = new_node
        self._size += 1

    #Removes the element at the given index if the list is not empty.
    def remove_at(self, index):
        print('remove_at : ' + str(index)) #Debug
        self._remove_node(self._get_node(index))
            
    #Removes the given element from the list if it is present.
    #By default, only the first occurence of the element is removed,
    #but "n" occurences can removed be setting the parameter "count" to "n".
    #All the occurences of the given element can also be removed at once
    #by setting the parameter "all" to True.
    def remove(self, value, count=1, all=False):
        print('remove : ' + str(value) + '  count : ' + str(count) + '  all : ' + str(all)) #Debug
        if not self.empty():
            found_count = 0
            cur_node = self._front
            while cur_node is not None and (all or found_count < count):
                if cur_node.value != value:
                    cur_node = cur_node.next
                else:
                    found_count += 1
                    if self._current == cur_node:
                        self._current = cur_node.prev
                    self._remove_node(cur_node)                  
             
    #Returns the number of elements present in the list.
    def size(self):
        return self._size



#------------------------------------Queue-------------------------------------

#Queue implemented using a linked list.
class Queue:
    def __init__(self):
        self._lst = LinkedList()

    #Return the number of elements present in the queue.
    def __len__(self):
        return self.size()

    #Returns a string representing the queue.
    def __str__(self):
        return str(self._lst)
         
    #Returns a boolean indicating if the queue is empty.
    def empty(self):
        return self._lst.empty()

    #Returns the value of the element at the
    #front of the queue or None if it is empty.
    def front(self):
        return self._lst.front()

    #Removes the element at the front of 
    #the queue but doesn't return it.
    def pop(self):
        self._lst.pop_front()

    #Appends the given element at the back of the queue.
    def push(self, value):
        self._lst.push_back(value)

    #Returns the number of elements present in the queue.
    def size(self):
        return self._lst.size()



#------------------------------------Stack-------------------------------------

#Stack implemented using a linked list.
class Stack:
    def __init__(self):
        self._lst = LinkedList()

    #Return the number of elements present in the stack.
    def __len__(self):
        return self.size()

    #Returns a string representing the stack.
    def __str__(self):
        return str(self._lst)

    #Returns sa boolean indicating if the stack is empty.
    def empty(self):
        return self._lst.empty()

    #Returns the value of the element at the
    #top of the stack or None if it is empty.
    def peek(self):
        return self._lst.front()

    #Removes the element at the top
    #of stack but doesn't return it.
    def pop(self):
        self._lst.pop_front()

    #Pushes the given element on the top of the stack.
    def push(self, value):
        self._lst.push_front(value)

    #Returns the number of elements present in the stack.
    def size(self):
        return self._lst.size()



#--------------------------------Min-Max Stack---------------------------------

#Class used to represent a node in a min-max stack.
class MinMaxNode:
    def __init__(self, value, next = None, min_so_far = None, max_so_far = None):
        self.value = value
        self.next = next
        self.min_so_far = min_so_far
        self.max_so_far = max_so_far


#Stack data structure which can also return the minimum and the maximum value.
#Push: O(1)   Pop: O(1)   Peek: O(1)   Min: O(1)   Max: O(1)
class MinMaxStack:
    def __init__(self):
        self._top = None
        self._min_node = None
        self._max_node = None
        self._size = 0

    #Returns sa boolean indicating if the stack is empty.
    def empty(self):
        return self._size == 0

    #Returns the maximum value in the
    #stack or None if it is empty.
    def max(self):
        return None if self.empty() else self._max_node.value

    #Returns the minimum value in the
    #stack or None if it is empty.
    def min(self):
       return None if self.empty() else self._min_node.value

    #Returns the value of the element at the
    #top of the stack or None if it is empty.
    def peek(self):
        return None if self.empty() else self._top.value

    #Removes the element at the top
    #of stack but doesn't return it.
    def pop(self):
        if not self.empty():
            if self._top == self._max_node:
                self._max_node = self._max_node.max_so_far
            if self._top == self._min_node:
                self._min_node = self._min_node.min_so_far
            self._top = self._top.next
            self._size -= 1

    #Pushes the given element on the top of the stack.
    def push(self, value):
        new_node = MinMaxNode(value)
        if self.empty():
            self._top = new_node
            self._min_node = new_node
            self._max_node = new_node
        else:
            new_node.min_so_far = self._min_node
            new_node.max_so_far = self._max_node
            new_node.next = self._top
            self._top = new_node
            if value <= self._min_node.value:
                self._min_node = new_node
            if value >= self._max_node.value:
                self._max_node = new_node
        self._size += 1

    #Returns the number of elements present in the stack.
    def size(self):
        return self._size



#--------------------------------Min-Max Queue---------------------------------

#Queue data structure which can return the minimum and 
#the maximum value implemented using two Min-Max stacks.
#Push: O(1)   Pop: O(1)   Front: O(1)   Min: O(1)   Max: O(1)
class MinMaxQueue:
    def __init__(self):
        self._push_stack = MinMaxStack()
        self._pop_stack = MinMaxStack()

    #Returns a boolean indicating if the queue is empty.
    def empty(self):
        return self._push_stack.empty() and self._pop_stack.empty()

    #Returns the value of the element at the
    #front of the queue or None if it is empty.
    def front(self):
        if self.empty():
            return None
        if self._pop_stack.empty():
            self._transfer_push_stack()
        return self._pop_stack.peek()

    #Returns the maximum value in the
    #queue or None if it is empty.
    def max(self):
        if self._pop_stack.empty():
            return self._push_stack.max()
        elif self._push_stack.empty():
            return self._pop_stack.max()
        else:
            return max(self._pop_stack.max(), self._push_stack.max())

    #Returns the minimum value in the
    #queue or None if it is empty.
    def min(self):
        if self._pop_stack.empty():
            return self._push_stack.min()
        elif self._push_stack.empty():
            return self._pop_stack.min()
        else:
            return min(self._pop_stack.min(), self._push_stack.min())

    #Removes the element at the front of 
    #the queue but doesn't return it.
    def pop(self):
        if not self.empty():    
            if self._pop_stack.empty():
                self._transfer_push_stack()
            self._pop_stack.pop()
          
    #Appends the given element at the back of the queue.      
    def push(self, value):
        self._push_stack.push(value)

    #Returns the number of elements present in the queue.
    def size(self):
        return self._push_stack.size() + self._pop_stack.size()

    def _transfer_push_stack(self):
        if not self.empty():
            while not self._push_stack.empty():
                self._pop_stack.push(self._push_stack.peek())
                self._push_stack.pop()

                


#---------------------------------Suffix tree----------------------------------

class SuffixTree:
    def __init__(self, string):
        self.string = string



#------------------------------------Trie--------------------------------------

#Class used to represent a trie's node.
class TrieNode:
    def __init__(self, char, ends_word = False, is_root = False):
        self.char = char
        self.ends_word = ends_word
        self.is_root = is_root
        self.children = dict()

    #Appends the given string under the node (as children).
    def add(self, string):
        if string is None or len(string) == 0:
            return
        if not string[0] in self.children:
            self.children[string[0]] = TrieNode(string[0])       
        if len(string) == 1:
            self.children[string[0]].ends_word = True
        else:
            self.children[string[0]].add(string[1:])

    #Returns a boolean indicating if the given string
    #is a prefix of any of the children of the node.
    def is_prefix(self, string):
        if string is None or len(string) == 0:
            return False
        if not string[0] in self.children:
            return False
        if len(string) == 1:
            return True       
        return self.children[string[0]].is_prefix(string[1:])

    #Returns a boolean indicating if the given string has previously
    #been added to the node (each character must be a sub-node and
    #the last character must be a node which ends a word). 
    def contains(self, string):
        if string is None or len(string) == 0:
            return False
        if not string[0] in self.children:
            return False
        if len(string) == 1:
            return self.children[string[0]].ends_word
        return self.children[string[0]].contains(string[1:])


#Trie data structure.
class Trie:
    def __init__(self):
        self.root = TrieNode(None, is_root = True)

    #Adds the given string in the trie.
    def add(self, string):
        self.root.add(string)

    #Returns a boolean indicating if the given string
    #is contained (has previously been added) in the trie.
    def contains(self, string):
        return self.root.contains(string)

    #Returns a boolena indicating if the given string
    #is a prefix of any previously added string.
    def is_prefix(self, string):
        return self.root.is_prefix(string)
        



#Test
#lst = [1, 4, 5, 0, 4, -2, 10, 5, 20, -13, 0]
#min_max_stack = MinMaxStack()
#min_max_queue = MinMaxQueue()

#print('-----Insert Test-----')
#for val in lst:
#    min_max_stack.push(val)
#    min_max_queue.push(val)
#    print(val)
#    print('Stack:  top:   {0}  min: {1}  max: {2}'.format(min_max_stack.peek(), min_max_stack.min(), min_max_stack.max()))
#    print('Queue:  front: {0}  min: {1}  max: {2}'.format(min_max_queue.front(), min_max_queue.min(), min_max_queue.max()))

#print('\n-----Stack Pop Test-----')
#while not min_max_stack.empty():
#    print(min_max_stack.peek())
#    print('Stack:  top:   {0}  min: {1}  max: {2}'.format(min_max_stack.peek(), min_max_stack.min(), min_max_stack.max()))
#    min_max_stack.pop()

#print('\n-----Queue Pop Test-----')
#while not min_max_queue.empty():
#    print(min_max_queue.front())
#    print('Queue:  front: {0}  min: {1}  max: {2}'.format(min_max_queue.front(), min_max_queue.min(), min_max_queue.max()))
#    min_max_queue.pop()



#lst = ["Bonjour", "Hello", "Hi", "Hey", "Bonne"]
#test = ["Bon", "Ha", "Hell", "Bonjour!", "Hey", "Bye", "k", "", None]
#trie = Trie()
#for string in lst:
#    trie.add(string)
#for string in test:
#    contains = trie.contains(string)
#    prefix = trie.is_prefix(string)
#    print(str(string) + ' :\tContains: ' + str(contains) + '\tPrefix: ' + str(prefix))



#array = [3,34,6,8,2,3,1,9,67]

#bst = ArrayBST()
#bst.insertArray(array)
#print(bst.getSortedArray())

#heap = BinaryHeap()
#heap.insertArray(array)
#while not heap.isEmpty():
#    print(heap.pop())

#lst = LinkedList()
#print(str(lst) + ' ' + str(lst.size()))

#lst.push_back(5)
#print(str(lst) + ' ' + str(lst.size()))

#lst.push_back('Hello')
#print(str(lst) + ' ' + str(lst.size()))

#lst.push_front(None)
#print(str(lst) + ' ' + str(lst.size()))

#front = lst.front()
#back = lst.back()
#print('Front: ' + str(front))
#print('Back: ' + str(back))

#lst.pop_back()
#print(str(lst) + ' ' + str(lst.size()))

#lst.pop_front()
#print(str(lst) + ' ' + str(lst.size()))

#lst.pop_front()
#print(str(lst) + ' ' + str(lst.size()))

#lst.pop_front()
#print(str(lst) + ' ' + str(lst.size()))

#lst.pop_back()
#print(str(lst) + ' ' + str(lst.size()))

#lst.insert('Wat', 0)
#print(str(lst) + ' ' + str(lst.size()))

#lst.insert('Lel', 0)
#print(str(lst) + ' ' + str(lst.size()))

#lst.insert('Kek', 1)
#print(str(lst) + ' ' + str(lst.size()))

#print(lst.contains('Lel'))
#print(lst.find('Lel'))

#print(lst.contains('Wut'))
#print(lst.find('Wut'))

#print(lst.at(0))
#print(lst[0])

#print(lst.at(1))
#print(lst[1])

#print(lst.at(2))
#print(lst[2])

#print(lst.at(-1))
#print(lst[-1])

#lst.remove('Wut')
#print(str(lst) + ' ' + str(lst.size()))

#lst.remove('Kek')
#print(str(lst) + ' ' + str(lst.size()))

#lst.insert('Wut', -1)
#print(str(lst) + ' ' + str(lst.size()))

#lst.remove_at(0)
#print(str(lst) + ' ' + str(lst.size()))

#lst.remove_at(-1)
#print(str(lst) + ' ' + str(lst.size()))

#lst.remove_at(-1)
#print(str(lst) + ' ' + str(lst.size()))

#lst.remove_at(0)
#print(str(lst) + ' ' + str(lst.size()))

#test_lst = [1, None, 'hello', 'boss', (1,2), [], 5]
#for val in test_lst:
#    lst.push_back(val)

#print(str(lst) + ' ' + str(lst.size()))

#for val in lst:
#    print(val)

#for val in lst:
#    print(val)

#print(len(lst))


#stack = Stack()
#print(stack)
#print(len(stack))
#print(str(stack) + ' ' + str(stack.size()))
#stack.push(10)
#print(str(stack) + ' ' + str(stack.size()))
#stack.push('Hello')
#print(str(stack) + ' ' + str(stack.size()))
#stack.push(None)
#print(str(stack) + ' ' + str(stack.size()))
#print(stack.peek())
#stack.pop()
#print(str(stack) + ' ' + str(stack.size()))
#print(stack.peek())
#stack.pop()
#print(str(stack) + ' ' + str(stack.size()))
#print(stack.peek())
#stack.pop()
#print(str(stack) + ' ' + str(stack.size()))
#print(stack.peek())
#stack.pop()
#print(str(stack) + ' ' + str(stack.size()))
#print(stack.peek())


#queue = Queue()
#print(queue)
#print(len(queue))
#print(str(queue) + ' ' + str(queue.size()))
#queue.push(10)
#print(str(queue) + ' ' + str(queue.size()))
#queue.push('Hello')
#print(str(queue) + ' ' + str(queue.size()))
#queue.push(None)
#print(str(queue) + ' ' + str(queue.size()))
#print(queue.front())
#queue.pop()
#print(str(queue) + ' ' + str(queue.size()))
#print(queue.front())
#queue.pop()
#print(str(queue) + ' ' + str(queue.size()))
#print(queue.front())
#queue.pop()
#print(str(queue) + ' ' + str(queue.size()))
#print(queue.front())
#queue.pop()
#print(str(queue) + ' ' + str(queue.size()))
#print(queue.front())









