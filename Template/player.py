from pygame import Rect, draw

class Player:
    def __init__(self, x, y, width, height, color, speed, maxX, MaxY):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.maxX = maxX
        self.maxY = MaxY

    def movePlayer(self):
        if self.rect.right > self.maxX:
            self.rect.right = self.maxX
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.maxY:
            self.rect.bottom = self.maxY
        elif self.rect.top < 0:
            self.rect.top = 0
                
    def moveTo(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY

    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y

    def draw(self, screen):
         draw.rect(screen, self.color , self.rect)