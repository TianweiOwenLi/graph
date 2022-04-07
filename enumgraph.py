import collections as ds
from functools import reduce
from copy import deepcopy

# EnumGraph is a class that represents undirected enumerable graphs. 
# Functionalities include generic graph search algorithms, edge addition 
# and deletion, as well as tree-specific functions like converting to /from 
# prufer encoding. Note that vertices non-negative integers.

class EnumGraph:

    def __init__(self,E):

        try:
            maxval, minval = reduce(max, map(max, E)), reduce(min, map(min, E))
        except TypeError as t:
            raise ValueError("invalid val in edge container:", repr(t))

        if(minval < 0):
            raise ValueError("negative vertices not allowed")

        n = maxval + 1
        self.vdict = {i : set() for i in range(n)}
        self.V = set()

        for (a,b) in E:
            self.V.add(a)
            self.V.add(b)
            self.vdict[a].add(b)
            self.vdict[b].add(a)

        self.vdict = {i : list(self.vdict[i]) for i in self.vdict}

    def __str__(self): # can be modified
        return str(self.vdict)

    def __repr__(self):
        return repr(self.vdict)

    def __eq__(self, g):
        return self.vdict == g.vdict

    # W: O(|s|) where s is the set of vertices at most 2-edges away from i
    def removeV(self, i):
        neighbors, self.vdict[i] = self.vdict[i], []
        self.V.remove(i)

        # can be optimized
        for n in neighbors:
            self.vdict[n] = list(filter(lambda x: x != i, self.vdict[n]))

    def removeE(self, edge):
        pass

    def addE(self, edge):
        pass

    def genericDFS(self, visit, revisit, finish):
        pass

    def dfsAll(self, gendfs):
        pass

    # W: O(n^2)
    # destructive
    def destructiveToPrufer(self):
        if len(self.V) <= 2: 
            return []

        leaves = list(filter(lambda i: len(self.vdict[i]) == 1, self.vdict))

        if not len(leaves):
            raise Exception("non-tree graph has no prufer code")

        minLeaf = leaves[0]
        parent = self.vdict[minLeaf] # leaves have unique parent
        self.removeV(minLeaf);
        return parent + self.destructiveToPrufer()

    # W: O(n^2)
    def toPrufer(self):
        return deepcopy(self).destructiveToPrufer()

    # W: O(n^2)
    @staticmethod
    def fromPrufer(code):
        n = 2 + len(code);
        s = set(range(n))
        if(max(s) < max(code)):
            raise ValueError("vertices too large")
        w = deepcopy(code)
        E = ds.deque() # a dequeue of edges
        while len(w):
            minLeaf = min(filter(lambda x: x not in w, s))
            parent = w[0]
            E.append((minLeaf,parent))
            s.remove(minLeaf)
            w = w[1:]

        # join last two vertices
        E.append(tuple(s))

        return EnumGraph(E);
