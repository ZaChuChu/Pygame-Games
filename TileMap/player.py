from pygame import Rect, draw, Color

class Player:
    def __init__(self, x, y, width, height, screenWidth, xOffset, maxX, screenHeight, yOffset, maxY, color):
        self.relativeX = x
        self.relativeY = y
        self.height = height
        self.width = width
        self.screenWidth = screenWidth
        self.xOffset = xOffset
        self.maxX = maxX
        self.screenHeight = screenHeight
        self.yOffset = yOffset
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
        self.borderColor = Color(50, 50, 50)

    def setConstraints(self):
        self.centerScreenX = (self.screenWidth - self.width) // 2
        self.centerScreenY = (self.screenHeight - self.height) // 2
        self.lowerXBound = self.centerScreenX - self.xOffset
        self.lowerYBound = self.centerScreenY - self.yOffset
        self.upperXBound = self.maxX - (self.centerScreenX - self.xOffset + self.width)
        self.upperYBound = self.maxY - (self.centerScreenY - self.yOffset + self.height)

    def movePlayer(self, xChange, yChange):
        xChange = max(-self.relativeX, min(xChange, self.maxX - (self.relativeX + self.width)))
        if xChange:
            self.relativeX += xChange
            self.setRectXPos()

        yChange = max(-self.relativeY, min(yChange, self.maxY - (self.relativeY + self.height)))
        if yChange:
            self.relativeY += yChange
            self.setRectYPos()

    def setRectXPos(self):
        if self.relativeX < self.lowerXBound:
            self.rect.x = self.relativeX + self.xOffset
            self.screenLeft = 0
            self.screenRight = self.screenWidth

        elif self.relativeX > self.upperXBound:
            self.rect.x = self.centerScreenX + (self.relativeX - self.upperXBound)
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
    
    def absoluteScreenEdges(self):
        return [self.screenLeft, self.screenTop, self.screenRight, self.screenBottom]
    
    def draw(self, screen):
         draw.rect(screen, self.color , self.rect)
         draw.rect(screen, self.borderColor, self.rect, 5)