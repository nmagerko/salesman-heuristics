import math
import random

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
            shortest_edge=edge;
    return shortest_edge;