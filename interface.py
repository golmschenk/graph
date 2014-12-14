"""Contains the interface for creating and managing graphs."""
from graph import Graph


class Interface:
    """The class for user interfacing with the graph code."""
    def __init__(self):
        self.graph = None

    def main_prompt(self):
        print("===============================")
        print("Graph Projects - Greg Olmschenk")
        print("===============================")
        while True:
            print()
            print("What would you like to do?")
            print("a - Create graph via prompt")
            print("b - Load graph from csv file")
            print("c - Check if the graph has cycles")
            print("d - List shortest path to each node (Dijkstra)")
            print("e - Find the reliability (option for multiple terminal)")
            print("f - Exit")
            print()
            user_input = input("Which option would you like?: ")
            if user_input.lower() == 'f':
                break
            elif user_input.lower() == 'a':
                self.create_graph_with_user_prompts()
            elif user_input.lower() == 'b':
                self.load_graph_from_file_prompt()
            if not self.graph:
                print('You must create or load a graph first.')
                continue
            self.graph.reset_graph()
            if user_input.lower() == 'c':
                self.check_for_cycles()
            elif user_input.lower() == 'd':
                self.graph.display_shortest_paths()
            elif user_input.lower() == 'e':
                self.find_reliability()
        print()

    def create_graph_with_user_prompts(self):
        """Asks the user for the information required to build a graph."""
        self.graph = Graph()
        user_input = input("Will the graph use reliability? (y/n): ")
        if user_input.lower().startswith('y'):
            self.graph.using_reliability = True
        user_input = input("Will the graph use weight? (y/n): ")
        if user_input.lower().startswith('y'):
            self.graph.using_weight = True
        number_of_vertices = int(input("How many vertices will there be?: "))
        self.graph.initialize_with_size(number_of_vertices)
        i = 0
        while True:
            print("Finish by typing -1 -1 for the edge vertices")
            user_input = input("Enter edge number %s's vertices: " % i)
            edge = list(map(int, user_input.split(' ')))
            if edge[0] == -1 and edge[1] == -1:
                break
            if self.graph.using_reliability:
                reliability = float(input("Enter edge number %s's reliability: " % i))
            else:
                reliability = 1.0
            if self.graph.using_weight:
                weight = float(input("Enter edge number %s's weight: " % i))
            else:
                weight = 1.0
            self.graph.add_edge(edge[0], edge[1], reliability=reliability, weight=weight)
            i += 1

    def load_graph_from_file_prompt(self):
        corrdinates = False
        reliability = False
        weight = False
        user_input = input("Is this file a list a 2D vertex coordinates? (y/n): ")
        if user_input.lower().startswith('y'):
            corrdinates = True
        else:
            user_input = input("Does this file include reliability? (y/n): ")
            if user_input.lower().startswith('y'):
                reliability = True
            user_input = input("Does this file include weight? (y/n): ")
            if user_input.lower().startswith('y'):
                weight = True
            if reliability and weight:
                print('Reliability should be placed before weight in your file.')
        user_input = input("Enter the relative path to your file: ")
        if corrdinates:
            self.graph = Graph.create_wireless_mesh_graph_from_csv(user_input)
        elif weight and reliability:
            self.graph = Graph.create_reliability_weighted_graph_from_csv(user_input)
        elif reliability:
            self.graph = Graph.create_reliability_graph_from_csv(user_input)
        elif weight:
            self.graph = Graph.create_weighted_graph_from_csv(user_input)
        else:
            self.graph = Graph.create_graph_from_csv(user_input)

    def check_for_cycles(self):
        has_cycle = self.graph.check_for_cycles()
        if has_cycle:
            print("Has a cycle.")
        else:
            print("No cycles.")

    def find_reliability(self):
        diameter = float(input("Enter a diameter: "))
        print('Enter a list of terminals separated by spaces.')
        terminal_string = input("Enter nothing for final node as only terminal: ")
        if terminal_string:
            terminal_list = list(map(int, terminal_string.split(' ')))
            reliability = self.graph.attain_reliability_for_diameter(diameter, terminal_list)
        else:
            reliability = self.graph.attain_reliability_for_diameter(diameter)
        print("The graph reliability is %f" % reliability)
