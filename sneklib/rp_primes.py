#Author: Remi Pelletier
#File:   rp_primes.py
#Desc.:  Module containing functions related to primes.

import math


#Constants to help find the n first primes.
PRIME_100    = 523
PRIME_256    = 1613
PRIME_500    = 3581
PRIME_1000   = 7919
PRIME_5000   = 48611
PRIME_10000  = 104729
PRIME_50000  = 611953
PRIME_100000 = 1299709
PRIME_500000 = 7368787


#Finds all the prime numbers smaller or equal to
#the given value (n) using an optimized version
#of the sieve of Eratosthenes.
#Complexity: O(n*log(log(n)))
def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    sieve = [True for _ in range(n-1)]
    max_factor = math.ceil(math.sqrt(n))
    for i in range(2, max_factor+1):
        if sieve[i-2]:
            j = i**2     
            while j <= n:
                sieve[j-2] = False
                j += i
    return [i + 2 for i in range(n-1) if sieve[i]]


#Returns a boolean indicating if the given number is prime.
def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or (n & 1) == 0 or (n % 3) == 0\
       or (((1 << (n-1)) % n) != 1):
        return False
    i = 5
    n_sqrt = math.ceil(math.sqrt(n))
    while i <= n_sqrt:
        if (n % i) == 0 or (n % (i + 2)) == 0:
            return False
        i += 6
    return True



#Tests
print(sieve_of_eratosthenes(PRIME_100000))