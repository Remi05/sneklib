#Author: Rémi Pelletier
#File:   rp_sorting.py
#Desc.:  Module containing various sorting functions.


#TODO: Consider returning a new list instead of modifying the list passed as an argument.


#Swaps two elements in a list (vector).
def swap(vector, i1, i2):
    tmp = vector[i1]
    vector[i1] = vector[i2]
    vector[i2] = tmp


#Sorts the elements in a list (vector) using Selection sort, can sort in reverse order as well.
def selectionSort(vector, reverse = False):
    for i in range(0, len(vector)-1):
        min = i
        for j in range(i+1, len(vector)):
            if (vector[j] < vector[min] and not reverse) or\
               (vector[j] > vector[min] and reverse):
                min = j
        swap(vector, i, min)


#Sorts the elements in a list (vector) using Bubble sort, can sort in reverse order as well.
def bubbleSort(vector, reverse = False):
    for i in range(0, len(vector)-1):
        for j in range(len(vector)-1, i, -1):
            if (vector[j] < vector[j-1] and not reverse) or\
               (vector[j] > vector[j-1] and reverse):
                swap(vector, j, j-1)


#Sorts the elements in a list (vector) using Insertion sort, can sort in reverse order as well.
def insertionSort(vector, reverse = False):
    for i in range(1, len(vector)):
        tmp = vector[i]
        j = i
        while j > 0 and ((tmp < vector[j-1] and not reverse) or\
                         (tmp > vector[j-1] and reverse)):
            vector[j] = vector[j-1]
            j -= 1
        vector[j] = tmp


#Merges the vector to be sorted and the temporary vector in the specified range (used for sorting using mergeSort()).
def _merge(vector, tmp, left, right, right_end):
    left_end = right - 1
    tmpPos = left
    nb_elements = right_end - left + 1

    while left <= left_end and right <= right_end:
        if vector[left] <= vector[right]:
            tmp[tmpPos] = vector[left]
            tmpPos += 1
            left += 1
        else:
            tmp[tmpPos] = vector[right]
            tmpPos += 1
            right += 1

    while left <= left_end:
        tmp[tmpPos] = vector[left]
        tmpPos += 1
        left += 1

    while right <= right_end:
        tmp[tmpPos] = vector[right]
        tmpPos += 1
        right += 1

    for i in range(0, nb_elements):
        vector[right_end] = tmp[right_end]
        right_end -= 1


#Recursive function used to sort sections of a vector (used for sorting using mergeSort()).
def _mergeSort(vector, tmp, left, right):
    if right > left:
        center = (left + right) // 2
        _mergeSort(vector, tmp, left, center)
        _mergeSort(vector, tmp, center + 1, right)
        _merge(vector, tmp, left, center + 1, right)


#Sorts the elements in a list (vector) using Merge sort.
def mergeSort(vector):
    tmp = [0]*len(vector)
    _mergeSort(vector, tmp, 0, len(vector)-1)
    
    
#Sorts the elements in a list (vector) using Counting sort (use only when the
#range of values is significantly smaller than the number of values).
def countingSort(vector):
    min_val = min(vector)
    max_val = max(vector)
    size = max_val - min_val + 1
    counts = [0]*size

    for i in range(0, len(vector)):
        counts[vector[i]-min_val] += 1

    cur_pos = 0
    for j in range(0, size):
        for k in range(0, counts[j]):
            vector[cur_pos] = j + min_val
            cur_pos += 1


#Sorts the elements, given as (key, val) tuples, in a list (vector) using Counting sort (use only when the
#range of values is significantly smaller than the number of values).
def countingSortWithValues(vector):
    min_val = min(e[0] for e in vector)
    max_val = max(e[0] for e in vector)
    size = max_val - min_val + 1
    indexed_vals = [[] for i in range(0, size)]

    for i in range(0, len(vector)):
        indexed_vals[vector[i][0]-min_val].append(vector[i][1])

    cur_pos = 0
    for j in range(0, size):
        for k in range(0, len(indexed_vals[j])):
            vector[cur_pos] = (j + min_val, indexed_vals[j][k])
            cur_pos += 1


#Returns a list containing the value of each (key,value) tuple in the vector
#(useful when using countingSortWithValues() to keep only the values after sorting).
def stripKeys(vector):
    return [tup[1] for tup in vector]
