from pygame import draw

class Piece:
    def __init__(self, color, rimColor, direction, radius):
        self.color = color
        self.rimColor = rimColor
        self.direction = direction
        self.isKing = False
        self.radius = radius

    def draw(self, screen, x, y):
        draw.circle(screen, self.color, (x, y), self.radius)
        draw.circle(screen, self.rimColor, (x, y), self.radius, 5)
        if self.isKing:
            draw.circle(screen, self.rimColor, (x, y), int(self.radius * .5) , 5)
