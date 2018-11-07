#Author: Remi Pelletier
#Desc.:  Module containing various statistics functions.

import math


#--------------------------------Miscellaneous---------------------------------

#Returns the factorial of n (n!).
def factorial(n):
    result = 1
    for i in range(n+1):
        result *= i
    return result

#Returns the combination of k in n (nCk).
def combination(k, n):
    return factorial(n) / (factorial(n - k) * factorial(k))

#Returns the permutation of k in n (nPk).
def permutation(k, n):
    return factorial(n) / factorial(n - k)

#Returns the average of the given samples.
def sample_average(samples):
    return sum(samples) / len(samples)

#Returns the variance of the given samples.
def sample_variance(samples):
    avg = sample_average(samples)
    return sum((sample - avg)**2 for sample in samples)

#Returns the probability for a random variable of which 
#the CDF is given to take a value in the given range [a, b].
def in_range(cdf, a, b):
    return cdf(b) - cdf(a)

#Returns the probability for a random variable of which the 
#CDF is given to take a value outside the given range [a, b].
def outside_range(cdf, a, b):
    return 1 - in_range(cdf, a, b)


#----------------------------Binomial distribution-----------------------------

def binomial_val(n, p):
    pass

#Returns the value of the mass function (pX(x)) of a binomial 
#distribution of parameters n and p for the given x.
def binomial_mass_function(n, p, x):
    return 0 if n <= 0 else combination(x, n) * p**x * (1 - p)**(n - x)

#Returns the value of the cumulative distribution function (FX(x))
#of a binomial distribution of parameters n and p for the given x.
def binomial_cdf(n, p, x):
    return sum(binomial_mass_function(n, p, i) for i in range(x+1))

#Returns the mean (E(X)) of a binomial distribution of parameters n and p.
def binomial_mean(n, p):
    return n * p

#Returns the variance (V(X)) of a binomial distribution of parameters n and p.
def binomial_variance(n, p):
    return n * p * (1 - p)

#Returns the median of a binomial distribution of parameters n and p.
def binomial_median(n, p):
    return math.floor(n * p)

#Returns the mode of a binomial distribution of parameters n and p.
def binomial_mode(n, p):
    return math.floor((n + 1) * p)


#---------------------------Geometric distribution-----------------------------

#Returns the value of the mass function (pX(x)) of a 
#geometric distribution of parameter p for the given x.
def geometric_mass_function(p, x):
    return (1 - p)**(x - 1) * p

#Returns the value of the cumulative distribution function (FX(x))
#of a geometric distribution of parameter p for the given x.
def geometric_cdf(p, x):
    return 0 if x < 1 else 1 - (1 - p)**x

#Returns the mean (E(X)) of a geometric distribution of parameter p.
def geometric_mean(p):
    return 0 if p == 0 else 1 / p

#Returns the variance (V(X)) of a geometric distribution of parameter p.
def geometric_variance(p):
    return 0 if p == 0 else (1 - p) / p**2


#-------------------------Hypergeometric distribution--------------------------

#Returns the value of the mass function (pX(x)) of a hypergeometric 
#distribution of parameters N, K and n for the given x.
def hypergeometric_mass_function(N, K, n, x):
    return combination(x, K) * combination(n-x, N-K) / combination(n, N) 

#Returns the value of the cumulative distribution function (FX(x))
#of a hypergeometric distribution of parameters N, K and n for the given x.
def hypergeometric_cdf(N, K, n, x):
    return sum(hypergeometric_mass_function(N, K, n, i) for i in range(x+1))

#Returns the mean (E(X)) of a hypergeometric 
#distribution of parameters N, K and n.
def hypergeometric_mean(N, K, n):
    return 0 if N == 0 else n * K / N

#Returns the variance (V(X)) of a hypergeometric 
#distribution of parameters N, K and n.
def hypergeometric_variance(N, K, n):
    return 0 if N == 0 else n * K / N * (1 - K / N) * ((N - n) / (N - 1))

#Returns the mode of a hypergeometric distribution of parameters N, K and n.
def hypergeometric_mode(N, K, n):
    return ((n + 1) * (K + 1)) // (N + 2)


#----------------------------Poisson distribution------------------------------

#Returns the value of the mass function (pX(x)) of a 
#poisson distribution of parameter c for the given x.
def poisson_mass_function(c, x):
    return math.exp(-c) * c**x / factorial(x)

#Returns the value of the cumulative distribution function (FX(x))
#of a poisson distribution of parameter c for the given x.
def poisson_cdf(c, x):
    return sum(poisson_mass_function(c, i) for i in range(x+1))


#----------------------------Uniform distribution------------------------------

#Returns the value of the denisty function (fX(x)) of a 
#uniform distribution of parameters a and b for the given x.
def uniform_density_function(a, b, x):
    return 0 if x < a or x > b else 1 / (b - a)

#Returns the value of the cumulative distribution function (FX(x))
#of a uniform distribution of parameters a and b for the given x.
def uniform_cdf(a, b, x):
    return min(max((x - a) / (b - a), 0), 1)

#Returns the mean (E(X)) of a uniform 
#distribution of parameters a and b,
def uniform_mean(a, b):
    return (a + b) / 2

#Returns the variance (V(X)) of a uniform 
#distribution of parameters a and b.
def uniform_variance(a, b):
    return (b - a)**2 / 12


#--------------------------Exponential distribution----------------------------

#Returns the value of the density function (fX(x)) of an 
#exponential distribution of parameter c for the given x.
def exponential_density_function(c, x):
    return 0 if x < 0 else c * math.exp(-c * x)

#Returns the value of the cumulative distribution function (FX(x))
#of an exponential distribution of parameter c for the given x.
def exponential_cdf(c, x):
    return 0 if x < 0 else 1 - math.exp(-c * x)

#Returns the mean (E(X)) of an 
#exponential distribution of parameter c.
def exponential_mean(c):
    return 0 if c == 0 else 1 / c

#Returns the variance (V(X)) of an 
#exponential distribution of parameter c.
def exponential_variance(c):
    return 0 if c == 0 else 1 / c**2

#Returns the median of an exponential 
#distribution of parameter c.
def exponential_median(c):
    return 0 if c == 0 else math.log(2) / c


#-----------------------------Normal distribution------------------------------

#Returns the value z of the standard normal distribution 
#corresponding to the given value x of the normal 
#distribution of parameters mean and std.
def x_to_z(mean, std, x):
    return (x - mean) / std

#Returns the value of phi (CDF of a standard normal distribution).
def phi(val):
    return (1.0 + math.erf(val / math.sqrt(2.0))) / 2.0

#Returns the value of the density function (fX(x))
#of a standard normal distribution for the given z.
def normal_z_density_function(z):
    return normal_x_density_function(0, 1, z)

#Returns the value of the density function (fX(x)) of a normal 
#distribution of parameters mean and std for the given x.
def normal_x_density_function(mean, std, x):
    return math.exp(-((x - mean)**2) / (2 * std**2)) / (std * math.sqrt(2 * math.pi))

#Returns the value of the cumulative distribution function (FX(x))
#of a standard normal distribution for the given z.
def normal_z_cdf(z):
    return phi(z)

#Returns the value of the cumulative distribution function (FX(x))
#of a normal distribution of parameters mean and std for the given x.
def normal_x_cdf(mean, std, x):
    return normal_z_cdf(x_to_z(mean, std, x))