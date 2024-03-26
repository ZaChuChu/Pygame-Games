from maze import Maze
from player import Player
import pygame
from pygame import Rect, draw

def main():

    wallLength = 50
    wallWidth = int(wallLength * .1)
    rows = 25
    cols = rows
    margin = wallLength
    wallOffset = wallLength - wallWidth
    mazeHeight = wallOffset * rows + wallWidth
    mazeWidth = wallOffset * cols + wallWidth
    if mazeHeight + 2 * margin > 1080:
        wallLength = 1080 // (rows + 2)
        wallOffset = wallLength - wallWidth
        margin = wallOffset
        mazeHeight = wallOffset * rows + wallWidth
        mazeWidth = wallOffset * cols + wallWidth
    
    maze = Maze(rows, cols, wallLength, wallWidth, margin, margin)

    screenWidth = mazeWidth + 2 * margin
    screenHeight = mazeHeight  + 2 * margin

    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    playerHeight = int((wallOffset - wallWidth) * .65)
    playerWidth = playerHeight
    playerColor = "dark grey"
    playerSpeed = int(wallOffset * .1)
    playerStartX = margin + wallWidth + wallOffset * maze.getEntrance() + (wallOffset - wallWidth - playerWidth) // 2
    playerStartY = margin + mazeHeight + (margin - playerHeight) // 2

    player = Player(playerStartX, playerStartY, playerWidth, playerHeight, playerColor, playerSpeed, screenWidth, screenHeight)

    running = True
    gameOver = False

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        if not gameOver:
            keys = pygame.key.get_pressed()
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
            
            if boxBottom - boxTop != 0 and boxLeft - boxRight != 0:
                if posChange[1] < 0:
                    verticalBox = [boxLeft, boxTop, boxRight, player.getY() - 1] 
                else:
                    verticalBox = [boxLeft, player.getY() + playerHeight + 1, boxRight, boxBottom]

                if posChange[0] < 0:
                    horizontalBox = [boxLeft, boxTop, player.getX() - 1, boxBottom] 
                else:
                    horizontalBox = [player.getX() + playerWidth + 1, boxTop, boxRight, boxBottom]
                    
                if posChange[1] != 0:
                    verticalWalls = maze.getVerticalMovementWalls(*[val - margin for val in verticalBox], posChange[1])
                else:
                    verticalWalls = []

                if posChange[0] != 0:
                    horizontalWalls = maze.getHorizontalMovementWalls(*[val - margin for val in horizontalBox], posChange[0])
                else:
                    horizontalWalls = []

            else:
                verticalWalls = []
                horizontalWalls = []

            if player.getY() > margin + mazeHeight:
                for rect in maze.getEntranceBorders():
                    horizontalWalls.append(rect)
            elif player.getY() < margin:
                for rect in maze.getExitBorders():
                    horizontalWalls.append(rect)

            player.movePlayer(posChange, [horizontalWalls, verticalWalls])
            
            if maze.winRect.contains(player.rect):
                gameOver = True

            screen.fill("orange")
            maze.draw(screen)
            player.draw(screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__": main()