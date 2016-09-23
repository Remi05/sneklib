#Author: Rémi Pelletier
#File:   rp_subsequences.py
#Desc.:  A module containing my implementation of
#        various subsequences related algorithms.

import math


#---------------------Longest common subsequence problem-----------------------

#Builds the table used for the dynamic programming approach of finding
#the longest common subsequence (LCS) between two sequences.
def build_lcs_table(seq1, seq2):
    m = len(seq1)
    n = len(seq2)
    lcs_table = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range(0, m):
        for j in range(0, n):
            if seq1[i] == seq2[j]:
                lcs_table[i+1][j+1] = lcs_table[i][j] + 1
            else:
                lcs_table[i+1][j+1] = max(lcs_table[i][j+1], lcs_table[i+1][j])

    return lcs_table


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


#Finds one of the longest common subsequences of
#two sequences using the given LCS table.
def backtrack_lcs(lcs_table, seq1, seq2, m, n):
    if m == 0 or n == 0:
        return list()
    elif seq1[m-1] == seq2[n-1]:
        lcs = backtrack_lcs(lcs_table, seq1, seq2, m-1, n-1)
        lcs.append(seq1[m-1])
        return lcs
    else:
        if lcs_table[m][n-1] >= lcs_table[m-1][n]:
            return backtrack_lcs(lcs_table, seq1, seq2, m, n-1)
        else:
            return backtrack_lcs(lcs_table, seq1, seq2, m-1, n)


#Builds the LCS table for the two given sequences and either
#returns one of the longest common subsequences (find_all = False)
#or all the longest common subsequences (find_all = True).
def longest_common_subsequence(seq1, seq2, find_all = False):
    lcs_table = build_lcs_table(seq1, seq2)
    return (backtrack_all_lcs(lcs_table, seq1, seq2, len(seq1), len(seq2))
            if find_all
            else backtrack_lcs(lcs_table, seq1, seq2, len(seq1), len(seq2)))




#-------------------Longest increasing subsequence problem---------------------

#Finds the highest index for which seq[last_val_indices[index]] > seq[i]
#using binary search (complexity O(log(n)).
def upper_bound(seq, last_val_indices, cur_size, cur_index):
    lo  = 1
    hi = cur_size
    mid  = 0
    while hi >= lo:
        mid =  math.ceil((hi+lo)/2)
        if seq[last_val_indices[mid]] <= seq[cur_index]:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo


#Finds the lowest index for which seq[last_val_indices[index]] > seq[i]
#using binary search (complexity O(log(n)).
def lower_bound(seq, last_val_indices, cur_size, cur_index):
    lo  = 1
    hi = cur_size
    mid  = 0
    while hi >= lo:
        mid =  math.ceil((hi+lo)/2)
        if seq[last_val_indices[mid]] >= seq[cur_index]:
            hi = mid - 1
        else:
            lo = mid + 1
    return lo


#Finds the longest increasing subsequence in the given sequence (O(n*log(n))).
#By default, it finds the longest nondecreasing subsequence but
#by setting strictly_increasing to True, the longest strictly
#increasing subsequence is found.
def longest_increasing_subsequence(seq, strictly_increasing = False):
    seq_length = len(seq)

    if seq_length == 0 or seq_length == 1:
        return seq

    #Array containing the indices of the smallest last value
    #of the LIS of length "index".
    last_val_indices = [0]*(seq_length+1) 
    last_val_indices[1] = 0
    #Array containing the indices of the values that come before
    #the value at "index" in the LIS ending at with seq[index].
    predecessor_indices = [0]*seq_length 
    max_length = 1

    #Fill last_val_indices (and predecessor_indices for LIS reconstruction)
    #with complexity O(n*log(n)).
    for i in range(1, seq_length):
        #Minimum value encountered in the sequence so far.
        if seq[i] < seq[last_val_indices[1]]: 
            last_val_indices[1] = i
            predecessor_indices[i] = i
        #New LIS found ("elif" because the minimum value so far can't be
        #greater than any value encountered so far).
        elif (strictly_increasing and seq[i] > seq[last_val_indices[max_length]]) or\
             (not strictly_increasing and seq[i] >= seq[last_val_indices[max_length]]): 
            max_length += 1
            last_val_indices[max_length] = i
            predecessor_indices[i] = last_val_indices[max_length-1]
        #Smaller value ending a shorter subsequence found ("else" because we
        #are looking for values smaller and greater (caught by the first two
        #conditions otherwise)).
        else:
            #Using binary search, find the index of the value to replace in
            #last_val_indices because seq[i] is smaller than
            #seq[last_val_indices[replacement_index]].
            replacement_index = (lower_bound(seq, last_val_indices, max_length, i)
                                 if strictly_increasing 
                                 else upper_bound(seq, last_val_indices, max_length, i)) 
            last_val_indices[replacement_index] = i
            predecessor_indices[i] = last_val_indices[replacement_index-1]

    #Reconstruct the LIS.
    lis = [0]*max_length
    seq_index = last_val_indices[max_length]
    for i in range(max_length-1, -1, -1):
        lis[i] = seq[seq_index]
        seq_index = predecessor_indices[seq_index]

    return lis




#Test
seq = [10, 30, 5, 50, 70, 30, 40, 60, 60]
print('Nondecreasig: ' +  str(find_lis(seq)))
print('Strictly increasing: ' + str(find_lis(seq, True)))

