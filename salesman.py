import bruteforce
import cities
import math
import networkx as nx
import utils
import sys

# the number of cities on our itinerary
if len(sys.argv) > 1:
    CITIES = int(sys.argv[1])
else:
    CITIES = 50

# get a random subgraph of the full cities graph
graph = utils.random_subgraph(cities.get_city_graph_safely(), CITIES)
# get the city positions for all nodes in the graph
city_positions = cities.get_city_positions_safely()

# keep track of which cities and edges we've included in our solution
visited_cities = []
visited_edges = []

def findAngle(node1, node2):
    """
    Finds the angle between node1 and node2
    """
    # get the positions of the city where we're at, and
    # where we want to go
    initial_position = city_positions[node1]
    next_position = city_positions[node2]

    # find the distance between the cities in each dimension
    delta_x = next_position[0] - initial_position[0]
    delta_y = next_position[1] - initial_position[1]

    # decide on the quadrant, based on the signs of delta_x
    # and delta_y
    quadrant = 1
    if delta_x < 0:
        quadrant = 2
        if delta_y < 0:
            quadrant = 3
    elif delta_y < 0 :
        quadrant = 4

    # get the inverse tangent of [opposite/adjacent],
    # correcting angle based on quadrant
    theta = math.degrees(math.atan(delta_y/delta_x))
    if quadrant== 2 or quadrant == 3:
        theta +=180
    return theta

def determine_best_radial_neighbor(node):
    """
    Given some node in the graph, find the next node in the
    outer circuit by comparing the angles to all other nodes in
    the graph, choosing the smallest difference between the current
    angle
    """    
    
    # determine the angle in which we are traveling along outer circuit
    # if this is the first point on the circuit, start directly south
    angle = 270.0
    if visited_edges:
        last_edge = visited_edges[-1]
        angle = findAngle(last_edge[0],last_edge[1])

    # pick the node to add to the outer circuit by finding the node with
    # the smallest difference in angle from [angle]
    next_edge = None
    smallest_angle = None
    for potential_neighbor in nx.non_neighbors(graph, node):
        # find the angle between the upcoming node and this node
        possible_next_angle = findAngle(node, potential_neighbor)
        
        # ensure that angle is positive
        if possible_next_angle < angle:
            possible_next_angle += 360
        # update the smallest angle and next edge if appropriate
        if smallest_angle is None or possible_next_angle < smallest_angle:
            next_edge = (node, potential_neighbor)
            smallest_angle = possible_next_angle

    # return the next edge to add to the solution   
    return next_edge

def find_most_western_vertex():
    """
    Finds the most western vertex in the graph, by
    finding the node with the most negative x-valued
    position
    """

    # compare every node
    furthest_node = None
    furthest_x= None
    for node in graph.nodes():
        position = city_positions[node]
        if furthest_x is None or position[0] < furthest_x:
            furthest_x = position[0]
            furthest_node = node
    return furthest_node

def choose_best_edge_deformation(inner_vertex):
    """
    In a list of edges, find the minimal-distance edge-deformation for a vertex 
    """
    best_dist = None
    best_edge = None
    for edge in visited_edges:
        # the positions of the two vertices of the edge
        position1 = city_positions[edge[0]]
        position2 = city_positions[edge[1]]
        # the inner vertex position
        vertex_position = city_positions[inner_vertex]
        # find the distance between the two points of the edge
        original_dist = utils.distance(position1, position2)
        # find the sum of the distances between the inner vertex and the edge's vertices
        new_dist = utils.distance(position1, vertex_position) + utils.distance(position2, vertex_position)
        # find the change in distance after deformation
        delta_dist = new_dist - original_dist
        if best_dist is None or delta_dist < best_dist:
            best_dist = delta_dist
            best_edge = edge
    return best_edge, best_dist
        
def apply_salesman():
    """
    Apply the solution algorithm to the globally-stored graph
    """
    global visited_edges
    # select the first node
    current_city = find_most_western_vertex()
    print("INITIAL CITY: " + current_city)

    # continue if we haven't visited any cities, or if we haven't
    # formed the outer circuit
    while len(visited_cities) == 0 or current_city!=visited_cities[0]:
        visited_cities.append(current_city)
        
        # get the next best edge for the outer circuit
        u, v = determine_best_radial_neighbor(current_city)
        graph.add_edge(u, v)

        current_city = v
        visited_edges.append((u, v))
        print("NEXT CITY: " + current_city)
    
    # connect the inner vertices
    while len(visited_cities) < CITIES: 
        next_best_vertex = None
        shortest_dist = None
        deformed_edge = None
        # find the best edge deformation for each vertex and compare.
        # the smallest change in distance for an edge deformation is the best choice
        for inner_vertex in [node for node in graph.nodes() if node not in visited_cities]:
            edge, dist = choose_best_edge_deformation(inner_vertex)
            if shortest_dist is None or dist < shortest_dist:
                shortest_dist = dist
                next_best_vertex = inner_vertex
                deformed_edge = edge
                
        u, v = deformed_edge
        # remove the edge we are going to deform
        graph.remove_edge(v, u)
        
        # remove it from the visited edges as well
        visited_edges = [edge for edge in visited_edges if edge != (u, v) and edge != (v, u)]
        
        graph.add_edge(next_best_vertex, u)
        graph.add_edge(next_best_vertex, v)
        visited_edges.append((next_best_vertex, u))
        visited_edges.append((next_best_vertex, v))
        visited_cities.append(next_best_vertex)
    
print("Beginning heuristic...")
apply_salesman()
utils.draw_graph(graph, city_positions, 'Heuristic')

print("\n" + "Beginning brute-force...")
#lightest_graph = bruteforce.bruteforce(graph, city_positions)
#utils.draw_graph(lightest_graph, city_positions)

utils.show_graphs()