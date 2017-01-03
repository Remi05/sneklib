#Author: Remi Pelletier
#File:   rp_dynamic_prog.py
#Desc.:  Module containing my implementation of dynamic
#        programming solutions to various problems.


#----------------------------------Fibonacci-----------------------------------

#Returns nth number in the Fibonacci 
#sequence using a bottom-up approach.
def fibonacci(n):
    if n < 1:
        return None
    prev = 1
    res  = 1
    tmp  = 0
    for i in range(2, n):
        tmp = prev
        prev = res
        res += tmp
    return res


#Recursive function used in fibonacci_mem().
def _fibonacci_mem_rec(n, arr):
    if n > len(arr):
        p1 = _fibonacci_mem_rec(n-1, arr)
        p2 = _fibonacci_mem_rec(n-2, arr)
        arr.append(p1 + p2)
    return arr[n-1]


#Returns nth number in the Fibonacci sequence 
#using a top-down approach with memorization.
def fibonacci_mem(n):
    if n < 1:
        return None
    arr = [1, 1]
    return _fibonacci_mem_rec(n, arr)


#Returns the n first numbers in the Fibonacci
#sequence using a bottom-up approach.
def fibopnacci_seq(n):
    if n < 1:
        return []
    if n == 1:
        return [1]
    seq = [1, 1]
    for i in range(2, n):
        seq.append(seq[i-1] + seq[i-2])
    return seq

          

#--------------------------------Change making---------------------------------

def change_making_nb_coins(coins, total):
    pass

def change_making_nb_ways(coins, total):
    #There is only one way of getting a
    #total of 0 (not taking any coin).
    if total == 0:
        return 1

    #It is impossible to get a negative total using positive values.
    #It is also impossible to get a positive total using 0 coins.
    if total < 0 or len(coins) == 0:
        return 0
 
    coins = list(set(coins)) #Remove duplicates.
    coins.sort() #Sort the coins.
    dp = [0 for _ in range(total+1)] #Initialize the table.   
    dp[0] = 1 #Set the edge case.

    #Compute the total number of ways we can
    #obtain a given total (cur_total) using all 
    #the coins up to the current one (coin).
    for coin in coins:
        for cur_total in range(coin, total+1):
            dp[cur_total] += dp[cur_total-coin]

    #The solution is the number of ways we can
    #make the total amount using all the coins.
    return dp[total]


def change_making_coins_list(coins, total):
    pass



#----------------------------------Knapsack------------------------------------

#Pseudo-polynomial solution to the 0-1 knapsack
#problem using dynamic programming.
def knapsack_01(max_weight, weights, values):
    nb_items = len(weights)
    dp = [[0 for x in range(max_weight+1)] for y in range(nb_items+1)]

    for i in range(1, nb_items+1): #Compute the max value using only the fist i items.
        for w in range(1, max_weight+1): #Compute the max value with max weight equal to w.
            if weights[i-1] <= w:
                #The current max value is either obtained by adding the
                #current item or by not adding it (max of the two).
                dp[i][w] = max(values[i-1] + dp[i-1][w - weights[i-1]], dp[i-1][w])
            else:
                #If the current item has a bigger weight than
                #the current max weight, the curent max value
                #is equal to the previous max value.
                dp[i][w] = dp[i-1][w] 

    #Return the max value obtained using all items
    #with max_weight as the maximum total weight.
    return dp[nb_items][max_weight] 


def knapsack_bounded(max_weight, weights, values, max_rep):
    pass #TODO

def knapsack_unbounded(max_weight, weights, values):
    pass #TODO