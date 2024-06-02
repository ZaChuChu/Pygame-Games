class ColorGroup:
    def __init__(self, cell, color, colors):
        self.color = color
        self.cells = set([cell])
        self.adjacent_sets = {color:set() for color in colors}

    def size(self):
        return len(self.cells)
    
    def refSize(self):
        return sum([len(group) for group in self.adjacent_sets.values()])
    
    def createReference(self, other):
        self.adjacent_sets[other.color].add(other)
        other.adjacent_sets[self.color].add(self)

    def merge(self, other):
        self.cells.update(other.cells)
        for color in other.adjacent_sets:
            for colorGroup in other.adjacent_sets[color]:
                if colorGroup not in self.adjacent_sets[color]:
                    self.createReference(colorGroup)
                colorGroup.adjacent_sets[other.color].discard(other)
            other.adjacent_sets[color].clear()
        other.cells.clear()
    
    def union(self, other):
        if self != other:  
            if self.color == other.color:
                other.merge(self)
                return other
            else:
                self.createReference(other)
                return self
        
    def claimColor(self, newColor):
        for cell in self.cells:
            cell.setColor(newColor)
        print(self.containsSelf())
        for adjacent_set in self.adjacent_sets.values():
            for colorGroup in adjacent_set:
                colorGroup.adjacent_sets[self.color].remove(self)
                colorGroup.adjacent_sets[newColor].add(self)
        print(self.containsSelf())
                
        for same_color_group in self.adjacent_sets[newColor]:
            same_color_group.adjacent_sets[newColor].remove(self)

        self.color = newColor

        print(self.containsSelf())
        for colorGroup in self.adjacent_sets[newColor]:
            self.merge(colorGroup)
        print(self.containsSelf())

        self.adjacent_sets[newColor].clear()
        
    def containsSelf(self):
        for groups in self.adjacent_sets.values():
            for group in groups:
                if group == self:
                    return True
        return False