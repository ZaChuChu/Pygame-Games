from snakeSegment import SnakeSegment
class Snake:
    def __init__(self, cell, direction):
        cell.makeSnake()
        self.head = SnakeSegment(cell)
        self.tail = self.head
        self.direction = direction # 0 up, 1 right etc

    def addSegment(self, cell):
        cell.makeSnake()
        newSegment = SnakeSegment(cell)
        newSegment.next = self.head
        self.head.prev = newSegment
        self.head = newSegment
        

    def setDirection(self, direction):
        if (direction + 2) % 4 != self.direction:
            self.direction = direction
    
    def move(self, cell):
        self.addSegment(cell)
        self.tail = self.tail.clearCell().prev

