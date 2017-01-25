#Author: Remi Pelletier
#File:   rp_puzzles.py
#Desc.:  Module containing solutions to various puzzles.

import rp_bit_manip

#------------------------------N Queens Puzzle---------------------------------

def _can_place_queen(grid, row, col):
    for i in range(row):
        if grid[i] == col or (row - i) == abs(col - grid[i]): 
            return False
    return True

def _place_queen(grid, n, row):
    if row == n:
        return True
    for col in range(n):
        if _can_place_queen(grid, row, col):
            grid[row] = col
            if _place_queen(grid, n, row+1):
                return True
    return False

def _print_grid(grid):
    n = len(grid)
    line = '* ' * n
    for row in grid:
        print(line[:row*2] + 'Q ' + line[row*2:])

def n_queens(n):
    if n == 2 or n == 3:
        return None
    grid = [0  for _ in range(n)]
    success = _place_queen(grid, n, 0)
    return grid if success else None



#------------------------------Josephus Problem--------------------------------

def josephus_problem(n):
    return ((n ^ rp_bit_manip.highest_set_bit(n)) << 1) | 1



#Tests
#n = 13
#solution = n_queens(n)
#_print_grid(solution)

#print(josephus_problem(41))