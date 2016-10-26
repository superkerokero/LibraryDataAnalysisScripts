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
                # Add other attributes for the first time.
                nodes[data[column]]["major"] = data[9]
                nodes[data[column]]["grade"] = data[7]
                nodes[data[column]]["state"] = data[8]
        return nodes

    def findRelation(self, col_nodes, col_relation):
        "Find related data by given relationship and save them in a list."
        edge_raw = dict()
        for data in self.df.values:
            try:
                edge_raw[data[col_relation]].append(data[col_nodes])
            except KeyError:
                edge_raw[data[col_relation]] = list()
                edge_raw[data[col_relation]].append(data[col_nodes])
        return edge_raw

    def createEdgeListFromRaw(self, raw):
        "Generate edge list from raw edge list."
        edges = dict()
        for data in raw.values():
            if len(data) > 1:
                for i in range(len(data)):
                    for j in range(i, len(data)):
                        try:
                            edges[(data[i], data[j])]["weight"] += 1
                        except KeyError:
                            edges[(data[i], data[j])] = dict()
                            edges[(data[i], data[j])]["weight"] = 1
        return edges

    def fastEdgeList(self, col_nodes, col_relation):
        "Fast version of EdgeList generation. O(n)"
        raw = self.findRelation(col_nodes, col_relation)
        print("Raw edge list generation completed. Start translation...")
        edges = self.createEdgeListFromRaw(raw)
        return edges

    def createEdgeList(self, col_nodes, nodes, relationships,
                       date_column=14, date_limit=20241003):
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
                if data[date_column] > date_limit:
                    break
                for j, ref in enumerate(self.df.values):
                    if ref[date_column] > date_limit:
                        break
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

    def createEdgeListSection(self, col_nodes, nodes, relationships, section):
        "Same as createEdgeList except only at designated section."
        edges = dict()
        for key, value in relationships.items():
            for i in range(section[0], section[1]+1):
                data = self.df.values[i]
                start = data[col_nodes]
                for j in range(section[0], section[1]+1):
                    ref = self.df.values[j]
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

    @staticmethod
    def findDate(date):
        "Convert integer date into date tuple."
        raw = str(date)
        year = int(raw[0:4])
        month = int(raw[4:6])
        day = int(raw[6:])
        return (year, month, day)

    def separateByMonth(self, date_column=14):
        "Generate range tuples for separating the graph by different months."
        max_line = len(self.df.values) - 1
        separate = list()
        start = 0
        previous = self.findDate(self.df.values[0][date_column])[1]
        for i, data in enumerate(self.df.values):
            current = self.findDate(data[date_column])[1]
            if previous != current:
                separate.append((start, i-1))
                start = i
            previous = current
            if i == max_line:
                separate.append((start, i-1))
        return separate

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
