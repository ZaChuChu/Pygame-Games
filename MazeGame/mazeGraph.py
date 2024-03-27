from node import Node
import random
from edge import Edge, mstSort
from functools import cmp_to_key

class MazeGraph:
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.edgeCount = ((self.rows - 1) * self.cols + (self.cols - 1 ) * self.rows)
        self.maxWeight = self.edgeCount * 4

    def startGraph(self):
        for row in self.nodes:
            for node in row:
                node.parent = node
                node.set = [node]

        self.edges = []

        for row in range(self.rows):
            for col in range(self.cols - 1):
                self.edges.append(Edge([row, col], [row, col + 1], random.randint(1, self.maxWeight)))

        for col in range(self.cols):
            for row in range(self.rows - 1):
                self.edges.append(Edge([row, col], [row + 1, col], random.randint(1, self.maxWeight)))
                
        self.edges.sort()

        self.generateMST()

    def clearNodes(self):
        for row in self.nodes:
            for node in row:
                node.parent = node
                node.set = [node]

    def generateMST(self):
        self.mst = []
        i = 0
        while len(self.nodes[0][0].parent.set) < (self.rows * self.cols):
            edge = self.edges[i]
            y1, x1 = edge.node1
            y2, x2 = edge.node2
            if self.nodes[y1][x1].union(self.nodes[y2][x2]):
                self.mst.append(edge)
            i += 1

        self.mst.sort(key=cmp_to_key(mstSort))
    
    def getMST(self):
        return self.mst

    def randomizeGraph(self):
        self.clearNodes()
        
        random.shuffle(self.mst)

        lowerPercent = .01
        upperPercent = .03

        for edge in self.mst[:random.randint(int(self.edgeCount * lowerPercent), int(self.edgeCount * upperPercent))]:
            edge.weight = random.randint(1, self.maxWeight)
        
        for edge in self.edges[self.edgeCount - (max(self.rows, self.cols) // 4):]:
            edge.weight = random.randint(1, self.maxWeight)

        self.edges.sort()

        self.generateMST()