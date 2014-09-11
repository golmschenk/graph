"""Graph class using an adjacency list."""
import csv


class Graph():
    def __init__(self):
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.adjacency_list = []
        self.visited = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.adjacency_list = []
        for i in range(size):
            self.adjacency_list.append([])

    def add_edge(self, vertex1, vertex2):
        self.adjacency_list[vertex1].append(vertex2)
        self.adjacency_list[vertex2].append(vertex1)

    def set_all_vertices_unvisited(self):
        self.visited = []
        for i in range(self.number_of_vertices):
            self.visited.append(False)

    def depth_first_search(self, start):
        self.visited[start] = True
        for node in self.adjacency_list[start]:
            if not self.visited[node]:
                self.depth_first_search(node)

    def get_edges_from_csv(self, file_path):
        with open(file_path) as file:
            for edge in csv.reader(file):
                edge = list(map(int, edge))
                self.add_edge(edge[0], edge[1])

