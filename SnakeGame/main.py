from cell import Cell
from snake import Snake
from pygame import Color
import pygame
import random

def main():
    height = 21
    width = 21
    cellLength = 20

    pygame.init()
    screen = pygame.display.set_mode((width * cellLength, height * cellLength))
    clock = pygame.time.Clock()

    running = True

    while running:
        cells = []
        for row in range(height):
            cells.append([])
            for col in range(width):
                cells[row].append(Cell(col, row, cellLength, screen))
        gameOver = False
        snakeySnake = Snake(cells[height//2][width//2], 0)
        random.choice(filterCells(cells)).makeFood()
        
        while not gameOver and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and snakeySnake.direction != 2:
                snakeySnake.setDirection(0)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN] and snakeySnake.direction != 0:
                snakeySnake.setDirection(2)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] and snakeySnake.direction != 3:
                snakeySnake.setDirection(1)
            elif keys[pygame.K_a] or keys[pygame.K_LEFT] and snakeySnake.direction != 1:
                snakeySnake.setDirection(3)
            
            if snakeySnake.direction % 2 == 0:
                if snakeySnake.direction > 1:
                    yChange = 1
                else:
                    yChange = -1
                xChange = 0
            else:
                if snakeySnake.direction > 1:
                    xChange = -1
                else:
                    xChange = 1
                yChange = 0

            newX = (snakeySnake.head.cell.x + xChange)
            newY = (snakeySnake.head.cell.y + yChange)

            if between(newX, 0 , width - 1) and between(newY, 0, height - 1):        
                newHead = cells[newY][newX]

                if newHead.isSpecial:
                    if newHead.isSnake:
                        gameOver = True
                    else:
                        snakeySnake.addSegment(newHead)
                        random.choice(filterCells(cells)).makeFood()
                else:
                    snakeySnake.move(newHead)
            else: 
                gameOver = True

            if gameOver:
                textSurface = pygame.font.Font(size = 80).render("Game Over", True, "Dark Red")
                textX = (screen.get_width() - textSurface.get_width())/2
                textY = (screen.get_height() - textSurface.get_height())/2
                textBackground = pygame.Rect(textX - 10, textY - 10, textSurface.get_width() + 20 , textSurface.get_height() + 20)
                pygame.draw.rect(screen, "dark gray" , textBackground)
                pygame.draw.rect(screen, "black" , textBackground, 5)
                screen.blit(textSurface,(textX,textY))
                pygame.display.flip()
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break
                    if keys[pygame.K_SPACE]:
                        break   
            else:
                screen.fill("dark green")
                for row in cells:
                    for cell in row:
                        cell.draw(screen)
                pygame.display.flip()
            clock.tick(10)
    pygame.quit()

def between(value, min, max):
    return min <= value and value <= max

def filterCells(cells):
    filtered = []
    for row in cells:
        for cell in row:
            if not cell.isSpecial:
                filtered.append(cell)
    return filtered
if __name__ == "__main__": main()