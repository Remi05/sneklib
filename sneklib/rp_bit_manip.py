#Author: Remi Pelletier
#File:   rp_bit_manip.py
#Desc.:  Module containing various bit manipulation related functions.


#Returns the absolute value of the
#given number (x) without branching.
def abs_no_branch(x):
    return (x & -(x >= 0)) | ((~x + 1) & -(x < 0)) 

#Counts the number of bits that are
#set (=1) in the given number (x)
#using Brian Kernighan's technique.
def count_set_bits(x):
    count = 0
    while x != 0:
        x &= x-1
        count += 1
    return count

#Counts the number of bits that are
#not set (=0) in the given number (x)
#using Brian Kernighan's technique.
def count_unset_bits(x):
    return count_set_bits(~x)

#Returns the highest set bit in the given number.
#If no bit is set (x = 0), 0 is returned.
def highest_set_bit(x):
    while (x & (x-1)) != 0:
        x &= x-1
    return x

#Returns the index of the highest
#set bit in the given number.
#If no bit is set (x = 0), -1 is returned.
def highest_set_bit_pos(x):
    if x == 0:
        return -1
    count = 0
    while x != 0:
        x >>= 1
        count += 1
    return count - 1

#Returns a boolean indicating whether or
#not the given value (x) is even.
def is_even(x):
    return (x & 1) == 0

#Returns a boolean indicating whether or
#not the given value (x) is odd.
def is_odd(x):
    return (x & 1) != 0

#Returns a boolean indicating whether or
#not the given value (x) is a power of 2.
def is_power_of_two(x):
    return (x & (x-1)) == 0

#Returns the lowest set bit in the given number.
#If no bit is set (x = 0), 0 is returned.
def lowest_set_bit(x):
    return x & -x

#Returns the index of the lowest
#set bit in the given number.
#If no bit is set (x = 0), -1 is returned.
def lowest_set_bit_pos(x):
    if x == 0:
        return -1
    count = 0
    while (x & 1) == 0:
        x >>= 1
        count += 1
    return count

#Returns the maximum of the two given
#values (x and y) without branching.
def max_no_branch(x, y):
    return y ^ ((x ^ y) & -(x > y))

#Returns the minimum of the two given
#values (x and y) without branching.
def min_no_branch(x, y):
    return y ^ ((x ^ y) & -(x < y))

#Returns the power of 2 that is nearest to x.
#If x if half-way between two powers of 2,
#the biggest of the two is chosen. 
#ie.: x = 48 -> 64-48 = 48-32 = 16 -> returns 64
def nearest_power_of_two(x):
    msb_pos = highest_set_bit_pos(x)
    return 1 << (msb_pos + ((x >> (msb_pos-1))&1))

#Returns a boolean indicating whether or not the two
#given values (x and y) have opposite signs (+/-).
def opposite_signs(x, y):
    return (x ^ y) < 0

#Returns a boolean indicating whether or not the two
#given values (x and y) have the same sign (+/-).
def same_sign(x, y): 
    return not opposite_signs(x, y)

#Swaps the odd and even bits in the given number (x).
#The given number must be representable on 64 bits.
def swap_odd_even_bits(x):
    even = (x & 0xAAAAAAAAAAAAAAAA) >> 1
    odd  = (x & 0x5555555555555555) << 1
    return even | odd

#Swaps the values of x and y without
#using a temporary variable.
def swap_values(x, y):
    x ^= y
    y ^= x
    x ^= y
    return x, y



#Tests
#x = 10
#y = 55
#print(min_no_branch(x,y))

