from pygame import Rect, draw
from mazeGraph import MazeGraph
from math import ceil
from tile import Tile
import random

class Maze:

    def __init__(self, rows, cols, segmentLength, segmentWidth, xOffset, yOffset, screenWidth, screenHeight):
        self.rows = rows
        self.cols = cols
        self.segmentLength = segmentLength
        self.segmentWidth = segmentWidth
        self.segmentOffset = segmentLength - segmentWidth
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.mazeHeight = self.segmentWidth + self.rows * self.segmentOffset
        self.mazeWidth = self.segmentWidth + self.cols * self.segmentOffset
        self.width = segmentWidth + self.segmentOffset * cols
        self.height = segmentWidth + self.segmentOffset * rows
        self.background = Rect(xOffset, yOffset, self.width, self.height)
        self.graph = MazeGraph(self.rows, self.cols)
        self.maxTileRows = (screenHeight - 1) // self.segmentOffset + 2
        self.maxTileCols = (screenWidth - 1) // self.segmentOffset + 2
        self.verticalWallTiles = [[Tile(Rect(0, 0, self.segmentWidth, self.segmentLength)) for col in range(self.maxTileCols)] for row in range(self.maxTileRows)]
        self.horizontalWallTiles = [[Tile(Rect(0, 0, self.segmentLength, self.segmentWidth)) for col in range(self.maxTileCols)] for row in range(self.maxTileRows)]
        self.prevVerticalRowEnd = self.maxTileRows - 1
        self.prevVerticalColEnd = self.maxTileCols - 1
        self.prevHorizontalRowEnd = self.maxTileRows - 1
        self.prevHorizontalColEnd = self.maxTileCols - 1
        self.winTile = Tile(Rect(0, yOffset + segmentLength // 5 * 2, segmentLength // 5, segmentLength // 5))
        self.outLine = Rect(0, yOffset + segmentLength // 5 * 2 - 4, segmentLength // 5 + 8, segmentLength // 5 + 8)
        self.startMaze()

    def startMaze(self):
        self.graph.startGraph()
        self.lastPlayerRow = -1
        self.lastPlayerCol = -1
        self.entranceColumn = random.randint(0, self.cols - 1)
        self.exitColumn = random.randint(0, self.cols - 1)
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
        self.horizontalWalls = [[False for j in range(self.cols)] for i in range(self.rows + 1)]
        
        for row in [0, self.rows]:
            for col in range(0, self.cols):
                self.horizontalWalls[row][col] = True

        for (i, row) in enumerate(verticalAdjacencies):
            i += 1
            x = 0
            for edge in row:
                edgeX = edge.node1[1]
                for wallX in range(x, edgeX):
                    self.horizontalWalls[i][wallX] = True
                x = edgeX + 1
            for wallX in range(x, self.cols):
                    self.horizontalWalls[i][wallX] = True
                
        # Make list of vertical walls by column
        self.verticalWalls = [[False for j in range(self.cols + 1)] for i in range(self.rows)]

        for (i, row) in enumerate(horizontalAdjacencies):
            x = 0
            for edge in row:
                edgeX = edge.node2[1]
                for wallX in range(x, edgeX):
                    self.verticalWalls[i][wallX] = True
                x = edgeX + 1
            for wallX in range(x, self.cols + 1):
                    self.verticalWalls[i][wallX] = True
    
    def randomize(self, playerRelativeX, playerRelativeY, playerWidth, playerHeight):
        x = playerRelativeX % self.segmentOffset
        y = playerRelativeY % self.segmentOffset
        if x >= self.segmentWidth and x + playerWidth <= self.segmentOffset:
            if y >= self.segmentWidth and y + playerHeight <= self.segmentOffset:
                row = playerRelativeY // self.segmentOffset
                col = playerRelativeX // self.segmentOffset
                if row != self.lastPlayerRow or col != self.lastPlayerCol:
                    self.lastPlayerRow = row
                    self.lastPlayerCol = col
                    self.graph.randomizeGraph()
                    self.generateWalls()

    def getEntrance(self):
        return self.entranceColumn
    
    def draw(self, screen):
        draw.rect(screen, "White", self.background)
        for row in self.horizontalWallTiles:
            for wallObj in row:
                if wallObj.display:
                    draw.rect(screen, "black", wallObj.rect)

        for row in self.verticalWallTiles:
            for wallObj in row:
                if wallObj.display:
                    draw.rect(screen, "black", wallObj.rect)

        if self.winTile.display:
            draw.rect(screen, "green", self.winTile.rect)
            draw.rect(screen, "dark green", self.outLine, 4)

    def didWin(self, playerRect):
        if self.winTile.display:
            return playerRect.contains(self.winTile.rect)
 
    def getVerticalMovementWalls(self, left, top, right, bottom, direction):
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
        
        return self.getWalls(verticalRowStart, verticalRowEnd, verticalColStart, verticalColEnd, horizontalRowStart, horizontalRowEnd, horizontalColStart, horizontalColEnd)

    def getHorizontalMovementWalls(self, left, top, right, bottom, direction):
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
        
        return self.getWalls(verticalRowStart, verticalRowEnd, verticalColStart, verticalColEnd, horizontalRowStart, horizontalRowEnd, horizontalColStart, horizontalColEnd)
    
    def getWalls(self, movementRange, screenRanges):
        walls = []
        tileVerticalRowStart, tileVerticalColStart = self.getVerticalStarts(screenRanges[0], screenRanges[1])
        verticalRowStart, verticalColStart = self.getVerticalStarts(movementRange[0], movementRange[1])
        verticalRowEnd, verticalColEnd = self.getVerticalEnds(movementRange[2], movementRange[3])
        for row in range(verticalRowStart, verticalRowEnd + 1):
            for col in range(verticalColStart, verticalColEnd + 1):
                wall = self.verticalWallTiles[row - tileVerticalRowStart][col - tileVerticalColStart]
                if wall.display:
                    walls.append(wall.rect)
        
        tileHorizontalRowStart, tileHorizontalColStart = self.getHorizontalStarts(screenRanges[0], screenRanges[1])
        horizontalRowStart, horizontalColStart = self.getHorizontalStarts(movementRange[0], movementRange[1])
        horizontalRowEnd, horizontalColEnd = self.getHorizontalEnds(movementRange[2], movementRange[3])
        for row in range(horizontalRowStart, horizontalRowEnd + 1):
            for col in range(horizontalColStart, horizontalColEnd + 1):
                wall = self.horizontalWallTiles[row - tileHorizontalRowStart][col - tileHorizontalColStart]
                if wall.display:
                    walls.append(wall.rect)
        return walls
    
    def setWallTiles(self, screenLeft, screenTop, screenRight, screenBottom):
        verticalRowStart, verticalColStart = self.getVerticalStarts(screenLeft, screenTop)
        verticalRowEnd, verticalColEnd = self.getVerticalEnds(screenRight, screenBottom)
        for verticalRow in range(verticalRowStart, verticalRowEnd + 1):
            for verticalCol in range(verticalColStart, verticalColEnd + 1):
                wallObj = self.verticalWallTiles[verticalRow - verticalRowStart][verticalCol - verticalColStart]
                if self.verticalWalls[verticalRow][verticalCol]:
                    wallObj.display = True
                    wallObj.rect.x = verticalCol * self.segmentOffset + self.xOffset - screenLeft
                    wallObj.rect.y = verticalRow * self.segmentOffset + self.yOffset - screenTop               
                else:
                    wallObj.display = False

        for row in range(verticalRowEnd - verticalRowStart + 1, self.prevVerticalRowEnd + 1):
            for col in range(self.prevVerticalColEnd + 1):
                self.verticalWallTiles[row][col].display = False

        for col in range(verticalColEnd - verticalColStart + 1, self.prevVerticalColEnd + 1):
            for row in range(self.prevVerticalRowEnd + 1):
                self.verticalWallTiles[row][col].display = False

        self.prevVerticalRowEnd = verticalRowEnd - verticalRowStart
        self.prevVerticalColEnd = verticalColEnd - verticalColStart

        horizontalRowStart, horizontalColStart = self.getHorizontalStarts(screenLeft, screenTop)
        horizontalRowEnd, horizontalColEnd = self.getHorizontalEnds(screenRight, screenBottom)

        for horizontalRow in range(horizontalRowStart, horizontalRowEnd + 1):
            for horizontalCol in range(horizontalColStart, horizontalColEnd + 1):
                wallObj = self.horizontalWallTiles[horizontalRow - horizontalRowStart][horizontalCol - horizontalColStart]
                if self.horizontalWalls[horizontalRow][horizontalCol]:
                    wallObj.display = True
                    wallObj.rect.x = horizontalCol * self.segmentOffset + self.xOffset - screenLeft
                    wallObj.rect.y = horizontalRow * self.segmentOffset + self.yOffset - screenTop                    
                else:
                    wallObj.display = False
                    
        for row in range(horizontalRowEnd - horizontalRowStart + 1, self.prevHorizontalRowEnd + 1):
            for col in range(self.maxTileCols):
                self.horizontalWallTiles[row][col].display = False

        for col in range(horizontalColEnd - horizontalColStart + 1, self.prevHorizontalColEnd + 1):
            for row in range(self.maxTileRows):
                self.horizontalWallTiles[row][col].display = False

        self.prevHorizontalRowEnd = horizontalRowEnd - horizontalRowStart
        self.prevHorizontalColEnd = horizontalColEnd - horizontalColStart

        if horizontalRowStart == 0 and verticalColStart <= self.exitColumn <= verticalColEnd:
            self.winTile.display = True
            self.winTile.rect.x = self.exitColumn  * self.segmentOffset + self.segmentLength // 5 * 2 + self.xOffset - screenLeft
            self.winTile.rect.y = self.yOffset + self.segmentLength // 5 * 2 - screenTop
            self.outLine.x = self.exitColumn  * self.segmentOffset + self.segmentLength // 5 * 2 - 4 + self.xOffset - screenLeft
            self.outLine.y = self.yOffset + self.segmentLength // 5 * 2 - screenTop - 4
        else:
            self.winTile.display = False


        self.background.x = max(0, self.xOffset - screenLeft)
        self.background.y = max(0, self.yOffset - screenTop)
        self.background.width = min(self.screenWidth, self.mazeWidth + self.xOffset - screenLeft)
        self.background.height = min(self.screenHeight, self.mazeHeight + self.yOffset - screenTop)      
  
    def getVerticalStarts(self, left, top):
        verticalRowStart = max(0, (top - self.yOffset - self.segmentWidth) // self.segmentOffset)
        verticalColStart = max(0, (left - self.xOffset) // self.segmentOffset)
        return verticalRowStart, verticalColStart

    def getVerticalEnds(self, right, bottom):
        verticalRowEnd = min(self.rows - 1, (bottom - self.yOffset) // self.segmentOffset)
        verticalColEnd = min(self.cols, (right - self.xOffset) // self.segmentOffset)
        return verticalRowEnd, verticalColEnd

    def getHorizontalStarts(self, left, top):
        horizontalRowStart = max(0, (top - self.yOffset) // self.segmentOffset)
        horizontalColStart = max(0, (left - self.segmentWidth - self.xOffset) // self.segmentOffset)
        return horizontalRowStart, horizontalColStart

    def getHorizontalEnds(self, right, bottom):
        horizontalRowEnd = min(self.rows, (bottom - self.yOffset) // self.segmentOffset)
        horizontalColEnd = min(self.cols - 1, (right - self.xOffset) // self.segmentOffset)
        return horizontalRowEnd, horizontalColEnd
