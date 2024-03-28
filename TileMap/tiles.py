import random
import math
from tile import Tile
from pygame import draw, Color, Rect

class Tiles:
    def __init__(self, rows, cols, cellWidth, cellHeight, xOffset, yOffset, screenWidth, screenHeight):
        self.rows = rows
        self.cols = cols
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.totalWidth = cols * cellWidth
        self.totalHeight = rows * cellHeight
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileColors = [[Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for col in range(cols)] for row in range(rows)]
        self.tiles = [[Tile(Rect(0, 0, cellWidth, cellHeight), self.tileColors[row][col]) for col in range(cols)] for row in range(rows)]
        self.prevRowStart = 0
        self.prevRowEnd = 0
        self.prevColStart = 0 
        self.prevColEnd = 0
        self.outLine = Rect(0,0,0,0)

    def setTiles(self, screenLeft, screenTop, screenRight, screenBottom):
        self.outLine.x = screenLeft
        self.outLine.y = screenTop
        self.outLine.width = screenRight - screenLeft
        self.outLine.height = screenBottom - screenTop
        tilesColStart = max((screenLeft - self.xOffset) // self.cellWidth, 0)
        tilesColEnd = min((screenRight - self.xOffset) // self.cellWidth, self.cols - 1)

        tilesRowStart = max((screenTop - self.yOffset) // self.cellHeight, 0)
        tilesRowEnd = min((screenBottom - self.yOffset) // self.cellHeight, self.rows - 1)

        for row in range(tilesRowStart, tilesRowEnd + 1):
            for col in range(tilesColStart, tilesColEnd + 1):
                self.tiles[row][col].rect.x = col * self.cellWidth + self.xOffset - screenLeft
                self.tiles[row][col].rect.y = row * self.cellHeight + self.yOffset - screenTop
                self.tiles[row][col].display = True
        
        for rowRange in [range(0, tilesRowStart), range(tilesRowEnd + 1, self.rows)]:
            for row in rowRange:
                for col in range(self.cols):
                    self.tiles[row][col].display = False

        for colRange in [range(0, tilesColStart), range(tilesColEnd + 1, self.cols)]:
            for col in colRange:
                for row in range(self.rows):
                    self.tiles[row][col].display = False

    def draw(self, screen):
        for row in self.tiles:
            for tileObj in row:
                if tileObj.display:
                    draw.rect(screen, tileObj.color, tileObj.rect)
        draw.rect(screen, "red", self.outLine, 5)
    