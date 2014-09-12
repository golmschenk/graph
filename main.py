from graph import Graph

g = Graph.create_weighted_graph_from_csv("examplegraphs/basic_weighted_graph")
g.vertex_list[1].value = 0
g.dijkstra_algorithm(1)
print('Complete')