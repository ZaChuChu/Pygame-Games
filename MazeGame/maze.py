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
        self.graph = MazeGraph(self.rows, self.cols)
        self.startMaze()

    def startMaze(self):
        self.graph.startGraph()
        self.lastPlayerRow = -1
        self.lastPlayerCol = -1
        self.entranceColumn = random.randint(0, self.cols - 1)
        self.exitColumn = random.randint(0, self.cols - 1)

        enterLeftBorder = self.xOffset + self.segmentOffset * self.entranceColumn
        self.enterBorderVerticals = [Rect(enterLeftBorder, self.height + self.yOffset, self.segmentWidth, self.yOffset), Rect(enterLeftBorder + self.segmentLength - self.segmentWidth, self.height + self.yOffset, self.segmentWidth, self.yOffset)]
        self.enterBorderHorizontal = Rect(enterLeftBorder, self.height + self.yOffset * 2 - self.segmentWidth, self.segmentLength, self.segmentWidth)

        exitLeftBorder = self.xOffset + self.segmentOffset * self.exitColumn
        self.exitBorderVerticals = [Rect(exitLeftBorder, 0, self.segmentWidth, self.yOffset), Rect(exitLeftBorder + self.segmentLength - self.segmentWidth, 0, self.segmentWidth, self.yOffset)]
        self.exitBorderHorizontal = Rect(exitLeftBorder, 0, self.segmentLength, self.segmentWidth)

        self.winRect = Rect(exitLeftBorder + self.segmentWidth, self.segmentWidth, self.segmentOffset - self.segmentWidth, self.yOffset - self.segmentWidth)
        self.startRect = Rect(enterLeftBorder + self.segmentWidth,  self.height + self.yOffset, self.segmentOffset - self.segmentWidth, self.yOffset - self.segmentWidth )

        self.generateWalls()

    def generateWalls(self):
        mst = self.graph.getMST()
        horizontalAdjacencies = [[] for i in range(self.rows)]
        verticalAdjacencies = [[] for i in range(self.rows - 1)]
        for edge in mst:
            if edge.node1[0] == edge.node2[0]:
                horizontalAdjacencies[edge.node1[0]].append(edge)
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
        self.verticalWalls = [[None for j in range(self.cols + 1)] for i in range(self.rows)]

        for (i, row) in enumerate(horizontalAdjacencies):
            x = 0
            for edge in row:
                edgeX = edge.node2[1]
                for wallX in range(x, edgeX):
                    self.verticalWalls[i][wallX] = Rect(wallX * self.segmentOffset + self.xOffset, i * self.segmentOffset + self.yOffset, self.segmentWidth, self.segmentLength)
                x = edgeX + 1
            for wallX in range(x, self.cols + 1):
                    self.verticalWalls[i][wallX] = Rect(wallX * self.segmentOffset + self.xOffset, i * self.segmentOffset + self.yOffset, self.segmentWidth, self.segmentLength)

    def randomize(self, playerRect):
        x = (playerRect.x - self.xOffset) % self.segmentOffset
        y = (playerRect.y - self.yOffset) % self.segmentOffset
        if x >= self.segmentWidth and x + playerRect.width <= self.segmentOffset:
            if y >= self.segmentWidth and y + playerRect.height <= self.segmentOffset:
                row = (playerRect.y - self.yOffset) // self.segmentOffset
                col = (playerRect.x - self.xOffset) // self.segmentOffset
                if row != self.lastPlayerRow or col != self.lastPlayerCol:
                    self.lastPlayerRow = row
                    self.lastPlayerCol = col
                    self.graph.randomizeGraph()
                    self.generateWalls()

    def getEntrance(self):
        return self.entranceColumn
    
    def getEntranceVerticals(self):
        return self.enterBorderVerticals
    
    def getEntranceHorizontal(self):
        return self.enterBorderHorizontal
    
    def getExitVerticals(self):
        return self.exitBorderVerticals
    
    def getExitHorizontal(self):
        return self.exitBorderHorizontal
    
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

        for wallSet in [self.enterBorderVerticals, self.exitBorderVerticals]:
            for wall in wallSet:
                draw.rect(screen, "black", wall)

        draw.rect(screen, "black", self.exitBorderHorizontal)
        draw.rect(screen, "black", self.enterBorderHorizontal)
        draw.rect(screen, "white", self.startRect)
        draw.rect(screen, "green", self.winRect)
 
    def getVerticalMovementWalls(self, left, top, right, bottom, direction):
        walls = []
       
        if direction < 0 and top % self.segmentOffset < self.segmentWidth and top > self.segmentOffset:
            verticalRowStart = (top // self.segmentOffset) - 1
        else:
            verticalRowStart = top // self.segmentOffset

        verticalRowStart = max(verticalRowStart, 0)
        verticalRowEnd = min(bottom // self.segmentOffset, self.rows - 1)

        verticalColStart = max(left // self.segmentOffset, 0)
        verticalColEnd = min(right // self.segmentOffset, self.cols)

        if left % self.segmentOffset < self.segmentWidth and left > self.segmentWidth:
            horizontalColStart = left // self.segmentOffset - 1
        else:
            horizontalColStart = left // self.segmentOffset

        horizontalColStart = max(horizontalColStart, 0)
        horizontalColEnd = min(right // self.segmentOffset, self.cols - 1)

        horizontalRowStart = max(top // self.segmentOffset, 0)
        horizontalRowEnd = min(bottom // self.segmentOffset, self.rows)

        for row in range(verticalRowStart, verticalRowEnd + 1):
            for col in range(verticalColStart, verticalColEnd + 1):
                wall = self.verticalWalls[row][col]
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

        horizontalColStart = max(horizontalColStart, 0)
        horizontalColEnd = min(right // self.segmentOffset, self.cols - 1)

        horizontalRowStart = max(top // self.segmentOffset, 0)
        horizontalRowEnd = min(bottom // self.segmentOffset, self.rows)

        if top % self.segmentOffset < self.segmentWidth and top > self.segmentOffset:
            verticalRowStart = top // self.segmentOffset - 1
        else:
            verticalRowStart = top // self.segmentOffset

        verticalRowStart = max(verticalRowStart, 0)
        verticalRowEnd = min(bottom // self.segmentOffset, self.rows - 1)

        verticalColStart = max(left // self.segmentOffset, 0)
        verticalColEnd = min(right // self.segmentOffset, self.cols)

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
