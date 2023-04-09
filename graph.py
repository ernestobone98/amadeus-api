import datatrater as dt
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import api_calls as api


# G = nx.Graph()

# G.add_nodes_from(dt.get_airport_iata_code())

# # demo weights for debbuging
# G.add_edge('MAD', 'BCN', weight=5.0)
# G.add_edge('MAD', 'ATH', weight=9.0)
# G.add_edge('MAD', 'CDG', weight=15.0)
# G.add_edge('MAD', 'LHR', weight=20.0)
# G.add_edge('MAD', 'FCO', weight=25.0)
# G.add_edge('MAD', 'MXP', weight=30.0)
# G.add_edge('MAD', 'AMS', weight=35.0)

# # Define the positions of nodes for drawing
# pos = nx.spring_layout(G)

# # Draw the graph
# nx.draw(G, pos)

# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# nx.write_graphml(G, "itinerary_weighted_graph.graphml")

# plt.show()

# Function working but raises Amadeus error: Departure airport code is not supported
def create_itinerary_graph(orig, dest):
    '''
    Creates a graph with the origin and destination as nodes and the weight of the edge
    as the price of the flight
    '''

    list_orig = api.airport_routes(orig)
    list_dest = api.airport_routes(dest)

    nodes = list(set(list_orig + list_dest))

    # print("nodes : ",nodes)

    for i in nodes:
        print("i : ",i)
        print("typeof i : ", type(str(i)))
        print("iata : ", type('ACE'))

        aux = api.airport_routes(i)
        # add aux elements to nodes only if it is not already in nodes
        nodes = list(set(nodes + aux))
        # make a pause of 100ms
        time.sleep(0.1)

    print(nodes)
    # G = nx.Graph()
    # G.add_nodes_from()

    # return G

create_itinerary_graph('MAD', 'BCN')