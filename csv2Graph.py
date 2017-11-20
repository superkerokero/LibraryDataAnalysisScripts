# -*- coding: utf-8 -*-
"""
csv2Graph.py
Read in csv file and convert its components into graph.
Graph is a collection of nodes and edges(connection of nodes).
"""

import csv
import sys
import networkx as nx


class csv2Graph(object):
    """
    The class that handles csv file related I/O processes.
    """
    def __init__(self, file):
        """
        Constructor of the class.
        Read data from given csv file and store it in a list.
        """
        try:
            # Open csv file with shift-jis encoding for Japanese support.
            with open(file, encoding='shift-jis') as csvfile:
                csvdata = csv.reader(csvfile, dialect='excel')
                # rawdata contains 2 dicts.
                # dict[0] is column-based.
                # dict[1] is row-based.
                rawdata = [dict(), dict()]
                for linum, row in enumerate(csvdata):
                    # first line doesn't contain useful data.
                    if linum == 0:
                        continue
                    for rank, data in enumerate(row):
                        # Add column-based data.
                        try:
                            rawdata[0][rank].append(data)
                        except KeyError:
                            rawdata[0][rank] = list()
                            rawdata[0][rank].append(data)
                        # Add row-based data.
                        # For consistency, linum - 1 is used for numbering.
                        try:
                            rawdata[1][linum-1].append(data)
                        except KeyError:
                            rawdata[1][linum-1] = list()
                            rawdata[1][linum-1].append(data)
            self.rawdata = rawdata
        except IOError:
            sys.exit("File \'{0}\' open failed!\n".format(file) +
                     "Check if the file name is correct.\n")

    def createNodeList(self, column):
        "Create a node list from the generated rawdata and given column."
        # create an empty node set.
        nodes = dict()
        for data in self.rawdata[0][column]:
            if data != "":
                try:
                    nodes[data]["population"] += 1
                except KeyError:
                    nodes[data] = dict()
                    nodes[data]["population"] = 1
        return (column, nodes)

    def createEdgeList(self, nodes, relationships):
        """
        Create an edge list based on given node list and the relationship.
        The relationship is given as another column from the rawdata.
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
            for i in range(len(self.rawdata[1])):
                start = self.rawdata[1][i]
                for j in range(len(self.rawdata[1])):
                    end = self.rawdata[1][j]
                    included = (start[nodes[0]] in nodes[1]) and \
                               (end[nodes[0]] in nodes[1])
                    related = (start[key] in value[1]) and \
                              (start[key] == end[key])
                    if i != j and related and included:
                        try:
                            edges[(start[nodes[0]],
                                  end[nodes[0]])]["weight"] += 1
                        except KeyError:
                            edges[(start[nodes[0]], end[nodes[0]])] = dict()
                            edges[(start[nodes[0]],
                                  end[nodes[0]])]["weight"] = 1
        return edges

    def createGraph(self, nodes, edges):
        "Create a graph object using given nodes and edges."
        G = nx.Graph()
        # Add nodes to the graph.
        G.add_nodes_from(nodes[1])
        # Add attributes to nodes.
        for a in nodes[1].keys():
            for attr in nodes[1][a]:
                G.node[a][attr] = nodes[1][a][attr]
        # Add edges to the graph.
        G.add_edges_from(edges.keys())
        # Add attributes to edges.
        for a, b in edges.keys():
            for attr in edges[(a, b)]:
                G[a][b][attr] = edges[(a, b)][attr]
        return G
