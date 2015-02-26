import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils
from matplotlib.cbook import Null
import math
import sys

# the number of cities on our itinerary
if len(sys.argv) > 1:
    CITIES = int(sys.argv[1])
else:
    CITIES = 40

# the number of alternative nearest neighbors to check
ALTERNATIVES = 3
# the number of nodes we want to work ahead
PREDICTION_CAP = 10

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# keep track of which edges we've included in our solution
visited_cities = []

visited_edges = []

city_positions = cities.get_city_positions_safely()

last_edge = None

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
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
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

def findAngle(node1, node2):
    initialPosition = city_positions[node1]
    nextPosition = city_positions[node2]
    delta_x = nextPosition[0] - initialPosition[0]
    delta_y = nextPosition[1] - initialPosition[1]
    quadrant = 1
    if delta_x < 0:
        quadrant = 2
        if delta_y < 0:
            quadrant = 3
    elif delta_y < 0 :
        quadrant = 4
    theta = math.degrees(math.atan(delta_y/delta_x))
    if quadrant== 2 or quadrant == 3:
        theta +=180
    return theta

def determine_best_radial_neighbor(node):
    """
    Returns it
    @author: jreynolds
    """
    global last_edge
    nearest_edges = graph.edges(node)
    angle = 180.0
    if last_edge is not None:
        angle=findAngle(last_edge[0],last_edge[1])
    next_edge = None
    smallest_angle = None
    for edge in nearest_edges:
        possible_next_angle = findAngle(node,edge[1])
        if possible_next_angle < angle:
            possible_next_angle += 360
        if smallest_angle is None or possible_next_angle < smallest_angle:
            smallest_angle = possible_next_angle
            next_edge = edge
    last_edge=next_edge
    return (next_edge, [rmv for rmv in nearest_edges if rmv != next_edge \
                                                    and rmv[1] not in visited_cities])

def find_extreme_vertex():
    """
    Find the most extreme vertex in the -x direction
    @author: jreynolds
    """
    furthest_node = None
    furthest_x= None
    for node in graph.nodes():
        position = city_positions[node]
        if furthest_x is None or position[0] < furthest_x:
            furthest_x = position[0]
            furthest_node = node
    return furthest_node
def average_position(node1, node2):
    position1 = city_positions[node1]
    position2 = city_positions[node2]
    new_position = ((position1[0]+position2[0])/2,(position1[1]+position2[1])/2)
    return new_position

def find_closest_outer_edge(inner_node):
    closest_edge = None
    shortest_dist = None
    for edge in visited_edges:
        # distance_to_edge_center = utils.distance(city_positions[inner_node], edge_center_position)
        distance_to_edge_center = utils.find_shortest_distance(edge, city_positions[inner_node])
        if shortest_dist is None or distance_to_edge_center< shortest_dist:
            shortest_dist = distance_to_edge_center
            closest_edge = edge
    return closest_edge

def find_closest_inner_vertex(outer_edge):
    closest_vertex = None
    shortest_dist = None
    for inner_node in [node for node in graph.nodes() if node not in visited_cities]:
        # distance_to_edge_center = utils.distance(city_positions[inner_node], edge_center_position)
        distance_to_edge = utils.find_shortest_distance(outer_edge, city_positions[inner_node])
        if shortest_dist is None or distance_to_edge < shortest_dist:
            shortest_dist = distance_to_edge
            closest_vertex = inner_node
    return closest_vertex, shortest_dist

def solve_salesman_radially():
    """
    Solves the problem
    @author: jreynolds
    """
    global visited_edges
    # select the first node
    current_city = find_extreme_vertex()
    print("INITIAL CITY: " + current_city)
    initial_city_nearest_edges = None

    # after [CITIES - 1], there's only one edge left to connect
    while len(visited_cities) == 0 or current_city!=visited_cities[0]:
        # get the possible edges to take, and the ones we can remove
        visited_cities.append(current_city)

        best_edge, rmv = determine_best_radial_neighbor(current_city)
        if len(visited_cities) > 1:
            graph.remove_edges_from(rmv)
        else:
            initial_city_nearest_edges=rmv

        current_city = best_edge[1]
        visited_edges.append(best_edge)
        print("NEXT CITY: " + current_city)
    graph.remove_edges_from([rmv for rmv in initial_city_nearest_edges if  rmv[1] != visited_cities[1] \
    and rmv[1]!= visited_cities[len(visited_cities)-1]])
    
    while len(visited_cities) < CITIES: 
        next_nearest_vertex = None
        shortest_dist = None
        deformed_edge = None
        for edge in visited_edges:
            vertex, dist = find_closest_inner_vertex(edge);
            if shortest_dist is None or dist < shortest_dist:
                next_nearest_vertex = vertex
                shortest_dist = dist
                deformed_edge = edge
        u, v = deformed_edge
        print(u, v)
        graph.remove_edge(v, u)
        visited_edges = [edge for edge in visited_edges if edge != (u, v) and edge != (v, u)]
        graph.remove_edges_from(graph.edges(next_nearest_vertex))
        graph.add_edge(next_nearest_vertex, u)
        graph.add_edge(next_nearest_vertex, v)
        visited_edges.append((next_nearest_vertex, u))
        visited_edges.append((next_nearest_vertex, v))
        visited_cities.append(next_nearest_vertex)
            
#     for inner_node in [node for node in graph.nodes() if node not in visited_cities]:
#         u, v = find_closest_outer_edge(inner_node)
#         print(u, v)
#         graph.remove_edge(v, u)
#         visited_edges = [edge for edge in visited_edges if edge != (u, v) and edge != (v, u)]
#         graph.remove_edges_from(graph.edges(inner_node))
#         graph.add_edge(inner_node, u)
#         graph.add_edge(inner_node, v)
#         visited_edges.append((inner_node, u))
#         visited_edges.append((inner_node, v))


#     for node in graph.nodes():
#         initial_city = visited_cities[0]
#         if graph.degree(node) == 1  and node != initial_city:
#             visited_cities.append(node)
#             print("FINAL CITY: " + node)
#             graph.add_edge(initial_city, node)
#             break

    draw_solution()
solve_salesman_radially()
#solve_salesman_problem()
