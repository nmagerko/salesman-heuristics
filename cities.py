import json
import networkx as nx
import utils

cityDataRaw = \
'[ { "city":"Miami", "state":"FL", "latitude":25.785, "longitude":-80.271 }, {\
"city":"Seattle", "state":"WA", "latitude":47.597, "longitude":-122.335 }, {\
"city":"San Diego", "state":"CA", "latitude":32.779, "longitude":-117.14 }, {\
"city":"Augusta", "state":"ME", "latitude":44.322, "longitude":-69.777  }, {\
"city":"San Francisco", "state":"CA", "latitude":37.767, "longitude":-122.424\
}, { "city":"Sacramento", "state":"CA", "latitude":38.579, "longitude":-121.468\
}, { "city":"Los Angeles", "state":"CA", "latitude":34.044,\
"longitude":-118.302 }, { "city":"Portland", "state":"OR", "latitude":45.514,\
"longitude":-122.66 }, { "city":"Bend", "state":"OR", "latitude":44.034,\
"longitude":-121.334 }, { "city":"Spokane", "state":"WA", "latitude":47.673,\
"longitude":-117.386 }, { "city":"Las Vegas", "state":"NV", "latitude":36.151,\
"longitude":-115.185 }, { "city":"Boise", "state":"ID", "latitude":43.605,\
"longitude":-116.22 }, { "city":"Salt Lake City", "state":"UT",\
"latitude":40.723, "longitude":-111.896 }, { "city":"Tucson", "state":"AZ",\
"latitude":32.24, "longitude":-110.951 }, { "city":"Butte", "state":"MT",\
"latitude":45.959, "longitude":-112.558 }, { "city":"Denver", "state":"CO",\
"latitude":39.744, "longitude":-104.986 }, { "city":"Albuquerque",\
"state":"NM", "latitude":35.108, "longitude":-106.607 }, { "city":"Cheyenne",\
"state":"WY", "latitude":41.161, "longitude":-104.834 }, { "city":"Colorado\
Springs", "state":"CO", "latitude":38.852, "longitude":-104.765 }, {\
"city":"Amarillo", "state":"TX", "latitude":35.196, "longitude":-101.845 }, {\
"city":"Bismarck", "state":"ND", "latitude":46.817, "longitude":-100.733 }, {\
"city":"Dodge City", "state":"KS", "latitude":37.755, "longitude":-100.026 }, {\
"city":"Pierre", "state":"SD", "latitude":44.425, "longitude":-100.291 }, {\
"city":"San Antonio", "state":"TX", "latitude":29.472, "longitude":-98.511 }, {\
"city":"Lincoln", "state":"NE", "latitude":40.82, "longitude":-96.68 }, {\
"city":"Oklahoma City", "state":"OK", "latitude":35.474, "longitude":-97.522 },\
{ "city":"Dallas", "state":"TX", "latitude":32.815, "longitude":-96.802 }, {\
"city":"Minneapolis", "state":"MN", "latitude":44.979, "longitude":-93.314 }, {\
"city":"Des Moines", "state":"IA", "latitude":41.6, "longitude":-93.634 }, {\
"city":"Kansas City", "state":"KS", "latitude":39.102, "longitude":-94.683 }, {\
"city":"Houston", "state":"TX", "latitude":29.77, "longitude":-95.409 }, {\
"city":"Duluth", "state":"MN", "latitude":46.821, "longitude":-92.13 }, {\
"city":"Little Rock", "state":"AR", "latitude":34.741, "longitude":-92.332 }, {\
"city":"Milwaukee", "state":"WI", "latitude":43.046, "longitude":-87.962 }, {\
"city":"Springfield", "state":"IL", "latitude":39.791, "longitude":-89.646 }, {\
"city":"Chicago", "state":"IL", "latitude":41.868, "longitude":-87.682 }, {\
"city":"Memphis", "state":"TN", "latitude":35.117, "longitude":-89.951 }, {\
"city":"Louisville", "state":"KY", "latitude":38.212, "longitude":-85.692 }, {\
"city":"Gaylord", "state":"MI", "latitude":44.995, "longitude":-84.668 }, {\
"city":"Lansing", "state":"MI", "latitude":42.72, "longitude":-84.559 }, {\
"city":"Indianapolis", "state":"IN", "latitude":39.799, "longitude":-86.15 }, {\
"city":"Nashville", "state":"TN", "latitude":36.151, "longitude":-86.782 }, {\
"city":"Huntsville", "state":"AL", "latitude":34.713, "longitude":-86.622 }, {\
"city":"Birmingham", "state":"AL", "latitude":33.503, "longitude":-86.793 }, {\
"city":"Detroit", "state":"MI", "latitude":42.368, "longitude":-83.103 }, {\
"city":"Cleveland", "state":"OH", "latitude":41.461, "longitude":-81.665 }, {\
"city":"Columbus", "state":"OH", "latitude":39.999, "longitude":-82.99  }, {\
"city":"Atlanta", "state":"GA", "latitude":33.798, "longitude":-84.38 }, {\
"city":"Tallahassee", "state":"FL", "latitude":30.454, "longitude":-84.255 }, {\
"city":"Charleston", "state":"SC", "latitude":32.837, "longitude":-79.993 }, {\
"city":"Buffalo", "state":"NY", "latitude":42.909, "longitude":-78.829  }, {\
"city":"Pittsburgh", "state":"PA", "latitude":40.444, "longitude":-79.991 }, {\
"city":"Columbia", "state":"SC", "latitude":34.028, "longitude":-81.007 }, {\
"city":"Savannah", "state":"GA", "latitude":32.051, "longitude":-81.107 }, {\
"city":"Tampa", "state":"FL", "latitude":27.988, "longitude":-82.485 }, {\
"city":"Charleston", "state":"WV", "latitude":38.354, "longitude":-81.634 }, {\
"city":"Richmond", "state":"VA", "latitude":37.552, "longitude":-77.483 }, {\
"city":"Raleigh", "state":"NC", "latitude":35.821, "longitude":-78.655 }, {\
"city":"Albany", "state":"NY", "latitude":42.661, "longitude":-73.767 }, {\
"city":"Philadelphia", "state":"PA", "latitude":39.998, "longitude":-75.145 },\
{ "city":"Montpelier", "state":"VT", "latitude":44.262, "longitude":-72.583 },\
{ "city":"New York", "state":"NY", "latitude":40.753, "longitude":-73.983 }, {\
"city":"Concord", "state":"MA", "latitude":42.457, "longitude":-71.375  }, {\
"city":"Boston", "state":"MA", "latitude":42.336, "longitude":-71.079 }, {\
"city":"SAINT LOUIS", "state":"MO", "latitude":38.635, "longitude":-90.285 }, {\
"city":"FLOYD", "state":"VA", "latitude":36.91, "longitude":-80.309 }]'

# the graph of the cities
city_graph = None
# the positions of the cities (longitude, latitude)
city_graph_pos = {}

def compute_total_distance(city_graph):
    """
    Computes the total distance of a city graph
    in estimated miles
    """
    total_distance = 0.0
    for edge in city_graph.edges():
        global city_graph_pos
        total_distance += utils.distance_miles(city_graph_pos[edge[0]], \
                                               city_graph_pos[edge[1]])
    
    return total_distance

def add_city_edges():
    """
    Adds edges to city graph
    """
    global city_graph
    nodes_to_connect = nx.nodes(city_graph)
    for node in nodes_to_connect:
        non_neighbors = nx.non_neighbors(city_graph, node)
        for non_neighbor in non_neighbors:
            city_graph.add_edge(node, non_neighbor);

def get_city_graph_safely():
    """
    Provides the city_graph, generating it if the graph does not already exist
    """
    global city_graph
    global city_graph_pos
    if not city_graph:
        city_graph = nx.Graph()
        for data in json.loads(cityDataRaw):
            cityName = ", ".join((data['city'].title(), data['state']))
            cityPos = (data['longitude'], data['latitude'],)
            city_graph_pos[cityName] = cityPos
            
            city_graph.add_node(cityName)
        add_city_edges()
    return city_graph

def get_city_positions_safely():
    """
    Provides the mappings of the cities to their geographical locations, in
    the form (longitude, latitude)
    """
    global city_graph_pos
    if not city_graph_pos:
        raise "City positions were empty. Generate the city graph first"
    return city_graph_pos