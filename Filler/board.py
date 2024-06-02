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
        
        set_references = [[i * cols + j for j in range(cols)] for i in range(rows)]

        get_reference = lambda index, array: array[index // cols][index % cols]
        
        find_actaul_index = lambda index : index if index == get_reference(index, set_references) else find_actaul_index(get_reference(index, set_references))
                 
        num_players = 2
        self.player_groups = [None for _ in range(num_players)]
        self.player_index = 0
        self.next_player_func = lambda index : (index + 1) % num_players
        
        if initial_sets[0][cols - 1].color == initial_sets[rows - 1][0].color:
            valid_colors = list(set(colors).difference([initial_sets[0][cols - 1].color]))
            initial_sets[rows - 1][0].claimColor(choice(valid_colors))
        
        for row in range(rows):
            for col in range(cols - 1):
                main_group = get_reference(find_actaul_index(row * cols + col), initial_sets)
                other_group = get_reference(find_actaul_index(row * cols + col + 1), initial_sets)
                if main_group != other_group:
                    if main_group.color == other_group.color:
                        main_group.merge(other_group)
                        set_references[row][col + 1] = row * cols + col
                    else:
                        main_group.createReference(other_group)

        for row in range(rows - 1):
            for col in range(cols):
                main_group = get_reference(find_actaul_index(row * cols + col), initial_sets)
                other_group = get_reference(find_actaul_index((row + 1) * cols + col), initial_sets)
                if main_group != other_group:
                    if main_group.color == other_group.color:
                        main_group.merge(other_group)
                        set_references[row + 1][col] = row * cols + col
                    else:
                        main_group.createReference(other_group)

        self.player_groups[0] = get_reference(find_actaul_index(cols - 1), initial_sets)
        self.player_groups[1] = get_reference(find_actaul_index((rows - 1) * cols), initial_sets)
        
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
        self.player_index = self.next_player_func(self.player_index)
        return old_color