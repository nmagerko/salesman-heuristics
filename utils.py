import cities
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as transforms
import networkx as nx
import random

MILES_PER_DEGREE = 69
NUM_FIGURES = 0;

america_image = plt.imread('america1.png')    # Open image


def draw_graph(graph, city_positions, graph_type, rand=False):
    """
    Draws a city graph
    """
    if not rand:
        #Creates a new figure. The 'figsize' argument determines the size of the window.
        fig = plt.figure(num=graph_type.upper(), figsize=(10,8))
        ax1 = plt.subplot(111)
        ax1.imshow(america_image, zorder=0, extent=[-125, -67, 25, 50.5])
        ax1.set_aspect(1.3)

        # tell networkx to generate pyplot graph
        nx.draw_networkx(graph, pos=city_positions, style='solid', with_labels=True)
        # display the window
        plt.title("APPROXIMATE TOTAL DISTANCE: {0} miles".format(str(int(cities.compute_total_distance(graph, city_positions)))))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show(block=False)
    if rand:
        image = mpimg.imread('noah_prince.png')
        #Creates a new figure. The 'figsize' argument determines the size of the window.
        fig = plt.figure(num=graph_type.upper())
        ax = plt.subplot(111)

        # tell networkx to generate pyplot graph
        nx.draw_networkx(graph, pos=city_positions, style='solid', with_labels=False)
        # display the window
        plt.title("APPROXIMATE TOTAL DISTANCE: {0} miles".format(str(int(cities.compute_total_distance(graph, city_positions)))))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        # Render Dr. Prince's face as all of the nodes.
        pos=city_positions

        trans = ax.transData.transform
        trans2 = fig.transFigure.inverted().transform

        #height and width of the image
        h = 76.0
        w  = 78.0
        for each_node in graph:

            # figure coordinates
            xx, yy = trans(pos[each_node])
            # axes coordinates
            xa, ya = trans2((xx, yy))

            # this is the image size
            piesize_1 = (300.0 / (h*80))
            piesize_2 = (300.0 / (w*80))
            p2_2 = piesize_2 / 2
            p2_1 = piesize_1 / 2
            a = plt.axes([xa - p2_2, ya - p2_1, piesize_2, piesize_1])

            #display it
            a.imshow(image)
            #turn off the axis from minor plot
            a.axis('off')

        plt.show(block=False)

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
    return math.sqrt((MILES_PER_DEGREE * (node1[0] - node2[0]))**2 + (MILES_PER_DEGREE * (node1[1] - node2[1]))**2)

def total_weight(edges, city_positions):
    total = 0
    for edge in edges:
        total += distance(city_positions[edge[0]],city_positions[edge[1]])

    return total

def get_random_graph(n):
    """
    Generates a set of random vertices
    """
    graph = nx.Graph()
    pos = {}
    for i in range(n):
        x = 100*(random.random() - .5)
        y = 100*(random.random() - .5)
        cityName = str(x) + "," + str(y)
        cityPos = (x,y,)
        graph.add_node(cityName)
        pos[cityName] = cityPos
    return graph, pos
