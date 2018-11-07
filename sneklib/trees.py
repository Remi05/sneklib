#Author: Remi Pelletier
#File:   trees.py
#Desc.:  A module containing my implementation of various tree data structures.


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

    def __len__(self):
        return self.size()

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
    def _get_index(self, value):
        pos = 0
        while pos < self._max_size and self._entries[pos] != None and self._entries[pos] != value:
            pos = self._get_left_child(pos) if value < self._entries[pos] else self._get_right_child(pos)
        return None if pos >= self._max_size or self._entries[pos] is None else pos

    #Enlarges the underlying array according to the set growth rate.
    def _enlarge(self):
        new_size = self._max_size * self._growth_rate + 1
        delta =  new_size - self._cur_size #+1 is to insure the size doesn't get stuck at 0.
        self._entries.extend([None for i in range(delta)])
        self._max_size = new_size

    #Returns the number of elements in the tree.
    def size(self):
        return self._cur_size

    #Returns a boolean indicating if the tree is empty.
    def is_empty(self):
        return self.size() == 0

    #Returns a boolean indicating whether or not
    #the specified value is present in the tree.
    def contains(self, value):
        return self._get_index(value) != None

    #Inserts the given value into the tree.
    def insert(self, value):
        if self._cur_size == self._max_size:
            self._enlarge()

        pos = 0
        while pos < self._max_size and self._entries[pos] != None:
            if self._entries[pos] == value:
                return #No duplicates
            pos = self._get_left_child(pos) if value < self._entries[pos] else  self._get_right_child(pos)

        if pos >= self._max_size:
            self._enlarge()

        self._entries[pos] = value
        self._cur_size += 1

    #Inserts every element of the given array into the tree.
    def insert_array(self, array):
        for value in array:
            self.insert(value)

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
    def max(self):
        return self._entries[self._get_rightmost(0)] if not self.is_empty() else None

    #Returns the minimum value in the tree.
    def min(self):
        return self._entries[self._get_leftmost(0)] if not self.is_empty() else None

    #Recursive method used to build an array where the elements'
    #order corresponds to the post-order traversal of the tree.
    def _get_postorder_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:    
            self._get_postorder_array(self._get_left_child(root), array)
            self._get_postorder_array(self._get_right_child(root), array)
            array.append(self._entries[root])

    #Returns an array where the elements' order
    #corresponds to the post-order traversal of the tree.
    def get_postorder_array(self):
        array = []
        self._get_postorder_array(0, array)
        return array

    #Recursive method used to build an array where the elements'
    #order corresponds to the pre-order traversal of the tree.
    def _get_preorder_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            array.append(self._entries[root])
            self._get_preorder_array(self._get_left_child(root), array)
            self._get_preorder_array(self._get_right_child(root), array)

    #Returns an array where the elements' order
    #corresponds to the pre-order traversal of the tree.
    def get_preorder_array(self):
        array = []
        self._get_preorder_array(0, array)
        return array

    #Recursive method used to build a reversly sorted array from the tree.
    def _get_reversed_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            self._get_reversed_array(self._get_right_child(root), array)
            array.append(self._entries[root])
            self._get_reversed_array(self._get_left_child(root), array)

    #Returns a reversly sorted array containing all the elements in the tree.
    def get_reversed_array(self):
        array = []
        self._get_reversed_array(0, array)
        return array
    
    #Recursive method used to build a sorted array from the tree.
    def _get_sorted_array(self, root, array):
        if self._cur_size > 0 and root < self._max_size and self._entries[root] != None:
            self._get_sorted_array(self._get_left_child(root), array)
            array.append(self._entries[root])
            self._get_sorted_array(self._get_right_child(root), array)

    #Returns a sorted array containing all the elements in the tree.
    def get_sorted_array(self):
        array = []
        self._get_sorted_array(0, array)
        return array

    
#---------------------------------Linked BST-----------------------------------

class BinaryTreeNode:
    def __init__(self, value, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child
        self.nb_occurences = 1


#Binary search tree implemented using linked nodes.
class LinkedBST:
    def __init__(self, root=None):
        self.root = root

    def __len__(self):
        return self.count()

    #Recursive method used to check if the 
    #specified value is present in the tree.
    def _contains(self, node, value):
        if node is None:
            return False
        if value < node.value:
            return self._contains(node.left_child, value)
        if value > node.value:
            return self._contains(node.right_child, value)
        return True

    #Returns a boolean indicating whether or not
    #the specified value is present in the tree.
    def contains(self, value):
        return self._contains(self.root, value)

    #Recursive method used to count the number of elements in the tree.
    def _count(self, node):
        return 0 if node is None else 1 + self._count(node.left_child) + self._count(node.right_child)

    #Returns the number of elements in the tree.
    def count(self):
        return self._count(self.root)

    #Recursive method used to insert the given value into the tree.
    def _insert(self, node, value):
        if value < node.value:
            if node.left_child is None:
                node.left_child = BinaryTreeNode(value)
            else:
                self._insert(node.left_child, value)
        elif value > node.value:
            if node.right_child is None:
                node.right_child = BinaryTreeNode(value)
            else:
                self._insert(node.right_child, value)
        else:
            node.nb_occurences += 1

    #Inserts the given value into the tree.
    def insert(self, value):
        if self.root is None:
            self.root = BinaryTreeNode(value)
        else:
            self._insert(self.root, value)

    #Inserts every element of the given array into the tree.
    def insert_array(self, array):
        for value in array:
            self.insert(value)

    #Returns a boolean indicating if the tree is empty.
    def is_empty(self):
        return root is None

    #Returns the rightmost element under the given node.
    def _get_rightmost(self, node):
        if node is None:
            return None
        return self._get_rightmost(node.right_child) if node.right_child is not None else node.value

    #Returns the maximum value in the tree.
    def max(self):
        return self._get_rightmost(root)

    #Returns the leftmost element under the given node.
    def _get_leftmost(self, node):
        if node is None:
            return None
        return self._get_leftmost(node.left_child) if node.left_child is not None else node.value
    
    #Returns the minimum value in the tree.
    def min(self):
        return self._get_leftmost(root)

    #Recursive method used to remove the first occurence
    #of the specified value from the tree if is present.
    def _remove(self, node, value):
        if node is None:
            return
        if value < node.value:
            self._remove(node.left_child, value)
        elif value > node.value:
            self._remove(node.right_child, value)
        else:
            if node.nb_occurences > 1:
                node.nb_occurences -= 1
            else:
                pass #TODO

    #Removes the first occurence of the specified 
    #value from the tree if it is present.
    def remove(self, value):
        self._remove(root, value)

    #Recursive method used to build an array where the elements'
    #order corresponds to the post-order traversal of the tree.
    def _get_postorder_array(self, node, array):
        if node is None:
            return 
        self._get_postorder_array(node.left_child, array)
        self._get_postorder_array(node.right_child, array)
        array.extend([node.value] * node.nb_occurences)

    #Returns an array where the elements' order
    #corresponds to the post-order traversal of the tree.
    def get_postorder_array(self):
        array = []
        self._get_postorder_array(self.root, array)
        return array

    #Recursive method used to build an array where the elements'
    #order corresponds to the pre-order traversal of the tree.
    def _get_preorder_array(self, node, array):
        if node is None:
            return 
        array.extend([node.value] * node.nb_occurences)
        self._get_preorder_array(node.left_child, array)
        self._get_preorder_array(node.right_child, array)

    #Returns an array where the elements' order
    #corresponds to the pre-order traversal of the tree.
    def get_preorder_array(self):
        array = []
        self._get_preorder_array(self.root, array)
        return array

    #Recursive method used to build a reversly sorted array from the tree.
    def _get_reversed_array(self, node, array):
        if node is None:
            return 
        self._get_reversed_array(node.right_child, array)
        array.extend([node.value] * node.nb_occurences)
        self._get_reversed_array(node.left_child, array)

    #Returns a reversly sorted array containing all the elements in the tree.
    def get_reversed_array(self):
        array = []
        self._get_reversed_array(self.root, array)
        return array

    #Recursive method used to build a sorted array from the tree.
    def _get_sorted_array(self, node, array):
        if node is None:
            return 
        self._get_sorted_array(node.left_child, array)
        array.extend([node.value] * node.nb_occurences)
        self._get_sorted_array(node.right_child, array)

    #Returns a sorted array containing all the elements in the tree.
    def get_sorted_array(self):
        array = []
        self._get_sorted_array(self.root, array)
        return array



#------------------------------------Trie--------------------------------------

#Class used to represent a trie node.
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

    #Returns the length of the longest common prefix of
    #the given string and the strings under the current node.
    def longest_prefix_length(self, string):
        if string is None or len(string) == 0 or not string[0] in self.children:
            return 0
        if len(string) == 1:
            return 1
        return self.children[string[0]].longest_prefix_length(string[1:]) + 1


#Trie data structure.
class Trie:
    def __init__(self):
        self._root = TrieNode(None, is_root = True)

    #Adds the given string in the trie.
    def add(self, string):
        self._root.add(string)

    #Returns a boolean indicating if the given string
    #is contained (has previously been added) in the trie.
    def contains(self, string):
        return self._root.contains(string)

    #Returns a boolean indicating if the given string
    #is a prefix of any previously added string.
    def is_prefix(self, string):
        return self._root.is_prefix(string)

    #Returns the longest common prefix between the given string
    #and any of the strings contained in the trie.
    def longest_common_prefix(self, string):
        return string[:self.longest_prefix_length(string)]

    #Returns the length of the longest common prefix between the
    #given string and any of the strings contained in the trie.
    def longest_prefix_length(self, string):
        return self._root.longest_prefix_length(string)