import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils

# the number of cities on our itinerary
CITIES = 19

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# keep track of which edges we've included in our solution
visited_cities = []

def get_nearest_neighbor_edges(node, requested=1):
    """
    Returns a tuple containing (a list of [number_to_return] nearest neighbors,
    and a list of the remaining edges)
    """
    incident_edges = graph.edges(node, data=True)
    sorted_edges = sorted(incident_edges, key=lambda edge: edge[2]['weight'])
    # Don't go to cities that we've visited (the second city in the edge)
    sorted_edges = [edge for edge in sorted_edges if edge[1] not in visited_cities]

    return (sorted_edges[0:requested], sorted_edges[requested:])

def draw_solution():
    """
    Draws the solution graph
    """
    city_positions = cities.get_city_positions_safely()
    nx.draw_networkx(graph, pos=city_positions, with_labels=True)
    plt.show()

def solve_salesman_problem():
    """
    Solves the problem
    """
    # select the first node
    current_city = graph.nodes()[0]
    print("INITIAL CITY: " + current_city)

    # after [CITIES - 1], there's only one edge left to connect
    while len(visited_cities) < CITIES - 2:
        # get the possible edges to take, and the ones we can remove
        visited_cities.append(current_city)
        nearest_edge, rmv = get_nearest_neighbor_edges(current_city)
        nearest_edge = nearest_edge[0]
        graph.remove_edges_from(rmv)

        current_city = nearest_edge[1]
        print("NEXT CITY: " + current_city)
        
    for node in graph.nodes():
        initial_city = visited_cities[0]
        if graph.degree(node) == 1  and node != initial_city:
            visited_cities.append(node)
            print("FINAL CITY: " + node)
            graph.add_edge(initial_city, node)
            break

    draw_solution()

solve_salesman_problem()
