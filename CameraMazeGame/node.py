class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent = self
        self.set = [self]

    def inUnion(self, other):
         return self.parent == other.parent

    def union(self, other):
        otherParent = other.parent
        selfParent = self.parent
        if selfParent != otherParent:
            if len(selfParent.set) > len(otherParent.set):
                for node in otherParent.set:
                    node.parent = selfParent
                    selfParent.set.append(node)
                otherParent.set = []
            else:
                for node in selfParent.set:
                    node.parent = otherParent
                    otherParent.set.append(node)
                selfParent.set = []
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.row} {self.col} {self.parent if self.parent != self else 0}"
                