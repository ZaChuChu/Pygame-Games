import random
import pygame
from time import time
from pygame import Rect, draw

def main():

    cellWidth = 50
    cellHeight = cellWidth
    rows = 25
    cols = rows
    xMargin = cellWidth
    yMargin = cellHeight


    screenWidth = cellWidth * cols + 2 * xMargin
    screenHeight = cellHeight * rows + 2 * yMargin

    pygame.init()
    pygame.display.set_caption("One Who Runs Through Mazes")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    playerHeight = 40
    playerWidth = playerHeight
    playerColor = "blue"
    playerSpeed = max(int(cellHeight * .05), 1)
    playerStartX = 0
    playerStartY = 0

    player = Player(playerStartX, playerStartY, playerWidth, playerHeight, playerColor, playerSpeed, screenWidth, screenHeight)

    running = True
    gameOver = False
    startTime = time()

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        keys = pygame.key.get_pressed()
        if not gameOver:
            
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                pass
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                pass
            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                pass
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                pass

            if winCondition:
                endTime = time()
                gameOver = True

            screen.fill("orange")
            player.draw(screen)
            pygame.display.flip()
            clock.tick(60)
        
        else:
            textSurface = pygame.font.Font(size = 80).render("Game Over", True, "Dark Red")
            textX = (screen.get_width() - textSurface.get_width())/2
            textY = (screen.get_height() - textSurface.get_height())/2
            textBackground = pygame.Rect(textX - 10, textY - 10, textSurface.get_width() + 20 , textSurface.get_height() + 20)
            pygame.draw.rect(screen, "dark gray" , textBackground)
            pygame.draw.rect(screen, "black" , textBackground, 5)
            screen.blit(textSurface,(textX,textY))
            pygame.display.flip()

            if keys[pygame.K_SPACE]:
                startTime = time()
                gameOver = False
                player.moveTo(playerStartX, playerStartY)


if __name__ == "__main__": main()

        
if __name__ == "__main__": main()