import cities
import networkx as nx
import matplotlib.pyplot as plt
import utils

def save_graph(G, positions):
    # draw graph, with positions
    nx.draw(G, pos=positions, with_labels=True)
    # save graph
    # plt.savefig("output/all_cities.png")
    plt.show()

# draw example
subgraph = utils.random_city_subgraph(cities.get_city_graph_safely(), 6)
city_positions = cities.get_city_positions_safely()

save_graph(subgraph, city_positions)
