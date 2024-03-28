from maze import Maze
from player import Player
import pygame
from time import time
from pygame import Rect, draw

def main():

    screenHeight = 1000

    wallLength = 50
    wallWidth = int(wallLength * .1)
    rows = 30
    cols = rows
    
    wallLength = max(screenHeight // (rows + 2), 1)
    wallWidth = max(int(wallLength / 8), 1)
    wallOffset = wallLength - wallWidth
    margin = wallOffset
    mazeHeight = wallOffset * rows + wallWidth
    mazeWidth = wallOffset * cols + wallWidth
  
    maze = Maze(rows, cols, wallLength, wallWidth, margin, margin)

    screenWidth = mazeWidth + 2 * margin
    screenHeight = mazeHeight  + 2 * margin

    pygame.init()
    pygame.display.set_caption("One Who Runs Through Mazes")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    playerHeight = int((wallOffset - wallWidth) * .65)
    playerWidth = playerHeight
    playerColor = "blue"
    playerSpeed = max(int(wallOffset * .05), 1)
    playerStartX = margin + wallWidth + wallOffset * maze.getEntrance() + (wallOffset - wallWidth - playerWidth) // 2
    playerStartY = margin + mazeHeight + (margin - playerHeight) // 2 - wallWidth

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
            posChange = [0, 0]
            boxLeft = player.getX()
            boxTop = player.getY()
            boxRight = boxLeft + playerWidth
            boxBottom = boxTop + playerHeight

            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                if not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                    boxRight += playerSpeed
                    posChange[0] = 1
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                boxLeft -= playerSpeed
                posChange[0] = -1

            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                if not keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    boxTop -= playerSpeed
                    posChange[1] = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                boxBottom += playerSpeed
                posChange[1] = 1

            boxLeft = min(max(boxLeft, margin), margin + mazeWidth)
            boxTop = min(max(boxTop, margin), margin + mazeHeight)
            boxRight = min(max(boxRight, margin), margin + mazeWidth)
            boxBottom = min(max(boxBottom, margin), margin + mazeHeight)
                
            if posChange[1] != 0:
                if posChange[1] < 0:
                    verticalBox = [boxLeft, boxTop, boxRight, player.getY() - 1] 
                else:
                    verticalBox = [boxLeft, player.getY() + playerHeight + 1, boxRight, boxBottom]
                verticalWalls = maze.getVerticalMovementWalls(*[val - margin for val in verticalBox], posChange[1])
            else:
                verticalWalls = []

            if posChange[0] != 0:
                if posChange[0] < 0:
                    horizontalBox = [boxLeft, boxTop, player.getX() - 1, boxBottom] 
                else:
                    horizontalBox = [player.getX() + playerWidth + 1, boxTop, boxRight, boxBottom]
                horizontalWalls = maze.getHorizontalMovementWalls(*[val - margin for val in horizontalBox], posChange[0])
            else:
                horizontalWalls = []

            if player.getY() >= margin + mazeHeight - playerSpeed:
                for rect in maze.getEntranceVerticals():
                    horizontalWalls.append(rect)
                verticalWalls.append(maze.getEntranceHorizontal())
            elif player.getY() <= margin + playerSpeed:
                for rect in maze.getExitVerticals():
                    horizontalWalls.append(rect)
                verticalWalls.append(maze.getExitHorizontal())

            player.movePlayer(posChange, [horizontalWalls, verticalWalls])

            if any([val != 0 for val in posChange]):
                maze.randomize(player.rect)
            
            if maze.winRect.contains(player.rect):
                endTime = time()
                gameOver = True

            screen.fill("orange")
            maze.draw(screen)
            player.draw(screen)
            pygame.display.flip()
            clock.tick(60)
        
        else:
            winText = pygame.font.Font(size = 80).render("You Solved The Maze!", True, "Green")
            totalTime = endTime - startTime
            if totalTime >= 60:
                timeText = pygame.font.Font(size = 60).render(f"Time: {round(totalTime // 60)}:{int(totalTime % 60)}", True, "Green")
            else:
                timeText = pygame.font.Font(size = 60).render(f"Time: {round(totalTime, 1)} seconds", True, "Green")
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