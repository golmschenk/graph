class Edge:
    def __init__(self, vertex1, vertex2, removed=False, reliability=1, weight=1):
        self.vertex_list = [vertex1, vertex2]
        self.reliability = reliability
        self.removed = removed
        self.weight = weight
