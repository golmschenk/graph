"""Contains the interface for creating and managing graphs."""
from graph import Graph


class Interface:
    """The class for user interfacing with the graph code."""
    def create_graph_with_user_prompts(self):
        """Asks the user for the information required to build a graph."""
        graph = Graph()
        user_input = input("Will the graph use reliability? (y/n): ")
        if user_input.lower().startswith('y'):
            graph.using_reliability = True
        user_input = input("Will the graph use weight? (y/n): ")
        if user_input.lower().startswith('y'):
            graph.using_weight = True
        number_of_vertices = int(input("How many vertices will there be?: "))
        graph.initialize_with_size(number_of_vertices)
        i = 0
        while True:
            print("Finish by typing -1 -1 for the edge vertices")
            user_input = input("Enter edge number %s's vertices: " % i)
            edge = list(map(int, user_input.split(' ')))
            if edge[0] == -1 and edge[1] == -1:
                break
            reliability = float(input("Enter edge number %s's reliability: " % i))
            weight = float(input("Enter edge number %s's weight: " % i))
            graph.add_weighted_reliability_edge(edge[0], edge[1], reliability, weight)
