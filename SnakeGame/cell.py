from pygame import Rect, draw

class Cell:
    def __init__(self, x, y, cellSize, screen) -> None:
        self.x = x
        self.y = y
        self.rect = Rect(x*cellSize, y*cellSize, cellSize, cellSize)
        self.isSpecial = False
        self.isSnake = False
        self.color = "black"
        self.screen = screen

    def makeSnake(self):
        self.isSpecial = True
        self.isSnake = True
        self.color = "orange"

    def makeFood(self):
        self.isSpecial = True
        self.color = "red"

    def draw(self, screen):
        if self.isSpecial:
            draw.rect(screen, "dark " + self.color , self.rect)
        draw.rect(screen, self.color , self.rect, 2)

    def clear(self):
        self.isSnake = False
        self.isSpecial = False
        self.color = "black"