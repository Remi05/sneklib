#Author: Rémi Pelletier
#File:   rp_subsequences.py
#Desc.:  A module containing my implementation of
#        various subsequences related algorithms.

import math


#-----------------Max subarray problem (Kadane's algorithm)--------------------

#Computes the maximum subarray using Kadane's algorithm
#and returns the start and end indices.
def max_subarray_range(array):
    max_ending_here = 0
    max_so_far      = 0
    start = 0
    end   = 0
    for i in range(len(array)):
        if max_ending_here + array[i] <= 0:
            start = i + 1
        else:
            max_ending_here = max_ending_here + array[i]
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




#---------------------Longest common subsequence problem-----------------------

#Builds the table used for the dynamic programming approach of finding
#the longest common subsequence (LCS) between two sequences.
def build_lcs_table(seq1, seq2):
    m = len(seq1)
    n = len(seq2)
    table = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range(0, m):
        for j in range(0, n):
            if seq1[i] == seq2[j]:
                table[i+1][j+1] = table[i][j] + 1
            else:
                table[i+1][j+1] = max(table[i][j+1], table[i+1][j])

    return table


#Returns the length of the longest common subsequece between two
#given sequences using the given LCS table.
def get_lcs_length(lcs_table):
    return lcs_table[-1][-1]


#Computes the length of the longest common subsequence 
#between two given sequences using a dynamic programming approach.
def compute_lcs_length(seq1, seq2):
    lcs_table = build_lcs_table(seq1, seq2)
    return get_lcs_length(lcs_table)


#Finds all the longest common subsequences of
#two sequences using the given LCS table.
def backtrack_all_lcs(lcs_table, seq1, seq2, m, n):
    if m == 0 or n == 0:
        return [[]]
    elif seq1[m-1] == seq2[n-1]:
        shorter_lcs = backtrack_all_lcs(lcs_table, seq1, seq2, m-1, n-1)
        for lcs in shorter_lcs:
            lcs.append(seq1[m-1])
        return shorter_lcs
    else:
        same_length_lcs = []
        if lcs_table[m][n-1] >= lcs_table[m-1][n]:
            shorter_up_lcs = backtrack_all_lcs(lcs_table, seq1, seq2, m, n-1)
            same_length_lcs.extend(shorter_up_lcs)
        if lcs_table[m-1][n] >= lcs_table[m][n-1]:
            shorter_left_lcs = backtrack_all_lcs(lcs_table, seq1, seq2, m-1, n)
            same_length_lcs.extend(shorter_left_lcs)
        return same_length_lcs


#Builds the LCS table for the two given sequences 
#and returns all the longest common subsequences.
def find_all_lcs(seq1, seq2):
    lcs_table = build_lcs_table(seq1, seq2)
    return backtrack_all_lcs(lcs_table, seq1, seq2, len(seq1), len(seq2))




#-------------------Longest increasing subsequence problem---------------------


def binary_search_index(seq, indices, i):
    low  = 1
    high = len(seq) - 1
    mid  = 0

    while high >= low:
        mid =  math.ceil((high+low)/2)
        if seq[indices[mid]] >= seq[i]:
            high = mid - 1
        else:
            low = mid + 1

    return mid


def find_lis(seq):
    indices = []
    last = 0

    for i in range(len(seq)):
        if seq[i] > last:
            indices.append(i)
            last = seq[i]
        else:
            pass





#Test
seq1 = "XMJYAUZ"
seq2 = "MZJAWXU"

lcs_table = build_lcs_table(seq1, seq2)

for line in lcs_table:
    print(line)

print(get_lcs_length(lcs_table))

all_lcs = find_all_lcs(seq1, seq2)

for lcs in all_lcs:
    print(lcs)