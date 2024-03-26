from pygame import Rect, draw

class Cell:
    def __init__(self, color, height, width, row, col, xOffset, yOffset):
        self.piece = None
        self.color = color
        self.height = height
        self.width = width
        self.row = row
        self.col = col
        self.x = xOffset + col * width
        self.y = yOffset + row * height
        self.rect = Rect(self.x, self.y, width, height) 
        self.highlight = False

    def getNextMoves(self):
        if self.piece is None:
            return []
        return self.piece.getValidSquares()
    
    def movePiece(self, newCell, rows):
        newCell.piece = self.piece
        if not newCell.piece.isKing:
            if newCell.row == 0 and self.piece.direction == -1:
                newCell.piece.isKing = True
            elif newCell.row == rows - 1 and self.piece.direction == 1:
                newCell.piece.isKing = True
        rows = [row for row in range(self.row, newCell.row, 1 if self.row < newCell.row else -1)]
        cols = [col for col in range(self.col, newCell.col, 1 if self.col < newCell.col else -1)]
        coordiates = [[rows[i], cols[i]] for i in range(len(rows))]
        return coordiates
    
    def __str__(self):
        return f"""Row: {self.row}, Col: {self.col}, Has Piece: {self.piece is not None}"""

    def drawCell(self, screen):
        if self.highlight:
            draw.rect(screen, "light blue", self.rect)
        else:
            draw.rect(screen, self.color, self.rect)
            if self.piece is not None:
                self.piece.draw(screen, self.x + self.width / 2, self.y + self.height / 2)
