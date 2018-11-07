#Author: Remi Pelletier
#File:   array_search.py
#Desc.:  Module containing various array search functions.


#Finds the position of an element (x)
#in the given array (arr) using binary search.
#The array needs to already be sorted.
#Returns -1 if the element is not found.
#Complexity: O(log(n))
def binary_search(arr, x, lo = 0, hi = -1):
    if x is None or arr is None or len(arr) == 0:
        return -1
    length = len(arr)
    lo %= length
    hi %= length # = to len(arr) - 1 when hi = -1 (default).
    while hi >= lo:
        mid = (hi + lo) // 2
        if arr[mid] == x:
            return mid
        if x < arr[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1


#Finds the position of an element (x)
#in the given array (arr) using linear search.
#Returns -1 if the element is not found.
#Complexity: O(n)
def linear_search(arr, x):
    if x is None or arr is None or len(arr) == 0:
        return -1
    pos = 0
    for val in arr:
        if val == x:
            return pos
        pos += 1
    return -1


#Finds the position of the first element in the given
#array (arr) which doesn't evaluate to less than the
#given value (x) using binary search.
#The array needs to be already sorted.
#If no value is found within the given bounds hi + 1
#is returned ( = len(arr) by default).
#Complexity: O(log(n))
def lower_bound(arr, x, lo = 0, hi = -1):
    if x is None or arr is None or len(arr) == 0:
        return -1
    length = len(arr)
    lo %= length
    hi %= length # = to len(arr) - 1 when hi = -1 (default).
    while hi >= lo:
        mid = (hi + lo) // 2
        if arr[mid] >= x:
            hi = mid - 1
        else:
            lo = mid + 1
    return lo


#Finds the position of the first element in the given
#array (arr) which evaluates to greater than the
#given value (x) using binary search.
#The array needs to be already sorted.
#If no value is found within the given bounds hi + 1
#is returned ( = len(arr) by default).
#Complexity: O(log(n))
def upper_bound(arr, x, lo = 0, hi = -1):
    if x is None or arr is None or len(arr) == 0:
        return -1
    length = len(arr)
    lo %= length
    hi %= length # = to len(arr) - 1 when hi = -1 (default).
    while hi >= lo:
        mid = (hi + lo) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo


#-----------------Max subarray problem (Kadane's algorithm)--------------------

#Computes the maximum subarray using Kadane's algorithm
#and returns the start and end indices.
def max_subarray_range(array):
    max_ending_here = 0
    max_so_far = 0
    start = 0
    end = 0
    for i in range(len(array)):
        if max_ending_here + array[i] <= 0:
            start = i + 1
        else:
            max_ending_here += array[i]
        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            end = i
    return start, end


#Returns the maximum subarray computed using Kadane's algorithm.
def max_subarray(array):
    start, end = max_subarray_range(array)
    return array[start:end+1]


#Returns the sum of the elements in the maximum
#subarray computed using Kadane's algorithm.
def max_subarray_sum(array):
    return sum(max_subarray(array))

