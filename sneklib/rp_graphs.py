#Author: Remi Pelletier
#File:   rp_graphs.py
#Desc.:  Module containing various functions
#        and classes related to graph theory.

import heapq
import sys
import rp_data_structures


#Counts the number of different vertices in the given list of edges.
def count_vertices(edges_list):
    return max(max(edge.v1, edge.v2) for edge in edges_list) - min(min(edge.v1, edge.v2) for edge in edges_list) + 1


#Class used to represent an edge.
class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


#Class used to represent a vertex.
class Vertex:
    def __init__(self, id, neighbors={}):
        self.id = id
        self.neighbors = neighbors


#Data structure used to represent a disjoint set.
class DisjointSet:
    def __init__(self, size):
        self.tree = [-1 for _ in range(size)]
        self.nb_trees = size

    def find(self, val):
        if self.tree[val] < 0:
            return val
        else:
            self.tree[val] = self.find(self.tree[val])
            return self.tree[val]

    def are_in_same_set(self, val1, val2):
        return self.find(val1) == self.find(val2)

    def union(self, val1, val2):
        root1 = self.find(val1)
        root2 = self.find(val2)

        if root1 == root2:
            return
        
        if self.tree[root2] < self.tree[root1]:
            self.tree[root1] = root2
        else:
            if self.tree[root1] == self.tree[root2]:
                self.tree[root1] -= 1
            self.tree[root2] = root1 

        self.nb_trees -= 1



#----------------------------Minimum spanning tree-----------------------------

#Finds the mininum spanning tree and returns it
#along with the sum of all it's edges' weight.
def kruskal(edges_list, nb_vertices=None, pre_sorted=False):
    if nb_vertices is None:
        nb_vertices = count_vertices(edges_list)

    disjoint_set = DisjointSet(nb_vertices)

    if not pre_sorted:
        edges_list.sort(key=lambda e: e.weight)

    mst = []
    total_weight = 0

    for edge in edges_list:
        if disjoint_set.nb_trees == 1:
            break

        if not disjoint_set.are_in_same_set(edge.v1, edge.v2):
            disjoint_set.union(edge.v1, edge.v2)
            mst.append(edge)
            total_weight += edge.weight

    return mst, total_weight