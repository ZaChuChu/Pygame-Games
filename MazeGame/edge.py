class Edge:
    def __init__(self, node1, node2, weight):
        self.weight = weight
        if node1[0] < node2[0] or node1[1] < node2[1]:
            self.node1 = node1
            self.node2 = node2
        else:
            self.node1 = node2
            self.node2 = node1
    
    def __lt__(self, obj):
        return self.weight <= obj.weight
    
    def __repr__(self) -> str:
        # return f"{self.weight} {self.node1} {self.node2}"
        return f"{self.node1} -> {self.node2}"
    
def mstSort(obj1, obj2):
    rowDiff = obj1.node1[0] - obj2.node1[0] 
    if rowDiff == 0:
        return obj1.node1[1] - obj2.node1[1]
    return rowDiff 