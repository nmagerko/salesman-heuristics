import math
import random

MILES_PER_DEGREE = 69

def random_subgraph(graph, number_of_nodes):
    """
    Creates a random subgraph from the given graph
    """
    all_nodes = set(graph.nodes())
    subgraph_nodes = random.sample(all_nodes, number_of_nodes)

    return graph.subgraph(subgraph_nodes)

def distance(node1, node2):
    """
    Finds the distance between node1 and node2
    """
    return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def distance_miles(node1, node2):
    """
    Finds the distance between node1 and node2 in miles
    """
    return math.sqrt((MILES_PER_DEGREE * (node1[0] - node2[0]))**2 + (MILES_PER_DEGREE * (node1[1] - node2[1]))**2)