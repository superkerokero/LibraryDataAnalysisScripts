# -*- coding: utf-8 -*-
"""
excel2Graph.py
Read in excel file and convert its components into graph using pandas.
Graph is a collection of nodes and edges(connection of nodes).
"""

import pandas as pd
import sys
import os
import networkx as nx



class excel2Graph(object):
    "The class that handles excel->graph conversion."
    def __init__(self, file):
        "Constructor of the class."
        if os.path.exists(file):
            self.df = pd.read_excel(file)
        else:
            sys.exit("{0} doesn't exist!".format(file))
            
    def createNodeList(self, column):
        "Create a node list from the generated dataframe and given column."
        # create an empty node set.
        nodes = dict()
        for data in self.df.values:
            try:
                nodes[data[column]]["population"] += 1
            except KeyError:
                nodes[data[column]] = dict()
                nodes[data[column]]["population"] = 1
        return nodes

    def createEdgeList(self, col_nodes, nodes, relationships):
        """
        Create an edge list based on given node list and the relationship.
        The relationship is given as another column from the dataframe.
        "relationships" is a dictionary with key as the column number and
        value as intented set of keywords(can be another nodes element as
        well).
        e.g.
        nodes as title of the book;
        column as student major(science, engineering, medical, etc.)
        Generated edges with connect book titles that were borrowed from
        the same student major.
        """
        edges = dict()
        for key, value in relationships.items():
            for i, data in enumerate(self.df.values):
                start = data[col_nodes]
                for j, ref in enumerate(self.df.values):
                    end = ref[col_nodes]
                    related = (data[key] in value) and \
                              (data[key] == ref[key])
                    if i != j and related:
                        try:
                            edges[(start, end)]["weight"] += 1
                        except KeyError:
                            edges[(start, end)] = dict()
                            edges[(start, end)]["weight"] = 1
        return edges

    def createGraph(self, nodes, edges):
        "Create a graph object using given nodes and edges."
        G = nx.Graph()
        # Add nodes to the graph.
        G.add_nodes_from(nodes)
        # Add attributes to nodes.
        for a in nodes.keys():
            for attr in nodes[a]:
                G.node[a][attr] = nodes[a][attr]
        # Add edges to the graph.
        G.add_edges_from(edges.keys())
        # Add attributes to edges.
        for a, b in edges.keys():
            for attr in edges[(a, b)]:
                G[a][b][attr] = edges[(a, b)][attr]
        return G
