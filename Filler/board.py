from cell import Cell
from color_group import ColorGroup
from pygame import draw, Rect
from random import choice

class Board:
    def __init__(self, rows, cols, square_size, xOffset, yOffset, colors, screen):
        height = rows * square_size
        width = cols * square_size
        self.border_width = min(height, width) // 50
        self.border_rect = Rect(xOffset - self.border_width, yOffset - self.border_width, width + 2 * self.border_width, height + 2 * self.border_width)
        self.screen = screen

        y_range = range(yOffset, yOffset + rows * square_size, square_size)
        x_range = range(xOffset, xOffset + cols * square_size, square_size)
        self.cells = [[Cell(x, y, square_size, choice(colors), screen) for x in x_range] for y in y_range]
        initial_sets = [[ColorGroup(cell, cell.color, colors) for cell in row] for row in self.cells]
        
        num_players = 2
        self.player_groups = [None for _ in range(num_players)]
        self.player_index = 0
        self.next_player_func = lambda index : (index + 1) % num_players

        if initial_sets[0][cols - 1].color == initial_sets[rows - 1][0].color:
            valid_colors = list(set(colors).difference([initial_sets[0][cols - 1].color]))
            initial_sets[rows - 1][0].claimColor(choice(valid_colors))
        
        for row in range(rows):
            for col in range(cols - 1):
                initial_sets[row][col] = initial_sets[row][col].union(initial_sets[row][col + 1])

        for row in range(rows - 1):
            for col in range(cols):
                initial_sets[row][col] = initial_sets[row][col].union(initial_sets[row + 1][col])

        self.player_groups[0] = initial_sets[0][cols - 1]
        self.player_groups[1] = initial_sets[rows - 1][0]

    def draw(self):
        draw.rect(self.screen, "black", self.border_rect, self.border_width)
        for row in self.cells:
            for cell in row:
                cell.draw()
        
    def getColors(self):
        return [colorGroup.color for colorGroup in self.player_groups]

    def changeColor(self, color):
        old_color = self.player_groups[self.player_index].color
        self.player_groups[self.player_index].claimColor(color)
        print(f"Player #{self.player_index} ref size: {self.player_groups[self.player_index].refSize()}")
        self.player_index = self.next_player_func(self.player_index)
        return old_color