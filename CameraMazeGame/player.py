from pygame import Rect, draw, Color

class Player:
    def __init__(self, x, y, width, height, screenWidth, screenHeight, xOffset, yOffset, maxX, maxY, speed, color):
        self.relativeX = x
        self.relativeY = y
        self.speed = speed
        self.height = height
        self.width = width
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.maxX = maxX
        self.maxY = maxY
        self.setConstraints()
        self.rect = Rect(0, 0, width, height)
        self.screenTop = 0
        self.screenLeft = 0
        self.screenRight = 0
        self.screenBottom = 0
        self.setRectXPos()
        self.setRectYPos()
        self.color = color
        self.borderColor = "dark " + color

    def setConstraints(self):
        self.centerScreenX = (self.screenWidth - self.width) // 2
        self.centerScreenY = (self.screenHeight - self.height) // 2
        self.lowerXBound = self.centerScreenX - self.xOffset
        self.lowerYBound = self.centerScreenY - self.yOffset
        self.upperXBound = self.maxX - (self.centerScreenX - self.xOffset + self.width)
        self.upperYBound = self.maxY - (self.centerScreenY - self.yOffset + self.height)

    def movePlayer(self, xChange, yChange, horizontalWalls, verticalWalls):
        testRect = self.rect.copy()
        for i in range(self.speed):
            if xChange:
                potRect = testRect.move(xChange, 0)
                if potRect.collidelist(horizontalWalls) == -1:
                    self.relativeX += xChange
                    testRect = potRect
            if yChange:
                potRect = testRect.move(0, yChange)
                if potRect.collidelist(verticalWalls) == -1:
                    self.relativeY += yChange
                    testRect= potRect

        if xChange:
            self.relativeX = max(0, min(self.relativeX, self.maxX - self.width))
            self.setRectXPos()

        if yChange:
            self.relativeY = max(0, min(self.relativeY, self.maxY - self.height))
            self.setRectYPos()
                
    def moveTo(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY

    def setRectXPos(self):
        if self.relativeX < self.lowerXBound:
            self.rect.x = self.relativeX + self.xOffset
            self.screenLeft = 0
            self.screenRight = self.screenWidth

        elif self.relativeX > self.upperXBound:
            self.rect.x = self.centerScreenX + self.relativeX - self.upperXBound
            self.screenRight = self.maxX + 2 * self.xOffset
            self.screenLeft = self.screenRight - self.screenWidth

        else:
            self.rect.x = self.centerScreenX
            self.screenLeft = self.relativeX - self.centerScreenX + self.xOffset
            self.screenRight = self.screenLeft + self.screenWidth
        
    def setRectYPos(self):
        if self.relativeY < self.lowerYBound:
            self.rect.y = self.relativeY + self.yOffset            
            self.screenTop = 0
            self.screenBottom = self.screenHeight

        elif self.relativeY > self.upperYBound:
            self.rect.y = self.relativeY - self.upperYBound + self.centerScreenY        
            self.screenBottom = self.maxY + 2 * self.yOffset
            self.screenTop = self.screenBottom - self.screenHeight     
            
        else:
            self.rect.y = self.centerScreenY            
            self.screenTop = self.relativeY - self.centerScreenY + self.yOffset
            self.screenBottom = self.screenTop + self.screenHeight

    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y
    
    def absoluteScreenEdges(self):
        return [self.screenLeft, self.screenTop, self.screenRight, self.screenBottom]
    
    def draw(self, screen):
         draw.rect(screen, self.color , self.rect)
         draw.rect(screen, self.borderColor, self.rect, 5)

    def playerRandomizeInfo(self):
        return [self.relativeX, self.relativeY, self.width, self.height]
    
    def getMovementRanges(self, xChange, yChange):
        if xChange < 0:
            verticalLeft = max(self.relativeX - self.speed, 0)
            verticalRight = self.relativeX + self.width
            horizontalLeft = max(self.relativeX - self.speed, 0)
            horizontalRight = self.relativeX
        elif xChange > 0:
            verticalLeft = self.relativeX 
            verticalRight = min(self.relativeX + self.width + self.speed, self.maxX)
            horizontalLeft = self.relativeX + self.width
            horizontalRight = min(self.relativeX + self.width + self.speed, self.maxX)
        else:
            verticalLeft = self.relativeX
            verticalRight = self.relativeX + self.width
            horizontalLeft = self.relativeX
            horizontalRight = self.relativeX
    
        if yChange < 0:
            verticalTop = max(self.relativeY - self.speed, 0)
            verticalBottom = self.relativeY
            horizontalTop = max(self.relativeY - self.speed, 0)
            horizontalBottom = self.relativeY + self.height
        elif yChange > 0:
            verticalTop = self.relativeY + self.height
            verticalBottom = min(self.relativeY + self.height + self.speed, self.maxY)
            horizontalTop = self.relativeY
            horizontalBottom = min(self.relativeY + self.height + self.speed, self.maxY)
        else:
            verticalTop = self.relativeY
            verticalBottom = self.relativeY
            horizontalTop = self.relativeY
            horizontalBottom = self.relativeY + self.height

        return [
            [horizontalLeft + self.xOffset, horizontalTop + self.yOffset, horizontalRight + self.xOffset, horizontalBottom + self.yOffset],
            [verticalLeft + self.xOffset, verticalTop + self.yOffset, verticalRight + self.xOffset, verticalBottom + self.yOffset]
        ]
