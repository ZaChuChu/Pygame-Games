from cell import Cell
from piece import Piece
from pygame import Rect, draw, Color

class Board:
    def __init__(self, rows, cols, x, y, width, height):
        self.cellHeight = height // rows
        self.cellWidth = width // cols
        self.border = Rect(0, 0, width + 50, height + 50)
        self.x = x
        self.y = y
        self.playerColors = ["red", Color(70, 70, 70)]
        self.rows = rows
        self.cols = cols
        self.makeBoard()


    def makeBoard(self):
        self.grid = []
        colors = ["black", "white"]
        pieceRows = (self.rows * 3) // 8
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                self.grid[row].append(Cell(colors[(row + col) % 2], self.cellHeight, self.cellWidth, row, col, self.x, self.y))
        radius = int(self.cellHeight * .85) // 2
        for row in range(pieceRows):
            for col in range(self.cols // 2):
                self.grid[row][col * 2 + row % 2].piece = Piece("red", "dark red", 1, radius)
        for row in range(self.rows - pieceRows, self.rows):
            for col in range(self.cols // 2):
                self.grid[row][col * 2 + row % 2].piece = Piece(Color(70, 70, 70), "dark gray", -1, radius)
        self.selectedCell = None
        self.nextMoves = []
        self.player = 0
    
    def clickCell(self, xPos, yPos):
        selectCell = self.grid[(yPos - self.y) // self.cellHeight][(xPos - self.x) // self.cellWidth]
        if selectCell in self.nextMoves:
            self.clearNextMoves()
            emptyCells = [self.grid[i[0]][i[1]] for i in self.selectedCell.movePiece(selectCell, self.rows)]
            if len(emptyCells) == 2:
                self.selectedCell = selectCell
                self.highlightJumps(selectCell)
            for cell in emptyCells: cell.piece = None
            if len(self.nextMoves) == 0:
                self.player = (self.player + 1 ) % 2
        else:
            self.clearNextMoves()
            if selectCell.piece is not None and selectCell.piece.color == self.playerColors[self.player]:
                self.highlightCells(selectCell)
                self.selectedCell = selectCell
            else:
                self.selectedCell = None

    def highlightJumps(self, cell):
        piece = cell.piece
        cells = []

        if cell.piece.isKing:
            direction = [1, -1]
        else:
            direction = [piece.direction]

        for vertical in direction:
            for horizontal in [1, -1]:
                x = cell.col + horizontal
                y = cell.row + vertical
                match self.isValidCell(x, y, piece.color):
                    case -1:
                        x += horizontal
                        y += vertical
                        if self.isValidCell(x, y, piece.color) == 1: 
                            cells.append(self.grid[y][x])
                            self.grid[y][x].highlight = True
                    case _:
                        pass
        for cell in cells:
            cell.highlight = True
        self.nextMoves = cells

    def highlightCells(self, cell):
        piece = cell.piece
        cells = []

        if cell.piece.isKing:
            direction = [1, -1]
        else:
            direction = [piece.direction]
        
        for vertical in direction:
            for horizontal in [1, -1]:
                x = cell.col + horizontal
                y = cell.row + vertical
                match self.isValidCell(x, y, piece.color):
                    case 1:
                        cells.append(self.grid[y][x])
                        self.grid[y][x].highlight = True
                    case -1:
                        x += horizontal
                        y += vertical
                        if self.isValidCell(x, y, piece.color) == 1: 
                            cells.append(self.grid[y][x])
                            self.grid[y][x].highlight = True
                    case _:
                        pass
        for cell in cells:
            cell.highlight = True
        self.nextMoves = cells

    def clearNextMoves(self):
        for cell in self.nextMoves:
            cell.highlight = False
        self.nextMoves = []

    def isValidCell(self, x, y, color):
        if (0 <= x < len(self.grid)) and (0 <= y < len(self.grid[0])):
            piece = self.grid[y][x].piece
            if piece is not None:
                return 0 if color == piece.color else -1
            return 1
        return 0

    def draw(self, screen):
        draw.rect(screen, self.playerColors[self.player], self.border, 25)
        for row in self.grid:
            for cell in row:
                cell.drawCell(screen)