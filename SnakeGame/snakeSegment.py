class SnakeSegment:
    def __init__(self, cell):
        self.next = None
        self.prev = None
        self.cell = cell
        cell.isSpecial = True
        cell.isSnake = True

    def clearCell(self):
        self.cell.clear()
        return self

