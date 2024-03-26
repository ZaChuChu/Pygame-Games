from maze import Maze
from player import Player
import pygame

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
        margin = wallLength
        wallOffset = wallLength - wallWidth
        mazeHeight = wallOffset * rows + wallWidth
        mazeWidth = wallOffset * cols + wallWidth
    
    maze = Maze(rows, cols, wallLength, wallWidth, margin, margin)

    pygame.init()
    screen = pygame.display.set_mode((mazeWidth + 2 * margin, mazeHeight  + 2 * margin))
    clock = pygame.time.Clock()

    playerHeight = int((wallOffset - wallWidth) * .65)
    playerWidth = playerHeight
    playerColor = "dark grey"
    playerSpeed = 5

    player = Player(margin + wallWidth + wallOffset * maze.getEntrance() + (wallOffset - wallWidth - playerWidth)// 2, margin + mazeHeight + (margin - playerHeight) // 2, playerWidth, playerHeight, playerColor, playerSpeed, margin * 2 + mazeWidth, margin * 2 + mazeHeight)

    

    running = True

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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

            verticalWalls = maze.getVerticalMovementWalls(*[val - margin for val in verticalBox], posChange[1])
            horizontalWalls = maze.getHorizontalMovementWalls(*[val - margin for val in horizontalBox], posChange[0])

        else:
            verticalWalls = []
            horizontalWalls = []

        player.movePlayer(posChange, [horizontalWalls, verticalWalls])

        screen.fill("orange")
        maze.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__": main()