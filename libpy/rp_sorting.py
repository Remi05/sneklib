#Author: Rémi Pelletier
#File:   rp_sorting.py
#Desc.:  Module containing various sorting functions.


import random


#Create a list (vector) of the given size and fills it with random numbers between min_val and max_val (both inclusive).
def createRandomVector(size, min_val, max_val):
    vector = [0]*size
    for i in range(0, size):
        vector[i] = random.randrange(min_val, max_val+1, 1)
    return vector


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


#Sorts the elements in a list (vector) using Comb sort, can sort in reverse order as well.
def combSort(vector, reverse = False):
    v_length = len(vector)
    shrink_factor = 1.3
    gap = v_length
    swapped = True

    while gap != 1 or swapped:
        gap /= shrink_factor
        gap  = 1 if gap < 1 else int(gap)
        swapped = False
        i = 0
        while (i + gap) < v_length:
            if (vector[i] > vector[i+gap] and not reverse) or\
               (vector[i] < vector[i+gap] and reverse):
                swap(vector, i, i + gap)
                swapped = True
            i += 1


#Sorts the elements in a list (vector) using Cocktail sort, can sort in reverse order as well.
def cocktailSort(vector, reverse = False):  
    left_end  = 0
    right_end = len(vector) - 1
    swapped   = True

    while swapped:
        for i in range(left_end, right_end):
            if (vector[i] > vector[i+1] and not reverse) or\
               (vector[i] < vector[i+1] and reverse):
                swap(vector, i, i+1)
                swapped = True
            else:
                swapped = False
        right_end -= 1

        for j in range(right_end, left_end, -1):
            if (vector[j] < vector[j-1] and not reverse) or\
               (vector[j] > vector[j-1] and reverse):
                swap(vector, j, j-1)
                swapped = True
        left_end += 1


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


#Sorts the elements in a list (vector) using Gnome sort, can sort in reverse order as well.
def gnomeSort(vector, reverse = False):
    i = 1
    while i < len(vector):
        if i == 0 or ((vector[i-1] <= vector[i] and not reverse) or\
                      (vector[i-1] >= vector[i] and reverse)):
            i += 1
        else:
            swap(vector, i-1, i)
            i -= 1


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


#Recursive function used to sort sections of a vector (used by mergeSort()).
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



#Partitions a list (vector) using the Lomuto partition scheme (used for Quicksort and Quickselect).
def _partition(vector, left, right):
    pivotIndex = right #Note: We can change how we choose the pivot.
    pivot = vector[pivotIndex] 
    swap(vector, pivotIndex, right)
    i = left
    for j in range(left, right):
        if vector[j] <= pivot:
            swap(vector, i, j)
            i += 1
    swap(vector, i, right)
    return i


#Recursive function used to find the element that would be at index k if the list was to be sorted (used by quickselect()).
def _quickselect(vector, left, right, k):
     if left == right:
         return vector[left]
     pivotIndex = _partition(vector, left, right)
     if k == pivotIndex:
         return vector[k]
     elif k < pivotIndex:
         return _quickselect(vector, left, pivotIndex-1, k)
     else:
         return _quickselect(vector, pivotIndex+1, right, k)


#Finds the element that would be at index k if the list (vector) was to be
#sorted (without necessarily sorting the list) using Quickselect.
def quickselect(vector, k):
    return _quickselect(vector, 0, len(vector)-1, k)


#Recursive function used to sort sections of a list (used by quicksort()).
def _quicksort(vector, left, right):
    if left < right:
        pivot = _partition(vector, left, right)
        _quicksort(vector, left, pivot-1)
        _quicksort(vector, pivot+1, right)


#Sorts the elements in a list (vector) using Quicksort (standard implementation).
def quicksort(vector):
    _quicksort(vector, 0, len(vector)-1)



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



#Test
vector = createRandomVector(15, 1, 100)
print(vector)
cocktailSort(vector)
print(vector)
