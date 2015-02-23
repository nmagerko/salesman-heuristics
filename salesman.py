import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils
import pdb

# the number of cities on our itinerary
CITIES = 6
# after finding the nearest neighbor, also choose [ALTERNATIVES_TO_CHECK] - 1
# of the closest remaining neighbors
ALTERNATIVES_TO_CHECK = 3

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# keep track of how many nodes we've taken care of so far
remaining = CITIES
# keep track of which edges we've included in our solution
solution_edges = []

def get_nearest_neighbor_edges(node, number_to_return=1):
    """
    Returns a tuple containing (a list of [number_to_return] nearest neighbors,
    and a list of the remaining edges)
    """
    incident_edges = graph.edges(node, data=True)
    sorted_edges = sorted(incident_edges, key=lambda edge: edge[2]['weight'])
    ### I think this is where the problem is coming up
    ### I was trying to make sure that we don't include any edges that are
    ### in the solution, but I think the list comprehension is wrong
    sorted_edges = [edge for edge in sorted_edges if edge not in solution_edges]

    return (sorted_edges[0:number_to_return], sorted_edges[number_to_return:])

def determine_best_neighbor_edge(edges):
    """
    I'll need to make this method a bit clearer
    Essentially, it takes the edges we're considering, and determines
    which one is the best edge to take. Assume this works for now
    """
    neighbor_prediction_weights = []
    for edge in edges:
        outcome_path = []
        # get the neighbor in question out of the tuple (x)
        potential_neighbor = edge[1]
        outcome_path.append(edge)
        # find its shortest edge (need to get edge out of list AND tuple)
        nearest_edge1 = get_nearest_neighbor_edges(potential_neighbor)[0][0]
        outcome_path.append(nearest_edge1)
        # get the new neighbor out of the previous edge
        potential_neighbor1 = nearest_edge1[1]
        # get the shortest edge of this new neighbor
        nearest_edge2 = get_nearest_neighbor_edges(potential_neighbor1)[0][0]
        outcome_path.append(nearest_edge2)
        neighbor_prediction_weights.append({ 'edge' : edge,
                                            'weight' : utils.total_weight(outcome_path)})

    sorted_weights = sorted(neighbor_prediction_weights, key=lambda edge: edge['weight'])
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

    # note that I'm only trying to get through the first 2 iterations here
    # so far it isn't working out
    for i in range (0, 2):
        # get the possible edges to take, and the ones we can remove
        possible_edges, rmv = get_nearest_neighbor_edges(current_city, ALTERNATIVES_TO_CHECK)
        graph.remove_edges_from(rmv)

        # get the edge that we should use from the determination function
        # its pretty nasty since it returns a list of dictionaries, but that's
        # the way we'll have to stick with for now
        final_edge, rmv = determine_best_neighbor_edge(possible_edges)
        # get the final edge from its dictionary, and append it to solution
        final_edge = final_edge['edge']
        solution_edges.append(final_edge)
        print("NEXT CITY: " + final_edge[1])

        # set the current city to the second point on the edge, and remove
        # all other edges that we were considering
        current_city = final_edge[1]
        for removal in rmv:
            graph.remove_edge(removal['edge'][0], removal['edge'][1])

    draw_solution()

solve_salesman_problem()
