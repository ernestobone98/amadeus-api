import datatrater as dt
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(dt.get_airport_iata_code())

# demo weights for debbuging
G.add_edge('MAD', 'BCN', weight=5.0)
G.add_edge('MAD', 'ATH', weight=9.0)
G.add_edge('MAD', 'CDG', weight=15.0)
G.add_edge('MAD', 'LHR', weight=20.0)
G.add_edge('MAD', 'FCO', weight=25.0)
G.add_edge('MAD', 'MXP', weight=30.0)
G.add_edge('MAD', 'AMS', weight=35.0)

# Define the positions of nodes for drawing
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos)

labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()