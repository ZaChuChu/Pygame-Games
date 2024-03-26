from node import Node
from edge import Edge, mstSort
from functools import cmp_to_key
import math
from pygame import Rect, draw
import random

class Maze:

    def __init__(self, rows, cols, segmentLength, segmentWidth, xOffset, yOffset):
        self.rows = rows
        self.cols = cols
        self.segmentLength = segmentLength
        self.segmentWidth = segmentWidth
        self.segmentOffset = segmentLength - segmentWidth

        # Generate Graph
        nodes = [[Node(row, col) for col in range(cols)] for row in range(rows)]
        self.entranceColumn = random.randint(0, cols-1)
        exitColumn = random.randint(0, cols-1)
        edges = []
        edgeCount = ((rows - 1) * cols + (cols - 1 ) * rows) * 2
        for row in range(rows):
            for col in range(cols - 1):
                edges.append(Edge([row, col], [row, col + 1], random.randint(1, edgeCount * 3)))
        for col in range(cols):
            for row in range(rows - 1):
                edges.append(Edge([row, col], [row + 1, col], random.randint(1, edgeCount * 3)))

        edges.sort()

        # Generate MST
        mst = []
        i = 0
        counted = 0

        while len(nodes[0][0].parent.set) < (rows * cols):
            edge = edges[i]
            y1, x1 = edge.node1
            y2, x2 = edge.node2
            if nodes[y1][x1].union(nodes[y2][x2]):
                mst.append(edge)
            i += 1

        mst.sort(key=cmp_to_key(mstSort))

        horizontalAdjacencies = [[] for i in range(cols-1)]
        verticalAdjacencies = [[] for i in range(rows-1)]
        for edge in mst:
            if edge.node1[0] == edge.node2[0]:
                horizontalAdjacencies[edge.node1[1]].append(edge)
            else:
                verticalAdjacencies[edge.node1[0]].append(edge)

        # Make list of horizontal walls by row
        self.horizontalWalls = [[None for j in range(cols)] for i in range(rows + 1)]
        
        for row, col in [[0, exitColumn], [rows, self.entranceColumn]]:
            for i in range(0, cols):
                self.horizontalWalls[row][i] = Rect(i * self.segmentOffset + xOffset, row * self.segmentOffset + yOffset, segmentLength, segmentWidth)
            self.horizontalWalls[row][col] = None

        for (i, row) in enumerate(verticalAdjacencies):
            i += 1
            x = 0
            for edge in row:
                edgeX = edge.node1[1]
                for wallX in range(x, edgeX):
                    self.horizontalWalls[i][wallX] = Rect(wallX * self.segmentOffset + xOffset, i * self.segmentOffset + yOffset, segmentLength, segmentWidth)
                x = edgeX + 1
            for wallX in range(x, cols):
                    self.horizontalWalls[i][wallX] = Rect(wallX * self.segmentOffset + xOffset, i * self.segmentOffset + yOffset, segmentLength, segmentWidth)
                
        # Make list of vertical walls by column
        self.verticalWalls = [[None for j in range(rows+1)] for i in range(cols + 1)]

        for index in [0, cols]:
            for i in range(rows):
                self.verticalWalls[index][i] = Rect(index * self.segmentOffset + xOffset, i * self.segmentOffset + yOffset, segmentWidth, segmentLength)

        for (i, row) in enumerate(horizontalAdjacencies):
            i += 1
            y = 0
            for edge in row:
                edgeY = edge.node1[0]
                for wallY in range(y, edgeY):
                    self.verticalWalls[i][wallY] = Rect(i * self.segmentOffset + xOffset, wallY * self.segmentOffset + yOffset, segmentWidth, segmentLength)
                y = edgeY + 1
            for wallY in range(y, rows):
                    self.verticalWalls[i][wallY] = Rect(i * self.segmentOffset + xOffset, wallY * self.segmentOffset + yOffset, segmentWidth, segmentLength)


    def getEntrance(self):
        return self.entranceColumn
    
    
    def draw(self, screen):
        for row in self.horizontalWalls:
            for wall in row:
                if wall is not None:
                    draw.rect(screen, "black", wall)

        for row in self.verticalWalls:
            for wall in row:
                if wall is not None:
                    draw.rect(screen, "black", wall)
 
    def getVerticalMovementWalls(self, left, top, right, bottom, direction):
        walls = []
       
        if direction < 0 and top % self.segmentOffset < self.segmentWidth and top > self.segmentWidth:
            verticalRowStart = (top // self.segmentOffset) - 1
        else:
            verticalRowStart = top // self.segmentOffset
        verticalRowEnd = bottom // self.segmentOffset
        
        verticalColStart = left // self.segmentOffset
        verticalColEnd = right // self.segmentOffset

        if left % self.segmentOffset < self.segmentWidth and left > self.segmentWidth:
            horizontalColStart = left // self.segmentOffset - 1
        else:
            horizontalColStart = left // self.segmentOffset
        horizontalColEnd = right // self.segmentOffset

        horizontalRowStart = top // self.segmentOffset
        horizontalRowEnd = bottom // self.segmentOffset

        for row in range(verticalRowStart, verticalRowEnd + 1):
            for col in range(verticalColStart, verticalColEnd + 1):
                wall = self.verticalWalls[col][row]
                if wall is not None:
                    walls.append(wall)

        for row in range(horizontalRowStart, horizontalRowEnd + 1):
            for col in range(horizontalColStart, horizontalColEnd + 1):
                wall = self.horizontalWalls[row][col]
                if wall is not None:
                    walls.append(wall)
        
        return walls

    def getHorizontalMovementWalls(self, left, top, right, bottom, direction):

        walls = []
        if direction < 0 and left % self.segmentOffset < self.segmentWidth and left > self.segmentWidth:
            horizontalColStart = (left // self.segmentOffset) - 1
        else:
            horizontalColStart = left // self.segmentOffset
        horizontalColEnd = right // self.segmentOffset

        horizontalRowStart = top // self.segmentOffset
        horizontalRowEnd = bottom // self.segmentOffset

        if top % self.segmentOffset < self.segmentWidth and top > self.segmentWidth:
            verticalColStart = top // self.segmentOffset - 1
        else:
            verticalColStart = top // self.segmentOffset
        verticalColEnd = bottom // self.segmentOffset

        verticalRowStart = left // self.segmentOffset
        verticalRowEnd = right // self.segmentOffset

        for row in range(horizontalRowStart, horizontalRowEnd + 1):
            for col in range(horizontalColStart, horizontalColEnd + 1):
                wall = self.horizontalWalls[row][col]
                if wall is not None:
                    walls.append(wall)

        for row in range(verticalRowStart, verticalRowEnd + 1):
            for col in range(verticalColStart, verticalColEnd + 1):
                wall = self.verticalWalls[row][col]
                if wall is not None:
                    walls.append(wall)
        
        return walls
