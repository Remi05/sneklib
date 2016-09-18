#Author: Remi Pelletier
#File:   rp_dynamic_prog.py
#Desc.:  Module containing my implementation of dynamic
#        programming solutions to various problems.


#Pseudo-polynomial solution to the 0-1 knapsack problem using dynamic programming.
def knapsack_01(max_weight, weights, values, nb_items = None):
    nb_items = len(weights) if nb_items is None else nb_items
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


def knapsack_bounded():
    pass #TODO

def knapsack_unbounded():
    pass #TODO