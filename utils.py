import math
import random
import cities

def distance(node1, node2):
    return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def total_weight(edges):
    total = 0
    for edge in edges:
        total += edge[2]['weight']

    return total

def random_city_subgraph(city_graph, number_of_nodes):
    all_nodes = set(city_graph.nodes())
    subgraph_nodes = random.sample(all_nodes, number_of_nodes)

    return city_graph.subgraph(subgraph_nodes)

def find_shortest_edge(graph):
    shortest_edge = None
    for edge in graph.edges():
        if shortest_edge is None or edge['weight'] < shortest_edge['weight']:
            shortest_edge=edge
    return shortest_edge

def find_shortest_distance(edge, node):
    city_positions = cities.get_city_positions_safely()
    C1, C2 = city_positions[edge[0]], city_positions[edge[1]] # edge endpoints
    x1, y1 = C1[0], C1[1] # endpoint coords
    x2, y2 = C2[0], C2[1]
    x0, y0 = node[0], node[1] # point not on edge

    # mathworld.wolfram.com/Point-LineDistance2-Dimensional.html
    numerator = abs( (x2-x1)*(y1-y0) - (x1-x0)*(y2-y1) )
    denominator = math.sqrt( (y2 - y1)**2 + (x2 - x1)**2 )

    mag = ( ( (x0-x1) * (x2-x1) ) + ( (y0-y1) * (y2-y1) ) )
    if(mag < 0) or (mag  > (x2-x1)**2+(y2-y1)**2): # Checks if closest point
                                                   # not on segment
        dist1 = distance(C1,node)
        dist2 = distance(C2,node)
        return min(dist2,dist1) # returns distance to closer endpoint
    else:
        return (numerator/denominator) # returns distance to closest point
                                       # between endpoints
