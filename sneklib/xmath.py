#Author: Remi Pelletier
#File:   xmath.py
#Desc.:  Module containing various functions related to mathematics.

import math
import time


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