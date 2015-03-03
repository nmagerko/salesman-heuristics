import itertools
import networkx as nx
import utils

def bruteforce(graph, city_positions):
    """
    Find the shortest Hamiltonian path in a graph
    via bruteforce
    """    
    # keep track of our progress
    nodes_checked = 0
    total_nodes = len(graph.nodes())
    
    # store the lightest graph and its weight
    lightest_graph = None
    lightest_graph_weight = None

    for node in graph.nodes():
        # output progress
        print(str(nodes_checked/float(total_nodes)*100) + "%")
            
        # create a graph to work on
        G = nx.Graph()
        if not lightest_graph:
            G.add_nodes_from(graph)
        else:
            G.add_nodes_from(lightest_graph)
        G.remove_node(node)
        
        for perm in itertools.permutations(G.nodes(), total_nodes - 1):
            H = nx.Graph()
            H.add_nodes_from(perm)
            
            for i in range(len(perm)):
                if(i + 1 < len(perm)):
                    H.add_edge(perm[i],perm[i+1])
            H.add_node(node)
            H.add_edge(node,perm[0])
            H.add_edge(perm[-1],node)
            if not lightest_graph_weight or utils.total_weight(H.edges(), city_positions) < lightest_graph_weight:
                lightest_graph = H
                lightest_graph_weight = utils.total_weight(H.edges(), city_positions)
        nodes_checked += 1 
    print("100.0%")

    return lightest_graph