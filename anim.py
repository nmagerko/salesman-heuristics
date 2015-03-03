import cities
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

GRAPH_LIST = []
america_image = plt.imread('america1.png')    # Open image

fig = plt.figure(num='HEURISTIC', figsize=(10,8))
ax1 = fig.add_subplot(111)
#     
#     # tell networkx to generate pyplot graph
#     nx.draw_networkx(graph, pos=city_positions, style='solid', with_labels=True)
# set the window to full-screen
#manager = plt.get_current_fig_manager()
#manager.resize(*manager.window.maxsize())
# display the window

def add_graph(graph):
    GRAPH_LIST.append(graph.copy())
    
def update(frame_number):
    ax1.clear()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    if frame_number == len(GRAPH_LIST)-1:
        plt.title("APPROXIMATE TOTAL DISTANCE: {0} miles".format(str(int(cities.compute_total_distance(GRAPH_LIST[len(GRAPH_LIST)-1])))))
    ax1.imshow(america_image, zorder=0, extent=[-125, -67, 25, 50.5])
    ax1.set_aspect(1.3)
    current_graph = GRAPH_LIST[frame_number]
    nx.draw_networkx(current_graph, pos=cities.get_city_positions_safely(), style='solid', with_labels=True)
    
def init():
    ax1.imshow(america_image, zorder=0, extent=[-125, -67, 25, 50.5])
    ax1.set_aspect(1.3)
    
def show_graphs():
    anim = animation.FuncAnimation(fig, update, range(0, len(GRAPH_LIST)), interval=1, init_func=init, repeat_delay=5000)
    plt.show()