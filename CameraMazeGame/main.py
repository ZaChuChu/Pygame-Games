from maze import Maze
from player import Player
import pygame
from time import time
from pygame import Rect, draw

def main():

    screenHeight = 500
    screenWidth = 500

    wallLength = 50
    wallWidth = int(wallLength * .1)
    rows = 30
    cols = rows
    wallOffset = wallLength - wallWidth
    margin = wallOffset
    xOffset = margin
    yOffset = xOffset
    mazeHeight = wallOffset * rows + wallWidth
    mazeWidth = wallOffset * cols + wallWidth
  
    maze = Maze(rows, cols, wallLength, wallWidth, margin, margin, screenWidth, screenHeight)

    pygame.init()
    pygame.display.set_caption("One Who Runs Through Mazes")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    playerHeight = int((wallOffset - wallWidth) * .65)
    playerWidth = playerHeight
    playerColor = "blue"
    playerSpeed = wallOffset // 15
    maxX = mazeWidth
    maxY = mazeHeight
    playerStartX = wallWidth + maze.getEntrance() * wallOffset + (wallOffset - wallWidth - playerWidth) // 2
    playerStartY = mazeHeight - wallOffset + (wallOffset - wallWidth - playerHeight) // 2

    player = Player(playerStartX, playerStartY, playerWidth, playerHeight, screenWidth, screenHeight, xOffset, yOffset, maxX, maxY, playerSpeed, playerColor)
    
    running = True
    gameOver = False
    startTime = time()
    maze.setWallTiles(*player.absoluteScreenEdges())

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        keys = pygame.key.get_pressed()
        if not gameOver:
            xChange = 0
            yChange = 0
            boxLeft = player.getX()
            boxTop = player.getY()
            boxRight = boxLeft + playerWidth
            boxBottom = boxTop + playerHeight

            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                if not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                    boxRight += playerSpeed
                    xChange = 1
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                boxLeft -= playerSpeed
                xChange = -1

            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                if not keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    boxTop -= playerSpeed
                    yChange = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                boxBottom += playerSpeed
                yChange = 1

            boxLeft = min(max(boxLeft, margin), margin + mazeWidth)
            boxTop = min(max(boxTop, margin), margin + mazeHeight)
            boxRight = min(max(boxRight, margin), margin + mazeWidth)
            boxBottom = min(max(boxBottom, margin), margin + mazeHeight)
                
            # if yChange != 0:
            #     if yChange < 0:
            #         verticalBox = [boxLeft, boxTop, boxRight, player.getY() - 1] 
            #     else:
            #         verticalBox = [boxLeft, player.getY() + playerHeight + 1, boxRight, boxBottom]
            #     verticalWalls = maze.getVerticalMovementWalls(*[val - margin for val in verticalBox], yChange)
            # else:
            verticalWalls = []

            # if xChange != 0:
            #     if xChange < 0:
            #         horizontalBox = [boxLeft, boxTop, player.getX() - 1, boxBottom] 
            #     else:
            #         horizontalBox = [player.getX() + playerWidth + 1, boxTop, boxRight, boxBottom]
            #     horizontalWalls = maze.getHorizontalMovementWalls(*[val - margin for val in horizontalBox], yChange)
            # else:
            horizontalWalls = []
            

            if xChange or yChange:
                player.movePlayer(xChange, yChange, horizontalWalls, verticalWalls)
                maze.randomize(*player.playerRandomizeInfo())
                maze.setWallTiles(*player.absoluteScreenEdges())

            screen.fill("orange")
            maze.draw(screen)
            player.draw(screen)
            pygame.display.flip()
            clock.tick(60)
        
        else:
            winText = pygame.font.Font(size = 80).render("You Solved The Maze!", True, "Green")
            totalTime = endTime - startTime
            timeText = pygame.font.Font(size = 60).render(f"Time: {round(totalTime // 60)}:"+f"{int(totalTime % 60)}".zfill(2), True, "Green")
            playText = pygame.font.Font(size = 40).render("(Press Space to play again)", True, "Green")
            winX = (screenWidth - winText.get_width()) // 2
            timeX = (screenWidth - timeText.get_width()) // 2
            playX = (screenWidth - playText.get_width()) // 2
            winY = (screenHeight - winText.get_height()) // 2
            timeY = winY + winText.get_height() + 5
            playY = timeY + timeText.get_height() + 5
            textBackground = pygame.Rect(winX - 15, winY - 15, winText.get_width() + 30, winText.get_height() + playText.get_height() + timeText.get_height() + 40)
            pygame.draw.rect(screen, "dark gray" , textBackground)
            pygame.draw.rect(screen, "black" , textBackground, 5)
            screen.blit(winText, (winX, winY))
            screen.blit(timeText, (timeX, timeY))
            screen.blit(playText, (playX, playY))
            pygame.display.flip()
            if keys[pygame.K_SPACE]:
                startTime = time()
                gameOver = False
                maze.startMaze()
                playerStartX = margin + wallWidth + wallOffset * maze.getEntrance() + (wallOffset - wallWidth - playerWidth) // 2
                player.moveTo(playerStartX, playerStartY)


if __name__ == "__main__": main()