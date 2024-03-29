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
        self.tiles = [[Tile(Rect(0, 0, cellWidth, cellHeight), Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))) for col in range(cols)] for row in range(rows)]
        # self.tiles = [[Tile(Rect(0, 0, cellWidth, cellHeight), "black" if (col + row) % 2 else "white") for col in range(cols)] for row in range(rows)]
        self.prevRowStart = 0
        self.prevRowEnd = rows - 1
        self.prevColStart = 0 
        self.prevColEnd = cols - 1

    def setTiles(self, screenLeft, screenTop, screenRight, screenBottom):
        tilesColStart = max((screenLeft - self.xOffset) // self.cellWidth, 0)
        tilesColEnd = min((screenRight - self.xOffset) // self.cellWidth, self.cols - 1)

        tilesRowStart = max((screenTop - self.yOffset) // self.cellHeight, 0)
        tilesRowEnd = min((screenBottom - self.yOffset) // self.cellHeight, self.rows - 1)

        for row in range(tilesRowStart, tilesRowEnd + 1):
            for col in range(tilesColStart, tilesColEnd + 1):
                self.tiles[row][col].rect.x = col * self.cellWidth + self.xOffset - screenLeft
                self.tiles[row][col].rect.y = row * self.cellHeight + self.yOffset - screenTop
                self.tiles[row][col].display = True
        
        for rowRange in [range(self.prevRowStart, tilesRowStart), range(tilesRowEnd + 1, self.prevRowEnd + 1)]:
            for row in rowRange:
                for col in range(self.prevColStart, self.prevColEnd + 1):
                    self.tiles[row][col].display = False

        for colRange in [range(self.prevColStart, tilesColStart), range(tilesColEnd + 1, self.prevColEnd + 1)]:
            for col in colRange:
                for row in range(self.prevRowStart, self.prevRowEnd + 1):
                    self.tiles[row][col].display = False
        
        self.prevRowStart = tilesRowStart
        self.prevRowEnd = tilesRowEnd
        self.prevColStart = tilesColStart
        self.prevColEnd = tilesColEnd


    def draw(self, screen):
        for row in self.tiles:
            for tileObj in row:
                if tileObj.display:
                    draw.rect(screen, tileObj.color, tileObj.rect)
    