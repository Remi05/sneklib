#Author: Rémi Pelletier
#File:   rp_sorting.py
#Desc.:  Module containing various sorting functions.


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



#Test
vector = [4, 12, 3, 8, 76, 1, 34, 2]
mergeSort(vector)
print(vector)
#insertionSort(vector, True)
#print(vector)