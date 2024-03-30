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
        self.maxTileCols = screenWidth // cellWidth + 2
        self.maxTileRows = screenHeight // cellHeight + 2 
        self.tiles = [[Tile(Rect(0, 0, cellWidth, cellHeight), None) for col in range(self.maxTileCols)] for row in range(self.maxTileRows)]
        self.prevRowEnd = 0
        self.prevColEnd = 0

    def setTiles(self, screenLeft, screenTop, screenRight, screenBottom):
        tilesColStart = max((screenLeft - self.xOffset) // self.cellWidth, 0)
        tilesColEnd = min((screenRight - self.xOffset) // self.cellWidth, self.cols - 1)
        tilesRowStart = max((screenTop - self.yOffset) // self.cellHeight, 0)
        tilesRowEnd = min((screenBottom - self.yOffset) // self.cellHeight, self.rows - 1)
        for row in range(tilesRowStart, tilesRowEnd + 1):
            for col in range(tilesColStart, tilesColEnd + 1):
                colIndex = col - tilesColStart
                rowIndex = row - tilesRowStart
                tileObj = self.tiles[rowIndex][colIndex]
                tileObj.rect.x = col * self.cellWidth + self.xOffset - screenLeft
                tileObj.rect.y = row * self.cellHeight + self.yOffset - screenTop
                tileObj.color = self.tileColors[row][col]
                tileObj.display = True

        for row in range(tilesRowEnd - tilesRowStart + 1, self.prevRowEnd + 1):
            for col in range(self.maxTileCols):
                self.tiles[row][col].display = False

        for col in range(tilesColEnd - tilesColStart + 1, self.prevColEnd + 1):
            for row in range(self.maxTileRows):
                self.tiles[row][col].display = False

        self.prevRowEnd = tilesRowEnd - tilesRowStart
        self.prevColEnd = tilesColEnd - tilesColStart


    def draw(self, screen):
        for row in self.tiles:
            for tileObj in row:
                if tileObj.display:
                    draw.rect(screen, tileObj.color, tileObj.rect)
    