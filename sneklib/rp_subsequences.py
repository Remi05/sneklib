
#-----------------Max subarray problem (Kadane's algorithm)--------------------

#Computes the maximum subarray using Kadane's algorithm
#and returns the start and end indices.
def maxSubarrayRange(array):
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
def maxSubarray(array):
    start, end = maxSubarrayRange(array)
    return array[start:end+1]


#Returns the sum of the elements in the maximum
#subarray computed using Kadane's algorithm.
def maxSubarraySum(array):
    return sum(maxSubarray(array))



#---------------------Longest common subsequence problem-----------------------

#Builds the table used for the dynamic programming approach of finding
#the longest common subsequence (LCS) between two sequences.
def buildLCSTable(seq1, seq2):
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
def getLCSLength(lcs_table):
    return lcs_table[-1][-1]


#Computes the length of the longest common subsequence 
#between two given sequences using a dynamic programming approach.
def computeLCSLength(seq1, seq2):
    lcs_table = buildLCSTable(seq1, seq2)
    return getLCSLength(lcs_table)


#Finds all the longest common subsequences of
#two sequences using the given LCS table.
def backtrackAllLCS(lcs_table, seq1, seq2, m, n):
    if m == 0 or n == 0:
        return [[]]
    elif seq1[m-1] == seq2[n-1]:
        shorter_lcs = backtrackAllLCS(lcs_table, seq1, seq2, m-1, n-1)
        for lcs in shorter_lcs:
            lcs.append(seq1[m-1])
        return shorter_lcs
    else:
        same_length_lcs = []
        if lcs_table[m][n-1] >= lcs_table[m-1][n]:
            shorter_up_lcs = backtrackAllLCS(lcs_table, seq1, seq2, m, n-1)
            same_length_lcs.extend(shorter_up_lcs)
        if lcs_table[m-1][n] >= lcs_table[m][n-1]:
            shorter_left_lcs = backtrackAllLCS(lcs_table, seq1, seq2, m-1, n)
            same_length_lcs.extend(shorter_left_lcs)
        return same_length_lcs


#Builds the LCS table for the two given sequences 
#and returns all the longest common subsequences.
def findAllLCS(seq1, seq2):
    lcs_table = buildLCSTable(seq1, seq2)
    return backtrackAllLCS(lcs_table, seq1, seq2, len(seq1), len(seq2))




#Test
seq1 = "XMJYAUZ"
seq2 = "MZJAWXU"

lcs_table = buildLCSTable(seq1, seq2)

for line in lcs_table:
    print(line)

print(getLCSLength(lcs_table))

all_lcs = findAllLCS(seq1, seq2)

for lcs in all_lcs:
    print(lcs)