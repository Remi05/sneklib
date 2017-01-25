#Author: Remi Pelletier
#File:   rp_math.py
#Desc.:  Module containing various functions related to mathematics.

import math
import time

#TODO: Write proper tests.
#TODO: Add additional pertinent functions.


#Returns a set containing all the factors of x.
def factors(x):
    if x == 0:
        return {}
    divs = {1, x}
    for i in range(2, int(math.ceil(math.sqrt(x)))+1):
        if (x % i) == 0:
            divs.add(i)
            divs.add(x // i)
    return divs


#Returns the greatest common divisor of a and b.
def gcd(a, b):
    return gcd_mod_it(a, b)


def gcd_binary(a, b):
    pass #TODO


#Computes the gcd of a and b iteratively using the modulus operator.
def gcd_mod_it(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#Computes the gcd of a and b recursively using the modulus operator.
def gcd_mod_rec(a, b):
    if b == 0:
        return a
    return gcd_mod_rec(a, a % b)


#Computes the gcd of a and b iteratively using substraction.
def gcd_sub_it(a, b):
    if a == 0:
        return b
    while b != 0:
        if a > b:
            a -= b
        else:
            b -= a
    return a


#Computes the gcd of a and b recursively using substraction.
def gcd_sub_rec(a, b):
    if a == 0:
        return b
    if a > b:
        return gcd_sub_rec(b, a-b)
    return gcd_sub_rec(b-a, a)


#Returns the least common multiple of a and b.
def lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return int(math.fabs(a)) // gcd(a, b) * int(math.fabs(b))


#Computes b^e mod m (b**e % m).
def modular_pow(b, e, m):
    if m == 1:
        return 0
    res = 1
    b %= m
    while e > 0:
        if e & 1:
            res = (res * b) % m
        e >>= 1
        b = (b**2) % m
    return res 


#Reduces the fraction a/b.
def reduce_fraction(a, b):
    gcd_val = gcd(a, b)
    return a // gcd_val, b // gcd_val




#-----------------------------------Tests--------------------------------------

#_____factors() test_____
#x = 60
#print(factors(x))


#_____gcd() test_____
#a = 2940
#b = 3150 
#print(gcd(a, b))


#_____lcm() test_____
#a = 2940
#b = 3150
#print(lcm(a, b))


#_____modular_pow() test_____
#b = 5004759379182
#e = 997179
#m = 497914
#start = time.time()
#val1 = (b**e) % m
#print(time.time()-start)
#start = time.time()
#val2 = modular_pow(b, e, m)
#print(time.time()-start)
#print("val1: {0}    val2: {1}".format(val1, val2))


#_____reduce_fraction() test_____
#a = 180
#b = 240
#print("{0}/{1} can be reduced to {2}/{3}".format(a, b, *(reduce_fraction(a,b))))