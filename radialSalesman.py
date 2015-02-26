'''
Created on Feb 25, 2015

@author: jreynolds
'''
import math
import cities
import matplotlib.pyplot as plt
import networkx as nx
import utils
from matplotlib.cbook import Null
import salesman

# the number of cities on our itinerary
CITIES = 16
# the number of alternative nearest neighbors to check
ALTERNATIVES = 3
# the number of nodes we want to work ahead
PREDICTION_CAP = 10

# get a random subgraph of the full cities graph
graph = utils.random_city_subgraph(cities.get_city_graph_safely(), CITIES)
# keep track of which edges we've included in our solution
visited_cities = []

last_edge = Null; 

city_positions = cities.get_city_positions_safely();

def draw_solution():
    """
    Draws the solution graph
    """
    city_positions = cities.get_city_positions_safely()
    nx.draw_networkx(graph, pos=city_positions, with_labels=True)
    plt.show()
    

solve_salesman_radially();