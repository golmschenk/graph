"""Graph class using an adjacency list."""
import copy
import csv
from edge import Edge
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
        self.removed_edge_probability_list = []
        self.removed_edge_list = []
        self.edge_list = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.vertex_list = []
        for i in range(size):
            self.vertex_list.append(Vertex(i))

    def add_edge(self, vertex1, vertex2):
        self.vertex_list[vertex1].adjacency_list.append(vertex2)
        self.vertex_list[vertex2].adjacency_list.append(vertex1)
        self.edge_list.append(Edge(vertex1, vertex2))

    def add_weighted_edge(self, vertex1, vertex2, weight):
        self.vertex_list[vertex1].adjacency_list.append(vertex2)
        self.vertex_list[vertex2].adjacency_list.append(vertex1)
        self.edge_list.append(Edge(vertex1, vertex2, weight=weight))

    def add_reliability_edge(self, vertex1, vertex2, reliability):
        self.vertex_list[vertex1].adjacency_list.append(vertex2)
        self.vertex_list[vertex2].adjacency_list.append(vertex1)
        self.edge_list.append(Edge(vertex1, vertex2, reliability=reliability))

    def add_weighted_reliability_edge(self, vertex1, vertex2, reliability, weight):
        self.vertex_list[vertex1].adjacency_list.append(vertex2)
        self.vertex_list[vertex2].adjacency_list.append(vertex1)
        self.edge_list.append(Edge(vertex1, vertex2, reliability=reliability, weight=weight))

    def set_all_vertices_unvisited(self):
        for vertex in self.vertex_list:
            vertex.visited = False

    def simple_depth_first_search(self, start):
        self.vertex_list[start].visited = True
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].visited:
                self.depth_first_search(vertex_index)
            else:
                self.has_a_cycle = True

    def reliability_depth_first_search(self, start):
        self.vertex_list[start].visited = True
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].visited:
                self.vertex_list[vertex_index].parent = start
                self.depth_first_search(vertex_index)
            else:
                self.has_a_cycle = True


    def depth_first_search(self, start):
        if self.using_reliability:
            self.reliability_depth_first_search(start)
        else:
            self.simple_depth_first_search(start)

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

    def attain_reliability_for_diameter(self, diameter):
        self.depth_first_search(self.vertex_list[0])
        if not self.vertex_list[self.number_of_vertices - 1].visited:
            return 0
        else:
            # Check if within diameter.
            vertex_index = self.number_of_vertices - 1
            for i in range(diameter):
                if self.vertex_list[vertex_index].parent == 0:
                    reached = True
                    break
            if not reached:
                return 0
            # Get the reliability of this graph.
            reliability = 1
            for edge in self.edge_list:
                if edge.removed:
                    reliability *= (1 - edge.reliability)
                else:
                    reliability *= edge.reliability
            # Add the reliability of the subgraphs.
            for edge in self.edge_list:
                subgraph = self.clone_with_edge_removed(edge)
                reliability += subgraph.attain_reliability_for_diameter(diameter)
            return reliability



    def clone_with_edge_removed(self, edge_to_remove):
        subgraph = Graph()
        subgraph.number_of_vertices = self.number_of_vertices
        subgraph.number_of_edges = self.number_of_edges - 1
        subgraph.using_reliability = self.using_reliability
        subgraph.using_weight = self.using_weight
        subgraph.vertex_list = copy.deepcopy(self.vertex_list)
        subgraph.edge_list = copy.deepcopy(self.edge_list)
        #Remove the edge
        for edge in subgraph.edge_list:
            if edge.vertex_list == edge_to_remove.vertex_list:
                subgraph.vertex_list[edge.vertex_list[0]].remove(edge.vertex_list[1])
                subgraph.vertex_list[edge.vertex_list[1]].remove(edge.vertex_list[0])
                edge.removed = True
        return subgraph




