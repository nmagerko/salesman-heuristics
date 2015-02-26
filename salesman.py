import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils
import math
import sys

# the number of cities on our itinerary
if len(sys.argv) > 1:
    CITIES = int(sys.argv[1])
else:
    CITIES = 55

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# get the city positions for all nodes in the graph
city_positions = cities.get_city_positions_safely()

# keep track of which cities and edges we've included in our solution
visited_cities = []
visited_edges = []

def draw_solution():
    """
    Draws the solution graph
    """
    # tell networkx to generate pyplot graph
    nx.draw_networkx(graph, pos=city_positions, with_labels=True)
    # set the window to full-screen
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    # display the window
    plt.show()

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
        64
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
    # get edges incident to the given node
    incident_edges = graph.edges(node)
    
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
    for edge in incident_edges:
        # find the angle between the upcoming node and this node
        possible_next_angle = findAngle(node, edge[1])
        
        # ensure that angle is positive
        if possible_next_angle < angle:
            possible_next_angle += 360
        # update the smallest angle and next edge if appropriate
        if smallest_angle is None or possible_next_angle < smallest_angle:
            next_edge = edge
            smallest_angle = possible_next_angle
            
    # return a tuple of the next edge, and all other edges excluding the next edge
    # and those edges connected to visited cities
    # the unused edges should be removed immediately upon return        
    return (next_edge, [rmv for rmv in incident_edges if rmv != next_edge \
                        and rmv[1] not in visited_cities])

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

def find_closest_outer_edge(inner_node):
    """
    Finds the closest edge on the existing circuit
    to the given node
    """
    
    # compare every visited edge
    closest_edge = None
    shortest_dist = None
    for edge in visited_edges:
        distance_to_edge = utils.find_shortest_distance(edge, city_positions[inner_node])
        if shortest_dist is None or distance_to_edge < shortest_dist:
            shortest_dist = distance_to_edge
            closest_edge = edge
    return closest_edge

def find_closest_inner_vertex(outer_edge):
    """
    Finds the closest inner vertex inside the existing circuit
    to the given circuit edge
    """
    closest_vertex = None
    shortest_dist = None
    #compare all inner vertices
    for inner_node in [node for node in graph.nodes() if node not in visited_cities]:
        distance_to_edge = utils.find_shortest_distance(outer_edge, city_positions[inner_node])
        if shortest_dist is None or distance_to_edge < shortest_dist:
            shortest_dist = distance_to_edge
            closest_vertex = inner_node
    return closest_vertex, shortest_dist

def choose_best_edge_deformation(inner_vertex):
    """
    In a list of edges, find the minimal-distance edge-deformation for a vertex 
    """
    best_dist = None
    best_edge = None
    for edge in visited_edges:
        # the positions of the two vertices of the edge
        P1 = city_positions[edge[0]]
        P2 = city_positions[edge[1]]
        # the inner vertex position
        V = city_positions[inner_vertex]
        # find the distance between the two points of the edge
        original_dist = utils.distance(P1, P2)
        # find the sum of the distances between the inner vertex and the edge's vertices
        new_dist = utils.distance(P1, V) + utils.distance(P2, V)
        # find the change in distance after deformation
        delta_dist = new_dist - original_dist
        if best_dist is None or delta_dist < best_dist:
            best_dist = delta_dist
            best_edge = edge
    return best_edge, best_dist
        
def solve_salesman():
    """
    Perform the algorithm, presenting the resulting solution plot at finish.
    """
    global visited_edges
    # select the first node
    current_city = find_most_western_vertex()
    print("INITIAL CITY: " + current_city)
    initial_city_nearest_edges = None

    # continue if we haven't visited any cities, or if we haven't
    # formed the outer circuit
    while len(visited_cities) == 0 or current_city!=visited_cities[0]:
        visited_cities.append(current_city)
        
        # get the possible edges to take, and the ones we can remove
        best_edge, rmv = determine_best_radial_neighbor(current_city)
        if len(visited_cities) > 1:
            graph.remove_edges_from(rmv)
        else:
            # Keep the initial city's edges for now;
            # we don't want to remove the last edge 
            # of the circuit by mistake
            initial_city_nearest_edges=rmv

        current_city = best_edge[1]
        visited_edges.append(best_edge)
        print("NEXT CITY: " + current_city)
    # Now that we found the final circuit edge, remove the edges of the first city that we saved.
    graph.remove_edges_from([rmv for rmv in initial_city_nearest_edges if  rmv[1] != visited_cities[1] \
    and rmv[1]!= visited_cities[-1]])
    # Also, remove the edges of all of the inner vertices. They're unimportant now.
    for vertex in graph.nodes():
        if vertex not in visited_cities:
            graph.remove_edges_from(graph.edges(vertex))
    
    # Connect the inner vertices
    while len(visited_cities) < CITIES: 
        next_best_vertex = None
        shortest_dist = None
        deformed_edge = None
        # find the best edge deformation for each vertex and compare.
        # The smallest change in distance for an edge deformation is the best choice
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
        # add the edges that occur from the edge deformation
        graph.add_edge(next_best_vertex, u)
        graph.add_edge(next_best_vertex, v)
        visited_edges.append((next_best_vertex, u))
        visited_edges.append((next_best_vertex, v))
        # add the new vertex to our visited cities
        visited_cities.append(next_best_vertex)

    draw_solution()
    
solve_salesman()
