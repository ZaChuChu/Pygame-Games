from pygame import draw, Rect

class ColorSelector:
    def __init__(self, x, y, square_size, color, screen) -> None:
        self.selected = False
        unselected_size = int(square_size * .8)
        unselected_margin = (square_size - unselected_size) // 2
        self.unselected_rect = Rect(x + unselected_margin, y + unselected_margin, unselected_size, unselected_size)
        selected_size = (unselected_size * 3) // 4 
        selected_margin = (square_size - selected_size) // 2
        self.selected_rect = Rect(x + selected_margin, y + selected_margin, selected_size, selected_size)
        self.color = color
        self.screen = screen
        
    def select(self):
        self.selected = True
        
    def unselect(self):
        self.selected = False
                
    def tryClick(self, pos):
        if not self.selected:
            if self.unselected_rect.collidepoint(pos):
                self.select()
                return True
        return False
        
    def isSelected(self):
        return self.selected
    
    def draw(self):
        draw.rect(self.screen, self.color, self.selected_rect if self.selected else self.unselected_rect)