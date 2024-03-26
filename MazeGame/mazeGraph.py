from node import Node
import random
from edge import Edge, mstSort
from functools import cmp_to_key

class MazeGraph:
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.generateEdges()

    def generateEdges(self):
        self.edges = []
        edgeCount = ((self.rows - 1) * self.cols + (self.cols - 1 ) * self.rows) * 2

        for row in range(self.rows):
            for col in range(self.cols - 1):
                self.edges.append(Edge([row, col], [row, col + 1], random.randint(1, edgeCount * 3)))

        for col in range(self.cols):
            for row in range(self.rows - 1):
                self.edges.append(Edge([row, col], [row + 1, col], random.randint(1, edgeCount * 3)))
                
        self.edges.sort()

    def getMST(self):
        mst = []
        i = 0
        counted = 0

        while len(self.nodes[0][0].parent.set) < (self.rows * self.cols):
            edge = self.edges[i]
            y1, x1 = edge.node1
            y2, x2 = edge.node2
            if self.nodes[y1][x1].union(self.nodes[y2][x2]):
                mst.append(edge)
            i += 1

        mst.sort(key=cmp_to_key(mstSort))
        return mst