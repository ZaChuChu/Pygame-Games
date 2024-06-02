from pygame import draw, Rect

class Cell:
    def __init__(self, x, y, square_size, color, screen):
        self.rect = Rect(x, y, square_size, square_size)
        self.color = color
        self.screen = screen

    def setColor(self, color):
        self.color = color

    def draw(self):
        draw.rect(self.screen, self.color, self.rect)
