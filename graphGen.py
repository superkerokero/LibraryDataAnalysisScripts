#!/usr/bin/env python3
# coding: utf-8

"The scipt that handles csv input."
import csv2Graph
import matplotlib.pyplot as plt
import networkx as nx
import argparse


def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(description="Generate GraphML file " +
                                     "from csv file.")
    parser.add_argument("-i", nargs="?", dest="input_file_name",
                        default="data/libsample.csv", metavar="filename",
                        help="input csv file name.")
    parser.add_argument("-o", nargs="?", dest="output_file_name",
                        default="example.graphml", metavar="filename",
                        help="output file name for generated GraphML file.")
    parser.add_argument("--show", action="store_true", dest="show_graph",
                        help="Show generated graph using matplotlib.")
    parser.add_argument("--node", nargs="?", dest="node",
                        default=7, metavar="column number",
                        help="Column number of data used to generate nodes.")
    parser.add_argument("--relation", nargs="?", dest="relation",
                        default=11, metavar="column number",
                        help="Column number of data used to build relations " +
                        "between nodes.")
    return parser.parse_args()


if __name__ == "__main__":
    args = cmdParse()
    csvobj = csv2Graph.csv2Graph(args.input_file_name)
    nodes = csvobj.createNodeList(int(args.node))
    relation = csvobj.createNodeList(int(args.relation))
    edges = csvobj.createEdgeList(nodes, {int(args.relation): relation})
    graph = csvobj.createGraph(nodes, edges)
    nx.draw(graph)
    nx.write_graphml(graph, args.output_file_name)
    print("Number of edges in graph: ", graph.number_of_edges())
    if args.show_graph:
        plt.show()
