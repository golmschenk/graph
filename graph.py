"""Graph class using an adjacency list."""
import copy
import csv
import math
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
        self.edge_list = []
        self.queue = []

    def initialize_with_size(self, size):
        self.number_of_vertices = size
        self.vertex_list = []
        for i in range(size):
            self.vertex_list.append(Vertex(i))

    def add_edge(self, vertex1, vertex2, reliability=1.0, weight=1.0):
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
                self.vertex_list[vertex_index].parent = start
                self.depth_first_search(vertex_index)
            else:
                if self.vertex_list[start].parent != vertex_index:
                    self.has_a_cycle = True

    def reliability_depth_first_search(self, start):
        self.vertex_list[start].visited = True
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].visited:
                self.vertex_list[vertex_index].parent = start
                self.depth_first_search(vertex_index)
            else:
                self.has_a_cycle = True

    def breadth_first_search(self, start):
        self.vertex_list[start].visited = True
        if self.vertex_list[start].parent == -1:
            self.vertex_list[start].value = 0
        for vertex_index in self.vertex_list[start].adjacency_list:
            if not self.vertex_list[vertex_index].visited:
                edge_vertex_list = [start, vertex_index]
                edge_vertex_list.sort()
                edge = next((x for x in self.edge_list if x.vertex_list == edge_vertex_list), "Not here")
                current_value = self.vertex_list[start].value + edge.weight
                if current_value < self.vertex_list[vertex_index].value:
                    self.vertex_list[vertex_index].parent = start
                    self.vertex_list[vertex_index].value = current_value
                    self.queue.append([vertex_index, current_value])
        if len(self.queue):
            self.queue.sort(key=lambda entry: entry[1])
            next_vertex = self.queue.pop(0)[0]
            self.breadth_first_search(next_vertex)
            return
        else:
            return


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

    def check_for_cycles(self):
        self.depth_first_search(0)
        return self.has_a_cycle

    def display_shortest_paths(self):
        source = 0
        self.dijkstra_algorithm(source)
        for vertex_index in self.vertex_list:
            path_string = str(vertex_index)
            current_index = vertex_index
            while current_index != -1:
                current_index = self.vertex_list[vertex_index]
                path_string = str(current_index) + ',' + path_string
            print(path_string)

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
            graph.add_edge(edge[0], edge[1], weight=edge[2])
        return graph

    @classmethod
    def create_reliability_graph_from_csv(cls, file_path):
        graph = cls()
        graph.using_reliability = True
        with open(file_path) as file:
            edge_list = list(csv.reader(file))
        graph.number_of_vertices = max([int(edge[i]) for edge in edge_list for i in range(2)]) + 1
        graph.initialize_with_size(graph.number_of_vertices)
        for edge in edge_list:
            edge = [int(edge[0]), int(edge[1]), float(edge[2])]
            graph.add_edge(edge[0], edge[1], reliability=edge[2])
        return graph

    @classmethod
    def create_reliability_weighted_graph_from_csv(cls, file_path):
        graph = cls()
        graph.using_reliability = True
        with open(file_path) as file:
            edge_list = list(csv.reader(file))
        graph.number_of_vertices = max([int(edge[i]) for edge in edge_list for i in range(2)]) + 1
        graph.initialize_with_size(graph.number_of_vertices)
        for edge in edge_list:
            edge = [int(edge[0]), int(edge[1]), float(edge[2]), float(edge[3])]
            graph.add_edge(edge[0], edge[1], reliability=edge[2], weight=edge[3])
        return graph

    @classmethod
    def create_wireless_mesh_graph_from_csv(cls, file_path):
        graph = cls()
        graph.using_reliability = True
        graph.using_weight = True
        with open(file_path) as file:
            position_list = list(csv.reader(file))
        i = 0
        #Create all the vertices
        for position_string in position_list:
            position = [float(position_string[0]), float(position_string[1])]
            graph.vertex_list.append(Vertex(i, position=position))
            graph.number_of_vertices += 1
            i += 1
        #Create the wireless mesh edges.
        i = 0
        while i < len(graph.vertex_list):
            j = i + 1
            while j < len(graph.vertex_list):
                vertex1 = graph.vertex_list[i]
                vertex2 = graph.vertex_list[j]
                if vertex1 is not vertex2:
                    distance = math.hypot(vertex2.position[0]-vertex1.position[0], vertex2.position[1]-vertex2.position[1])
                    reliability = 1 - (0.001 * (distance**2))
                    graph.add_edge(vertex1.label, vertex2.label, reliability=reliability, weight=distance)
                j += 1
            i += 1
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

    def attain_reliability_for_diameter(self, diameter, terminal_list=None):
        if not terminal_list:
            terminal_list = [self.number_of_vertices - 1]
        self.breadth_first_search(0)
        if not all(self.vertex_list[terminal_index].visited for terminal_index in terminal_list):
            return 0
        else:
            if diameter < all(self.vertex_list[terminal_index].value for terminal_index in terminal_list):
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
                if not edge.removed:
                    subgraph = self.clone_with_edge_removed(edge)
                    reliability += subgraph.attain_reliability_for_diameter(diameter, terminal_list=terminal_list)
            return reliability

    def reset_all_vertices(self):
        self.set_all_vertices_unvisited()
        for vertex in self.vertex_list:
            vertex.parent = -1
        for vertex in self.vertex_list:
            vertex.value = float("inf")

    def reset_graph(self):
        self.reset_all_vertices()
        for edge in self.edge_list:
            edge.removed = False
        self.queue = []
        self.has_a_cycle = False

    def clone_with_edge_removed(self, edge_to_remove):
        subgraph = Graph()
        subgraph.number_of_vertices = self.number_of_vertices
        subgraph.number_of_edges = self.number_of_edges - 1
        subgraph.using_reliability = self.using_reliability
        subgraph.using_weight = self.using_weight
        subgraph.vertex_list = copy.deepcopy(self.vertex_list)
        subgraph.reset_all_vertices()
        subgraph.edge_list = copy.deepcopy(self.edge_list)
        #Remove the edge
        for edge in subgraph.edge_list:
            if edge.vertex_list == edge_to_remove.vertex_list:
                subgraph.vertex_list[edge.vertex_list[0]].adjacency_list.remove(edge.vertex_list[1])
                subgraph.vertex_list[edge.vertex_list[1]].adjacency_list.remove(edge.vertex_list[0])
                edge.removed = True
        return subgraph


if __name__ == "__main__":
    graph = Graph.create_reliability_graph_from_csv("examplegraphs/quarter_success_mini_graph.csv")
    #graph = Graph.create_wireless_mesh_graph_from_csv("examplegraphs/basic_wireless_mesh_graph.csv")
    r = graph.attain_reliability_for_diameter(4, terminal_list=[1,2])
    print(r)
    #graph = Graph.create_weighted_graph_from_csv("examplegraphs/basic_weighted_graph.csv")
    #graph.breadth_first_search(0)
    #print('go')