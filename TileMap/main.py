import random
import pygame
from time import time
from tiles import Tiles
from player import Player
from pygame import Rect, draw

def main():

    cellWidth = 100
    cellHeight = cellWidth
    cols = 10
    rows = 10
    xMargin = cellWidth
    yMargin = cellHeight

    screenWidth = 500
    screenHeight = 500
    tilesObj = Tiles(rows, cols, cellWidth, cellHeight, xMargin, yMargin, screenWidth, screenHeight)

    pygame.init()
    pygame.display.set_caption("One Who Runs Through Mazes")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    playerHeight = 50
    playerWidth = playerHeight
    playerColor = "White"
    playerSpeed = 5
    playerMaxX = cols * cellWidth
    playerMaxY = rows * cellHeight
    playerStartX = (playerMaxX - playerWidth) // 2
    playerStartY = (playerMaxY - playerHeight) // 2
    # playerStartX = 0
    # playerStartY = 0

    player = Player(playerStartX, playerStartY, playerWidth, playerHeight, screenWidth, xMargin, playerMaxX, screenHeight, yMargin, playerMaxY, playerColor)
                
    tilesObj.setTiles(*player.absoluteScreenEdges())

    running = True
    gameOver = False
    startTime = time()

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        keys = pygame.key.get_pressed()
        if not gameOver:
            
            xChange = 0
            yChange = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                xChange -= playerSpeed
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                xChange += playerSpeed
            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                yChange -= playerSpeed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                yChange += playerSpeed

            if xChange or yChange:
                player.movePlayer(xChange, yChange)
                tilesObj.setTiles(*player.absoluteScreenEdges())

            screen.fill("orange")
            draw.rect(screen, "Black", Rect(0, 0, screenWidth, screenHeight), xMargin)
            tilesObj.draw(screen)
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