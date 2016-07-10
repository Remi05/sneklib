#Author: Rémi Pelletier
#File:   rp_sorting.py
#Desc.:  Module containing various sorting functions.


import random


#Creates a list of the given size and fills it with random numbers between min_val and max_val (both inclusive).
def createRandomList(size, min_val, max_val):
    lst = [0]*size
    for i in range(0, size):
        lst[i] = random.randrange(min_val, max_val+1, 1)
    return lst


#Swaps two elements in a list .
def swap(lst, i1, i2):
    lst[i1], lst[i2] = lst[i2], lst[i1]


#Sorts the elements in a list using Selection sort, can sort in reverse order as well.
def selectionSort(lst, reverse = False):
    for i in range(0, len(lst)-1):
        min = i
        for j in range(i+1, len(lst)):
            if (not reverse and lst[j] < lst[min]) or\
               (    reverse and lst[j] > lst[min]):
                min = j
        swap(lst, i, min)


#Sorts the elements in a list using Bubble sort, can sort in reverse order as well.
def bubbleSort(lst, reverse = False):
    v_length = len(lst)
    for i in range(0, v_length-1):
        for j in range(v_length-1, i, -1):
            if (not reverse and lst[j] < lst[j-1]) or\
               (    reverse and lst[j] > lst[j-1]):
                swap(lst, j, j-1)


#Sorts the elements in a list using an improved version of Bubble sort, can sort in reverse order as well.
def improvedBubbleSort(lst, reverse = False):
    end = len(lst)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, end):
            if (not reverse and lst[i] < lst[i-1]) or\
               (    reverse and lst[i] > lst[i-1]):
                swap(lst, i, i-1)
                swapped = True
        end -= 1


#Function used in oddEvenSort() to perform either an odd-even or an even-odd iteration.
#Prevents code duplication and conditional statement evaluation at each iteration.
def _oddEvenIter(lst, start, end, reverse = False):
    swapped = False
    for i in range(start, end, 2):
        if (not reverse and lst[i] < lst[i-1]) or\
           (    reverse and lst[i] > lst[i-1]):
            swap(lst, i, i-1)
            swapped = True  
    return swapped


#Sorts the elements in a list using Odd-even sort, can sort in reverse order as well.
def oddEvenSort(lst, reverse = False):
    length = len(lst)
    swapped = True
    while swapped:
        swapped  = _oddEvenIter(lst, 1, length, reverse) #Odd-even iteration
        swapped |= _oddEvenIter(lst, 2, length, reverse) #Even-odd iteration


#Sorts the elements in a list using Comb sort, can sort in reverse order as well.
def combSort(lst, reverse = False):
    v_length = len(lst)
    shrink_factor = 1.3
    gap = v_length
    swapped = True

    while gap != 1 or swapped:
        gap /= shrink_factor
        gap  = 1 if gap < 1 else int(gap)
        swapped = False
        i = 0
        while (i + gap) < v_length:
            if (not reverse and lst[i] > lst[i+gap]) or\
               (    reverse and lst[i] < lst[i+gap]):
                swap(lst, i, i + gap)
                swapped = True
            i += 1


#Sorts the elements in a list using Cocktail sort, can sort in reverse order as well.
def cocktailSort(lst, reverse = False):  
    left_end  = 0
    right_end = len(lst) - 1
    swapped   = True

    while swapped:
        for i in range(left_end, right_end):
            if (not reverse and lst[i] > lst[i+1]) or\
               (    reverse and lst[i] < lst[i+1]):
                swap(lst, i, i+1)
                swapped = True
            else:
                swapped = False
        right_end -= 1

        for j in range(right_end, left_end, -1):
            if (not reverse and lst[j] < lst[j-1]) or\
               (    reverse and lst[j] > lst[j-1]):
                swap(lst, j, j-1)
                swapped = True
        left_end += 1


#Sorts the elements in a list using Insertion sort, can sort in reverse order as well.
def insertionSort(lst, reverse = False):
    for i in range(1, len(lst)):
        tmp = lst[i]
        j = i
        while j > 0 and ((not reverse and tmp < lst[j-1]) or\
                         (    reverse and tmp > lst[j-1])):
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = tmp


#Sorts the elements in a list using Gnome sort, can sort in reverse order as well.
def gnomeSort(lst, reverse = False):
    v_length = len(lst)
    i = 1
    while i < v_length:
        if i == 0 or ((not reverse and lst[i-1] <= lst[i]) or\
                      (    reverse and lst[i-1] >= lst[i])):
            i += 1
        else:
            swap(lst, i-1, i)
            i -= 1


#Merges the list to be sorted and the temporary list in the specified range (used for sorting using mergeSort()).
def _merge(lst, tmp, left, right, right_end):
    left_end = right - 1
    tmpPos = left
    nb_elements = right_end - left + 1

    while left <= left_end and right <= right_end:
        if lst[left] <= lst[right]:
            tmp[tmpPos] = lst[left]
            tmpPos += 1
            left += 1
        else:
            tmp[tmpPos] = lst[right]
            tmpPos += 1
            right += 1

    while left <= left_end:
        tmp[tmpPos] = lst[left]
        tmpPos += 1
        left += 1

    while right <= right_end:
        tmp[tmpPos] = lst[right]
        tmpPos += 1
        right += 1

    for i in range(0, nb_elements):
        lst[right_end] = tmp[right_end]
        right_end -= 1


#Recursive function used to sort sections of a list (used by mergeSort()).
def _mergeSort(lst, tmp, left, right):
    if right > left:
        center = (left + right) // 2
        _mergeSort(lst, tmp, left, center)
        _mergeSort(lst, tmp, center + 1, right)
        _merge(lst, tmp, left, center + 1, right)


#Sorts the elements in a list using Merge sort.
def mergeSort(lst):
    tmp = [0]*len(lst)
    _mergeSort(lst, tmp, 0, len(lst)-1)



#Partitions a list using the Lomuto partition scheme (used for Quicksort and Quickselect).
def _partition(lst, left, right):
    pivotIndex = right #Note: We can change how we choose the pivot.
    pivot = lst[pivotIndex] 
    swap(lst, pivotIndex, right)
    i = left
    for j in range(left, right):
        if lst[j] <= pivot:
            swap(lst, i, j)
            i += 1
    swap(lst, i, right)
    return i


#Recursive function used to find the element that would be at index k if the list was to be sorted (used by quickselect()).
def _quickselect(lst, left, right, k):
     if left == right:
         return lst[left]
     pivotIndex = _partition(lst, left, right)
     if k == pivotIndex:
         return lst[k]
     elif k < pivotIndex:
         return _quickselect(lst, left, pivotIndex-1, k)
     else:
         return _quickselect(lst, pivotIndex+1, right, k)


#Finds the element that would be at index k if the list was to be
#sorted (without necessarily sorting the list) using Quickselect.
def quickselect(lst, k):
    return _quickselect(lst, 0, len(lst)-1, k)


#Recursive function used to sort sections of a list (used by quicksort()).
def _quicksort(lst, left, right):
    if left < right:
        pivot = _partition(lst, left, right)
        _quicksort(lst, left, pivot-1)
        _quicksort(lst, pivot+1, right)


#Sorts the elements in a list using Quicksort (standard implementation).
def quicksort(lst):
    _quicksort(lst, 0, len(lst)-1)



#Sorts the elements in a list using Counting sort (use only 
#when the range of values is smaller or equal than the number of values).
def countingSort(lst):
    min_val = min(lst)
    max_val = max(lst)
    size = max_val - min_val + 1
    counts = [0]*size

    for i in range(0, len(lst)):
        counts[lst[i]-min_val] += 1

    cur_pos = 0
    for j in range(0, size):
        for k in range(0, counts[j]):
            lst[cur_pos] = j + min_val
            cur_pos += 1


#Sorts the elements, given as (key, val) tuples, in a list using Pigeonhole sort 
#(use only when the range of values is smaller or equal than the number of values).
def pingeonholeSort(lst):
    min_val = min(lst, key=lambda e : e[0])
    max_val = max(lst, key=lambda e : e[0])
    size = max_val - min_val + 1
    indexed_vals = [[] for i in range(0, size)]

    for i in range(0, len(lst)):
        indexed_vals[lst[i][0]-min_val].append(lst[i][1])

    cur_pos = 0
    for j in range(0, size):
        for k in range(0, len(indexed_vals[j])):
            lst[cur_pos] = (j + min_val, indexed_vals[j][k])
            cur_pos += 1


#Returns a list containing the value of each (key,value) tuple in the list
#(useful when using pingeonHoleSort() to keep only the values after sorting).
def stripKeys(lst):
    return [tup[1] for tup in lst]



#Test
lst = createRandomList(15, 1, 100)
print(lst)
oddEvenSort(lst)
print(lst)
