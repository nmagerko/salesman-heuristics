import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils

# the number of cities on our itinerary
CITIES = 16
# the number of alternative nearest neighbors to check
ALTERNATIVES = 3
# the number of nodes we want to work ahead
PREDICTION_CAP = 5

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# keep track of which edges we've included in our solution
visited_cities = []

def clean_edge_list(edge_list, extra=[]):
    """
    Removes any edges that would involve moving backwards
    along the solution
    """
    return [edge for edge in edge_list if edge[1] not in visited_cities \
            and edge[1] not in extra]
    

def get_nearest_neighbor_edges(node, requested=1, traveled=[]):
    """
    Returns a tuple containing (a list of [number_to_return] nearest neighbors,
    and a list of the remaining edges)
    """
    incident_edges = graph.edges(node, data=True)
    sorted_edges = sorted(incident_edges, key=lambda edge: edge[2]['weight'])
    # Don't go to cities that we've visited (the second city in the edge)
    sorted_edges = clean_edge_list(sorted_edges, extra=traveled)

    return (sorted_edges[0:requested], sorted_edges[requested:])

def determine_best_neighbor_edge(potential_edges):
    neighbor_prediction_weights = []
    for edge in potential_edges:
        outcome_path = []
        outcome_nodes = []
        
        outcome_path.append(edge)
        potential_neighbor = edge[1]
        outcome_nodes.append(potential_neighbor)
        
        for predictions in range(0, PREDICTION_CAP):
            nearest_edge_list = get_nearest_neighbor_edges(node=outcome_nodes[-1], traveled=outcome_nodes)
            if nearest_edge_list[0]:
                next_edge = nearest_edge_list[0][0]
                outcome_path.append(next_edge)
                next_node = next_edge[1]
                outcome_nodes.append(next_node)
            
        neighbor_prediction_weights.append({ 'edge': edge,
                                             'weight': utils.total_weight(outcome_path) })
        
    sorted_weights = sorted(neighbor_prediction_weights, key=lambda edge: edge['weight'])
    sorted_weights = [prediction_weight['edge'] for prediction_weight in sorted_weights]
    
    return (sorted_weights[0], sorted_weights[1:])

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
        nearest_edges, rmv = get_nearest_neighbor_edges(current_city, ALTERNATIVES)
        graph.remove_edges_from(rmv)
        
        best_edge, rmv = determine_best_neighbor_edge(nearest_edges)
        graph.remove_edges_from(rmv)

        current_city = best_edge[1]
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
