"""Vertex class using an adjacency list."""


class Vertex():
    def __init__(self, label):
        self.label = label
        self.adjacency_list = []
        self.visited = False
        self.parent = -1
        self.value = float("inf")
