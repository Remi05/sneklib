#Author: Rémi Pelletier
#File:   rp_string_search.py
#Desc.:  A module containing my implementation of
#        various string search related algorithms.


#-----------------------Longest common substring problem-----------------------

#...




#---------------------------Substring search problem---------------------------


#____________________________Rabin-Karp algorithm______________________________

#Rolling hash function (used by default in my implementation of Rabin-Karp)
def rk_rolling_hash(new_str, old_str = None, old_hash = None):
    length = len(new_str)
    if old_str == None or old_hash == None:
        return sum(ord(new_str[-1-i]) * (101 ** i) for i in range(length))
    else:
        return 101 * (old_hash - (ord(old_str[0]) * (101**(length-1)))) + ord(new_str[-1])


#Finds the first or all the occurences of a pattern in a string using Rabin-Karp.
#find_all = True  -> found : [indices]   / not found : []
#find_all = False -> found : index       / not found : None
def rabin_karp_search(s, pattern, find_all = False, rolling_hash = rk_rolling_hash):
    m = len(pattern)
    n = len(s)

    indices = []

    if m > n:
        return indices

    pattern_hash = rolling_hash(pattern)
    str_hash = rolling_hash(s[0:m])

    for i in range(n-m+1):
        if str_hash == pattern_hash and s[i:i+m] == pattern:
            indices.append(i)
            if not find_all:
                return i
        str_hash = rolling_hash(s[i+1:i+m+1], s[i:i+m], str_hash)

    return indices if find_all else None


#Finds the first all the occurences of each pattern of a set in a string using Rabin-Karp.
#**Note**: All the patterns in the set must be of same length.
#The indices are returned in a dictionnary where the key is the pattern and the value is given as follows:
#find_all = True  -> found : [indices]   / not found : []
#find_all = False -> found : index       / not found : None
def rabin_karp_set_search(s, pattern_set, find_all = False, rolling_hash = rk_rolling_hash):
    hash_dict = { rolling_hash(pattern) : pattern for pattern in pattern_set }
    hash_set = hash_dict.keys()
    indices_dict = { pattern : [] if find_all else None for pattern in pattern_set }
    found_set = set()

    m = len(next(iter(pattern_set)))
    n = len(s)

    if m > n:
        indices_dict

    str_hash = rolling_hash(s[0:m])

    for i in range(n-m+1):
        if str_hash in hash_set and s[i:i+m] in pattern_set:
            if find_all:
                indices_dict[s[i:i+m]].append(i)
            elif not s[i:i+m] in found_set:
                indices_dict[s[i:i+m]] = i
                found_set.add(s[i:i+m])
                if not pattern_set.difference(found_set):
                    return indices_dict
        str_hash = rolling_hash(s[i+1:i+m+1], s[i:i+m], str_hash)

    return indices_dict



#________________________Knuth-Morris-Pratt algorithm__________________________

#Creates the partial match table used in the KMP algorithm.
def create_partial_match_table(pattern):
    pattern_length = len(pattern)
    table = [0] * (pattern_length + 1)
    table[0] = -1
    table[1] = 0

    i = 2 #Table index
    c = 0

    while i <= pattern_length:
        if pattern[i-1] == pattern[c]:
            c += 1
            table[i] = c
            i += 1
        elif c > 0:
            c = table[c]
        else: #i = 0
            table[i] = 0
            i += 1

    return table


#Finds the first or all the occurences of a pattern in a string using Knuth-Morris-Pratt (KMP).
#find_all = True  -> found : [indices]   / not found : []
#find_all = False -> found : index       / not found : None
def kmp_search(s, pattern, find_all = False):
    table     = create_partial_match_table(pattern)
    start_pos = 0
    cur_pos   = 0
    indices   = []

    str_length     = len(s)
    pattern_length = len(pattern)

    while start_pos + cur_pos < str_length:
        if s[start_pos + cur_pos] == pattern[cur_pos]:
            cur_pos += 1
            if cur_pos == pattern_length:
                if not find_all:
                    return start_pos
                else:
                    indices.append(start_pos)
                    start_pos += cur_pos - table[cur_pos]
                    cur_pos = table[cur_pos]
        else:
            if cur_pos != 0:
                start_pos += cur_pos - table[cur_pos]
                cur_pos = table[cur_pos]
            else:
                start_pos += 1

    return indices if find_all else None



#___________________________Boyer-Moore algorithm______________________________




#_______________________Boyer-Moore-Horspoole algorithm________________________





#Test
pattern = "dldj"
pattern_set = set(["abba", "djgk", "bbbb", "dldj", "kkkk"])
string = "abbbbbbcdaaaabadjgkldldjabbbbacbaabbabbkla"

print(kmp_search(string, pattern, True))
