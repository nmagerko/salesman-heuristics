import cities
import networkx as nx
import matplotlib.pyplot as plt

def save_graph(G, positions):
    # draw graph, with positions
    nx.draw(G, pos=positions)
    # save graph
    plt.savefig("output/all_cities.png")
    plt.show()

# draw example
save_graph(cities.get_city_graph_safely(), cities.get_city_positions_safely())
