import pygame
from board import Board

def main():
    squareSize = 50
    rowCount = 8
    colCount = rowCount
    boardHeight = squareSize * rowCount
    boardWidth = squareSize * colCount
    offset = 25
    headingHeight = 50
    if boardHeight > 1080 - 2 * offset - headingHeight:
        boardHeight = (1080 - 2 * offset - headingHeight) // rowCount * rowCount
        squareSize = boardHeight // rowCount
        boardWidth = squareSize * colCount
    if boardWidth > 1920 - 2 * offset - headingHeight:
        boardWidth = (1920 - 2 * offset - headingHeight )// colCount * colCount
        squareSize = boardWidth // colCount
        boardHeight = squareSize * colCount
    pygame.init()
    screen = pygame.display.set_mode((boardWidth + 2 * offset, boardHeight + 2 * offset))
    clock = pygame.time.Clock()
    running = True
    gameBoard = Board(rowCount, colCount, offset, offset, boardWidth, boardHeight)
    mousePressed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # screen.fill("light green")
        if pygame.mouse.get_pressed()[0]:
            if not mousePressed:
                coordinates = pygame.mouse.get_pos()

                if onBoard(coordinates, offset, boardWidth, boardHeight):
                    gameBoard.clickCell(*coordinates)
                mousePressed = True
        else:
            mousePressed = False
        gameBoard.draw(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

def onBoard(coordinates, offset, boardWidth, boardHeight):
    limits = [boardWidth, boardHeight]
    for i in range(2):
        if not (offset <= coordinates[i] and limits[i] + offset > coordinates[i]):
            return False
    return True

if __name__ == "__main__": main()