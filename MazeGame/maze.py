from pygame import Rect, draw
from mazeGraph import MazeGraph
import random

class Maze:

    def __init__(self, rows, cols, segmentLength, segmentWidth, xOffset, yOffset):
        self.rows = rows
        self.cols = cols
        self.segmentLength = segmentLength
        self.segmentWidth = segmentWidth
        self.segmentOffset = segmentLength - segmentWidth
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = segmentWidth + self.segmentOffset * cols
        self.height = segmentWidth + self.segmentOffset * rows
        self.background = Rect(xOffset, yOffset, self.width, self.height)

        # Generate Graph
        self.graph = MazeGraph(rows, cols)
        self.generateMaze()
    
    def generateMaze(self):
        self.entranceColumn = random.randint(0, self.cols - 1)
        self.exitColumn = random.randint(0, self.cols - 1)

        exitLeftBorder = self.xOffset + self.segmentOffset * self.exitColumn
        self.exitBorderRects = [Rect(exitLeftBorder, 0, self.segmentWidth, self.yOffset), 
                                Rect(exitLeftBorder + self.segmentLength - self.segmentWidth, 0, self.segmentWidth, self.yOffset), 
                                Rect(exitLeftBorder, 0, self.segmentLength, self.segmentWidth)]

        self.winRect = Rect(exitLeftBorder + self.segmentWidth, self.segmentWidth, self.segmentOffset - self.segmentWidth, self.yOffset - self.segmentWidth)

        enterLeftBorder = self.xOffset + self.segmentOffset * self.entranceColumn
        self.enterBorderRects = [Rect(enterLeftBorder, self.height + self.yOffset, self.segmentWidth, self.yOffset), 
                                 Rect(enterLeftBorder + self.segmentLength - self.segmentWidth, self.height + self.yOffset, self.segmentWidth, self.yOffset), 
                                 Rect(enterLeftBorder, self.height + self.yOffset * 2 - self.segmentWidth, self.segmentLength, self.segmentWidth)]
        self.generateWalls()

    def generateWalls(self):
        mst = self.graph.getMST()

        horizontalAdjacencies = [[] for i in range(self.cols - 1)]
        verticalAdjacencies = [[] for i in range(self.rows - 1)]
        for edge in mst:
            if edge.node1[0] == edge.node2[0]:
                horizontalAdjacencies[edge.node1[1]].append(edge)
            else:
                verticalAdjacencies[edge.node1[0]].append(edge)

        # Make list of horizontal walls by row
        self.horizontalWalls = [[None for j in range(self.cols)] for i in range(self.rows + 1)]
        
        for row, col in [[0, self.exitColumn], [self.rows, self.entranceColumn]]:
            for i in range(0, self.cols):
                self.horizontalWalls[row][i] = Rect(i * self.segmentOffset + self.xOffset, row * self.segmentOffset + self.yOffset, self.segmentLength, self.segmentWidth)
            self.horizontalWalls[row][col] = None

        for (i, row) in enumerate(verticalAdjacencies):
            i += 1
            x = 0
            for edge in row:
                edgeX = edge.node1[1]
                for wallX in range(x, edgeX):
                    self.horizontalWalls[i][wallX] = Rect(wallX * self.segmentOffset + self.xOffset, i * self.segmentOffset + self.yOffset, self.segmentLength, self.segmentWidth)
                x = edgeX + 1
            for wallX in range(x, self.cols):
                    self.horizontalWalls[i][wallX] = Rect(wallX * self.segmentOffset + self.xOffset, i * self.segmentOffset + self.yOffset, self.segmentLength, self.segmentWidth)
                
        # Make list of vertical walls by column
        self.verticalWalls = [[None for j in range(self.rows)] for i in range(self.cols + 1)]

        for index in [0, self.cols]:
            for i in range(self.rows):
                self.verticalWalls[index][i] = Rect(index * self.segmentOffset + self.xOffset, i * self.segmentOffset + self.yOffset, self.segmentWidth, self.segmentLength)

        for (i, row) in enumerate(horizontalAdjacencies):
            i += 1
            y = 0
            for edge in row:
                edgeY = edge.node1[0]
                for wallY in range(y, edgeY):
                    self.verticalWalls[i][wallY] = Rect(i * self.segmentOffset + self.xOffset, wallY * self.segmentOffset + self.yOffset, self.segmentWidth, self.segmentLength)
                y = edgeY + 1
            for wallY in range(y, self.rows):
                    self.verticalWalls[i][wallY] = Rect(i * self.segmentOffset + self.xOffset, wallY * self.segmentOffset + self.yOffset, self.segmentWidth, self.segmentLength)

    def getEntrance(self):
        return self.entranceColumn
    
    def getEntranceBorders(self):
        return self.enterBorderRects
    
    def getExitBorders(self):
        return self.exitBorderRects
    
    def draw(self, screen):
        draw.rect(screen, "White", self.background)

        for row in self.horizontalWalls:
            for wall in row:
                if wall is not None:
                    draw.rect(screen, "black", wall)

        for row in self.verticalWalls:
            for wall in row:
                if wall is not None:
                    draw.rect(screen, "black", wall)

        for wallSet in [self.enterBorderRects, self.exitBorderRects]:
            for wall in wallSet:
                draw.rect(screen, "black", wall)

        draw.rect(screen, "green", self.winRect)
 
    def getVerticalMovementWalls(self, left, top, right, bottom, direction):
        walls = []
       
        if direction < 0 and top % self.segmentOffset < self.segmentWidth and top > self.segmentWidth:
            verticalColStart = (top // self.segmentOffset) - 1
        else:
            verticalColStart = top // self.segmentOffset
        verticalColEnd = bottom // self.segmentOffset

        verticalRowStart = max(left // self.segmentOffset, 0)
        verticalRowEnd = min(right // self.segmentOffset, self.cols)

        if left % self.segmentOffset < self.segmentWidth and left > self.segmentWidth:
            horizontalColStart = left // self.segmentOffset - 1
        else:
            horizontalColStart = left // self.segmentOffset
        horizontalColEnd = right // self.segmentOffset

        horizontalRowStart = max(top // self.segmentOffset, 0)
        horizontalRowEnd = min(bottom // self.segmentOffset, self.rows)

        verticalColStart = max(verticalColStart, 0)
        verticalColEnd = min(verticalColEnd, self.rows - 1)

        for row in range(verticalRowStart, verticalRowEnd + 1):
            for col in range(verticalColStart, verticalColEnd + 1):
                wall = self.verticalWalls[row][col]
                if wall is not None:
                    walls.append(wall)

        horizontalColStart = max(horizontalColStart, 0)
        horizontalColEnd = min(horizontalColEnd, self.cols - 1)

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

        horizontalRowStart = max(top // self.segmentOffset, 0)
        horizontalRowEnd = min(bottom // self.segmentOffset, self.rows)

        if top % self.segmentOffset < self.segmentWidth and top > self.segmentWidth:
            verticalColStart = top // self.segmentOffset - 1
        else:
            verticalColStart = top // self.segmentOffset
        verticalColEnd = bottom // self.segmentOffset

        verticalRowStart = max(left // self.segmentOffset, 0)
        verticalRowEnd = min(right // self.segmentOffset, self.cols)

        horizontalColStart = max(horizontalColStart, 0)
        horizontalColEnd = min(horizontalColEnd, self.cols - 1)
        verticalColStart = max(verticalColStart, 0)
        verticalColEnd = min(verticalColEnd, self.rows - 1)

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
