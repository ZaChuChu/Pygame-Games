import pygame
from board import Board
from color_selector import ColorSelector

def main():
    rows = 10
    cols = rows
    square_size = 50
    
    x_offset = 50
    y_offset = x_offset
    
    border_width = (min(rows, cols) * square_size) // 50
    board_width = cols * square_size + 2 * border_width
    board_height = rows * square_size + 2 * border_width
    screen_width = x_offset * 2 + board_width
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    selector_size = min(screen_width // len(colors), 100)
    screen_height = y_offset + board_height + selector_size

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True

    board = Board(rows, cols, square_size, x_offset + border_width, y_offset + border_width, colors, screen)
    select_margin = (screen_width - selector_size * len(colors)) // 2
    select_func = lambda i : ColorSelector(i * selector_size + select_margin, y_offset + board_height, selector_size, colors[i], screen)
    color_selectors = {colors[i]:select_func(i) for i in range(len(colors))}
    
    for color in board.getColors():
        color_selectors[color].select()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > screen_height - selector_size:
                    for color in color_selectors:
                        if color_selectors[color].tryClick(pos):
                            old_color = board.changeColor(color)
                            color_selectors[old_color].unselect()
                            break
                           
        screen.fill("white")
        board.draw()
        for selector in color_selectors.values():
            selector.draw()
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__": main()