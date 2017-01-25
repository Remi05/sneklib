#Author: Remi Pelletier
#File:   rp_random.py
#Desc.:  A module containing my implementation of various
#        sequence permutations related algorithms.

import random


#Swaps the elements in a sequence at the given indices.
def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]


#Randomly shuffles a sequence in place using Fisher-Yates (or Knuth) shuffle.
def fisher_yates_shuffle(lst, seed=None):
    length = len(lst)
    random.seed(seed)
    for i in range(length-2):
        j = random.randint(i, length-1)
        swap(lst, i, j)



#Test
a = [1, 3, 12, 34, 67, 101, 307]
fisher_yates_shuffle(a)
print(a)