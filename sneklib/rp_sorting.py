#Author: Rémi Pelletier
#File:   rp_sorting.py
#Desc.:  Module containing various sorting functions.


import random
import itertools
import rp_data_structures


#-----------------------------Sorting functions--------------------------------

#Swaps two elements in a list .
def swap(lst, i1, i2):
    lst[i1], lst[i2] = lst[i2], lst[i1]


#Sorts the elements in a list using Selection sort, 
#can sort in reverse order as well.
def selection_sort(lst, reverse = False):
    for i in range(0, len(lst)-1):
        min = i
        for j in range(i+1, len(lst)):
            if (not reverse and lst[j] < lst[min]) or\
               (    reverse and lst[j] > lst[min]):
                min = j
        swap(lst, i, min)


#Finds the element that would be at index k if the list was to bebsorted 
#(without necessarily sorting the list) using a shortened selection sort.
def select(lst, k):
    k = max(k, len(lst)-1)
    cpy = lst[:]
    i = 0
    while i <= k:
        min = i
        for j in range(i+1, len(cpy)):
            if cpy[j] < cpy[min]:
                min = j
        swap(cpy, i, min)
        i += 1
    return cpy[k]


#Sorts the elements in a list using Bubble sort, 
#can sort in reverse order as well.
def bubble_sort(lst, reverse = False):
    v_length = len(lst)
    for i in range(0, v_length-1):
        for j in range(v_length-1, i, -1):
            if (not reverse and lst[j] < lst[j-1]) or\
               (    reverse and lst[j] > lst[j-1]):
                swap(lst, j, j-1)


#Sorts the elements in a list using an improved version of Bubble sort, 
#can sort in reverse order as well.
def improved_bubble_sort(lst, reverse = False):
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


#Function used in odd_even_sort() to perform either an odd-even 
#or an even-odd iteration. Prevents code duplication and
#conditional statement evaluation at each iteration.
def _odd_even_iter(lst, start, end, reverse = False):
    swapped = False
    for i in range(start, end, 2):
        if (not reverse and lst[i] < lst[i-1]) or\
           (    reverse and lst[i] > lst[i-1]):
            swap(lst, i, i-1)
            swapped = True  
    return swapped


#Sorts the elements in a list using Odd-even sort, 
#can sort in reverse order as well.
def odd_even_sort(lst, reverse = False):
    length = len(lst)
    swapped = True
    while swapped:
        #Odd-even iteration
        swapped  = _odd_even_iter(lst, 1, length, reverse)
        #Even-odd iteration
        swapped |= _odd_even_iter(lst, 2, length, reverse) 


#Sorts the elements in a list using Comb sort, 
#can sort in reverse order as well.
def comb_sort(lst, reverse = False):
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


#Sorts the elements in a list using Cocktail sort, 
#can sort in reverse order as well.
def cocktail_sort(lst, reverse = False):  
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


#Sorts the elements in a list using Insertion sort, 
#can sort in reverse order as well.
def insertion_sort(lst, reverse = False):
    for i in range(1, len(lst)):
        tmp = lst[i]
        j = i
        while j > 0 and ((not reverse and tmp < lst[j-1]) or\
                         (    reverse and tmp > lst[j-1])):
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = tmp


#Sorts the elements in a list, within the given range (start and end
#are both included), using Insertion sort, can sort in reverse order as well.
def insertion_sort_range(lst, start, end, reverse = False):
    for i in range(start+1, end+1):
        tmp = lst[i]
        j = i
        while j > start and ((not reverse and tmp < lst[j-1]) or\
                             (    reverse and tmp > lst[j-1])):
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = tmp


#Sorts the elements in a list using Gnome sort,
#can sort in reverse order as well.
def gnome_sort(lst, reverse = False):
    v_length = len(lst)
    i = 1
    while i < v_length:
        if i == 0 or ((not reverse and lst[i-1] <= lst[i]) or\
                      (    reverse and lst[i-1] >= lst[i])):
            i += 1
        else:
            swap(lst, i-1, i)
            i -= 1


#Sorts the elements in a list using Heap sort.
def heap_sort(lst):
    heap = rp_data_structures.BinaryHeap()
    heap.insert_array(lst)
    i = 0
    while not heap.empty():
        lst[i] = heap.pop()
        i += 1


#Sorts the elements in a list using Tree sort,
#can sort in reverse order as well.
def tree_sort(lst, reverse = False):
    bst = rp_data_structures.ArrayBST()
    bst.insert_array(lst)
    if reverse:
        lst[:] = bst.get_reverse_array()
    else:
        lst[:] = bst.get_sorted_array()


#Merges the list to be sorted and the temporary list in the specified range
#(used for sorting using merge_sort()).
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


#Recursive function used to sort sections of a list (used by merge_sort()).
def _merge_sort(lst, tmp, left, right):
    if right > left:
        center = (left + right) // 2
        _merge_sort(lst, tmp, left, center)
        _merge_sort(lst, tmp, center + 1, right)
        _merge(lst, tmp, left, center + 1, right)


#Sorts the elements in a list using Merge sort.
def merge_sort(lst):
    tmp = [0]*len(lst)
    _merge_sort(lst, tmp, 0, len(lst)-1)



#Partitions a list using the Lomuto partition scheme
#(used for Quicksort and Quickselect).
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


#Recursive function used to find the element that would be at
#index k if the list was to be sorted (used by quickselect()).
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
    return _quickselect(lst[:], 0, len(lst)-1, k)


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
def counting_sort(lst):
    min_val, max_val = min(lst), max(lst)
    size = max_val - min_val + 1
    counts = [0]*size

    for i in range(0, len(lst)):
        counts[lst[i]-min_val] += 1

    cur_pos = 0
    for j in range(0, size):
        for k in range(0, counts[j]):
            lst[cur_pos] = j + min_val
            cur_pos += 1


#Sorts the elements in a list usin Bucket sort (use only 
#when the range of values is smaller or equal than the number of values). 
def bucket_sort(lst, nb_buckets=10, cutoff=0):
    if nb_buckets == 1 or len(lst) <= cutoff:
        insertion_sort(lst)
        return

    min_val, max_val = min(lst), max(lst)
    if min_val == max_val:
        return

    val_range = max_val - min_val
    bucket_range = val_range // nb_buckets + 1
    buckets = [[] for _ in range(nb_buckets)]

    for val in lst:
        buckets[(val-min_val) // bucket_range].append(val)

    for bucket in buckets:
        bucket_sort(bucket, nb_buckets, cutoff)

    lst[:] = list(itertools.chain.from_iterable(buckets))
    


#Sorts the elements, given as (key, val) tuples, in a list using Pigeonhole sort 
#(use only when the range of values is smaller or equal than the number of values).
def pingeonhole_sort(lst):
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
#(useful when using pingeon_hole_sort() to keep only the values after sorting).
def strip_keys(lst):
    return [tup[1] for tup in lst]





#-----------------------------------Tests--------------------------------------

#Creates a list of the given size and fills it with random
#numbers between min_val and max_val (both inclusive).
def create_random_list(size, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(size)]


#Returns a boolean indicating if the list is sorted
#(can verify if a list is sorted in reverse order as well).
def is_sorted(lst, reverse = False):
    length = len(lst)
    if lst is None or length == 0:
        return False
    for i in range(0, length-1):
        if not reverse and lst[i] > lst[i+1] or\
           reverse and lst[i] < lst[i+1]:
            return False
    return True


SIZES  = [10, 50, 250]
RANGES = [(-100, -10), (-50, 50), (10, 100)]

#Runs tests on a sorting function using all the cominations
#of sizes and ranges given in SIZES and RANGES.
def run_tests(func, args):
    nb_tests = 0
    passed_tests = 0
    for size in SIZES:
        for val_range in RANGES:
            nb_tests += 1
            min_val, max_val = val_range
            lst = create_random_list(size, min_val, max_val)
            func_args = (lst, *args)
            try:
                func(*func_args)
            except Exception as e:
                print('An error occured with arguments : ' + str(func_args) + '\n')
                print('Error : ' + str(e))
                continue
            if not is_sorted(*func_args):
                print('Failed test with arguments : ' + str(func_args) + '\n')
            else:
                passed_tests += 1
    return passed_tests, nb_tests


#Tests a given sorting function.
def test_function(func, has_reverse):
    print('Testing : ' + func.__name__)
    passed, total = 0, 0
    if has_reverse:
        p1, t1 = run_tests(func, (False,))
        p2, t2 = run_tests(func, (True,))
        passed, total = p1+p2, t1+t2
    else:
        passed, total = run_tests(func, ())
    print(str(passed) + '/' + str(total) + ' tests passed.\n')


#pigeonholeSort is not in this list since it uses 
#(key, value) pairs instead of a standard list.
SORTING_FUNTIONS = [ (bubble_sort,    True),  (bucket_sort,          False), 
                     (cocktail_sort,  True),  (comb_sort,            True), 
                     (counting_sort,  False), (gnome_sort,           True),
                     (heap_sort,      False), (improved_bubble_sort, True),
                     (insertion_sort, True),  (merge_sort,           False),
                     (odd_even_sort,  True),  (quicksort,            False),
                     (selection_sort, True),  (tree_sort,            True) ]
  
#Tests all the functions in SORTING_FUNCTIONS.
def test_all_functions():
    for func, has_reverse in SORTING_FUNTIONS:
        test_function(func, has_reverse)



#Program entry point.
test_all_functions()