import datatrater as dt
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
from api_calls import FlightSearch

class ItineraryGraph:
    def __init__(self, orig, dest):
        self.orig = orig
        self.dest = dest
        self.api = FlightSearch()
        self.list_orig = self.api.airport_routes(orig)
        self.list_dest = self.api.airport_routes(dest)
        self.iterate = list(set(self.list_orig + self.list_dest))
        self.nodes = self.iterate
        self.G = nx.Graph()

    def generate_nodes(self):
        print("Generating nodes...")
        for i in self.iterate:
            try:
                aux = self.api.airport_routes(i)
                # add aux elements to nodes only if it is not already in nodes
                self.nodes = list(set(self.nodes + aux))
                # make a pause of 100ms
                time.sleep(0.1)
            except:
                continue

    def add_nodes_to_graph(self):
        print("Adding nodes to the graph...")
        self.G.add_nodes_from(self.nodes)

    def create_itinerary_graph(self):
        '''
        Creates a graph with the origin and destination as nodes and the weight of the edge
        as the price of the flight
        '''

        self.generate_nodes()
        self.add_nodes_to_graph()

        # Add edges
        for node in self.nodes:
            try:
                response = self.api.get_prices(self.orig, node, "2023-11-11", encode=False)
                prices = response['total'].to_list()
                # convert prices to integers
                prices = list(map(int, prices))
                # get the average price
                price = int(np.mean(prices))
                # add edge to graph
                self.G.add_edge(self.orig, node, weight=price)
                # make a pause of 100ms
                time.sleep(0.1)
            except:
                continue

        for node in self.nodes:
            try:
                response = self.api.get_prices(node, self.dest, "2023-11-11", encode=False)
                prices = response['total'].to_list()
                # convert prices to integers
                prices = list(map(int, prices))
                # get the average price
                price = int(np.mean(prices))
                # add edge to graph
                self.G.add_edge(node, self.dest, weight=price)
                # make a pause of 100ms
                time.sleep(0.1)
            except:
                continue
