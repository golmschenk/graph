"""Graph class using an adjacency list."""


class Graph():
    def __init__(self):
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.adjacency_list = []
        self.visited = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.head_nodes = []
        for i in range(size):
            self.head_nodes.append([])

    def add_edge(self, vertex1, vertex2):
        self.head_nodes[vertex1].append(vertex2)
        self.head_nodes[vertex2].append(vertex1)

    def set_all_vertices_unvisited(self):
        self.visited = []
        for i in range(self.number_of_vertices):
            self.visited.append(False)

    def depth_first_search(self, start):
        self.visited[start] = True
        for node in self.adjacency_list[start]:
            if not self.visited[node]:
                self.depth_first_search(node)

