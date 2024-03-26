from pygame import Rect, draw

class Player:
    def __init__(self, x, y, width, height, color, speed, maxX, MaxY):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.maxX = maxX
        self.maxY = MaxY

    def movePlayer(self, posChange, walls):
        for i in range(self.speed):
            if posChange[0]:
                potRect = self.rect.move(posChange[0], 0)
                if potRect.collidelist(walls[0]) == -1:
                    self.rect = potRect
            if posChange[1]:
                potRect = self.rect.move(0, posChange[1])
                if potRect.collidelist(walls[1]) == -1:
                    self.rect = potRect

        if self.rect.right > self.maxX:
            self.rect.right = self.maxX
        elif self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.bottom > self.maxY:
            self.rect.bottom = self.maxY
        elif self.rect.top < 0:
            self.rect.top = 0
                

    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y

    def checkTop(self, wall):
        self.rect.top = max(self.rect.top, wall.bottom + 1)

    def checkLeft(self, wall):
        self.rect.left = max(self.rect.left, wall.right + 1)

    def checkBottom(self, wall):
        self.rect.bottom = min(self.rect.bottom, wall.top - 1)

    def checkRight(self, wall):
        self.rect.right = min(self.rect.right, wall.left - 1)

    def draw(self, screen):
         draw.rect(screen, self.color , self.rect)