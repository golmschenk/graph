"""Graph class using an adjacency list."""


class Graph():
    def __init__(self):
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.head_nodes = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.head_nodes = []
        for i in range(size):
            self.head_nodes.append([])
