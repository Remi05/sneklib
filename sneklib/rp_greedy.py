#Author: Remi Pelletier
#File:   rp_greedy.py
#Desc.:  Module containing miscellaneous greedy algorithms.


def make_change(coins, total):
    coins = sorted(list(coins), reverse = True)
    solution = []
    remainder = total
    for coin in coins:
        if remainder == 0:
            break
        nb_coins = int(remainder // coin)
        solution.extend([coin]*nb_coins)
        remainder -= nb_coins * coin
    return solution


def knapsack_01(max_weight, weights, values):
    items = zip(weights, values)
    items = sorted(items, lambda i: i[1]/id[0])
    total_value = 0
    remainder = max_weight
    for item in items:
        if remainder == 0:
            break
        if remainder >= item[0]:
            total_value += item[1]
            remainder -= item[0]
    return total_value


def knapsack_bounded(max_weight, weights, values, max_rep):
    items = zip(weights, values)
    items = sorted(items, lambda i: i[1]/id[0])
    total_value = 0
    remainder = max_weight
    for item in items:
        if remainder == 0:
            break
        nb_items = min(remainder // item[0], max_rep)
        value += nb_items * item[1]
        remainder -= nb_items * item[0]
    return total_value


def knapsack_unbounded(max_weight, weights, values):
    items = zip(weights, values)
    items = sorted(items, lambda i: i[1]/id[0])
    total_value = 0
    remainder = max_weight
    for item in items:
        if remainder == 0:
            break
        nb_items = remainder // item[0]
        value += nb_items * item[1]
        remainder -= nb_items * item[0]
    return total_value


#Tests
coins = {0.01, 0.05, 0.10, 0.25, 1.00}
total = 1.47
print(make_change(coins, total))
