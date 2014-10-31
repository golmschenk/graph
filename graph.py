"""Graph class using an adjacency list."""
import copy
import csv
from vertex import Vertex
from operator import attrgetter


class Graph():
    def __init__(self):
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.using_weight = False
        self.using_reliability = False
        self.has_a_cycle = False
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

    def add_reliability_edge(self, vertex1, vertex2, reliability):
        self.vertex_list[vertex1].adjacency_list.append((vertex2, reliability))
        self.vertex_list[vertex2].adjacency_list.append((vertex1, reliability))

    def add_weighted_reliability_edge(self, vertex1, vertex2, reliability, weight):
        self.vertex_list[vertex1].adjacency_list.append((vertex2, reliability, weight))
        self.vertex_list[vertex2].adjacency_list.append((vertex1, reliability, weight))

    def set_all_vertices_unvisited(self):
        for vertex in self.vertex_list:
            vertex.visited = False

    def depth_first_search(self, start):
        self.vertex_list[start].visited = True
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].visited:
                self.depth_first_search(vertex_index)
            else:
                if self.vertex_list[start].parent != vertex_index:
                    self.has_a_cycle = True

    def get_edges_from_csv(self, file_path):
        with open(file_path) as file:
            for edge in csv.reader(file):
                edge = list(map(int, edge))
                self.add_edge(edge[0], edge[1])

    @classmethod
    def create_graph_from_csv(cls, file_path):
        graph = cls()
        with open(file_path) as file:
            edge_list = list(csv.reader(file))
        graph.number_of_vertices = max([int(vertex_index) for edge in edge_list for vertex_index in edge]) + 1
        graph.initialize_with_size(graph.number_of_vertices)
        for edge in edge_list:
            edge = list(map(int, edge))
            graph.add_edge(edge[0], edge[1])
        return graph

    @classmethod
    def create_weighted_graph_from_csv(cls, file_path):
        graph = cls()
        graph.using_weight = True
        with open(file_path) as file:
            edge_list = list(csv.reader(file))
        graph.number_of_vertices = max([int(edge[i]) for edge in edge_list for i in range(2)]) + 1
        graph.initialize_with_size(graph.number_of_vertices)
        for edge in edge_list:
            edge = list(map(int, edge))
            graph.add_weighted_edge(edge[0], edge[1], edge[2])
        return graph

    def find_number_of_components(self):
        number_of_components = 0
        for vertex in self.vertex_list:
            if not vertex.visited:
                self.depth_first_search(vertex.label)
                number_of_components += 1
        return number_of_components

    def dijkstra_algorithm(self, start):
        self.vertex_list[start].visited = True
        #Update adjacent vertices' weights.
        for adjacent_edge in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[adjacent_edge[0]].visited:
                if adjacent_edge[1] + self.vertex_list[start].value < self.vertex_list[adjacent_edge[0]].value:
                    self.vertex_list[adjacent_edge[0]].value = adjacent_edge[1] + self.vertex_list[start].value
                    self.vertex_list[adjacent_edge[0]].parent = start
        unvisited_vertex_list = [vertex for vertex in self.vertex_list if not vertex.visited]
        if unvisited_vertex_list:
            minimum_value_vertex = min(unvisited_vertex_list, key=attrgetter('value'))
            self.dijkstra_algorithm(minimum_value_vertex.label)






