import cities
import math
import matplotlib.pyplot as plt
import networkx as nx
import random

MILES_PER_LATITUDE_DEGREE = 68.71
MILES_PER_LONGITUDE_DEGREE = 69.17 
NUM_FIGURES = 0;

america_image = plt.imread('america1.png')    # Open image


def draw_graph(graph, city_positions, graph_type):
    """
    Draws a city graph
    """
    plt.figure(graph_type.upper())
    plt.imshow(america_image, zorder=0, extent=[-125, -67, 25, 50.5])
    # tell networkx to generate pyplot graph
    nx.draw_networkx(graph, pos=city_positions, style='solid', with_labels=True)
    # set the window to full-screen
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    # display the window
    plt.title("APPROXIMATE TOTAL DISTANCE: {0} miles".format(str(int(cities.compute_total_distance(graph)))))
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

def show_graphs():
    plt.show()

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
    return math.sqrt((MILES_PER_LONGITUDE_DEGREE * (node1[0] - node2[0]))**2 + (MILES_PER_LATITUDE_DEGREE * (node1[1] - node2[1]))**2)

def total_weight(edges, city_positions):
    total = 0
    for edge in edges:
        total += distance(city_positions[edge[0]],city_positions[edge[1]])

    return total