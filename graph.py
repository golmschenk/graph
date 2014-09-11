"""Graph class using an adjacency list."""
import csv
from vertex import Vertex


class Graph():
    def __init__(self):
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.is_weighted = False
        self.vertex_list = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.vertex_list = []
        for i in range(size):
            self.vertex_list.append(Vertex(i))

    def add_edge(self, vertex1, vertex2):
        self.vertex_list[vertex1].adjacency_list.append(vertex2)
        self.vertex_list[vertex2].adjacency_list.append(vertex1)

    def add_weighted_edge(self, vertex1, vertex2, weight):
        self.vertex_list[vertex1].adjacency_list.append((vertex2, weight))
        self.vertex_list[vertex2].adjacency_list.append((vertex1, weight))

    def set_all_vertices_unvisited(self):
        for vertex in self.vertex_list:
            vertex.visited = False

    def depth_first_search(self, start):
        self.vertex_list[start].visited = True
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].adjacency_list:
                self.depth_first_search(vertex_index)

    def get_edges_from_csv(self, file_path):
        with open(file_path) as file:
            for edge in csv.reader(file):
                edge = list(map(int, edge))
                self.add_edge(edge[0], edge[1])

    def find_number_of_components(self):
        number_of_components = 0
        for vertex in self.vertex_list:
            if not vertex.visited:
                self.depth_first_search(vertex.label)
                number_of_components += 1
