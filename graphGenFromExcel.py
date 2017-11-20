#!/usr/bin/env python3
# coding: utf-8

"The scipt that creates graph from excel data."
import excel2Graph
import matplotlib.pyplot as plt
import networkx as nx
import argparse


def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(description="Generate GraphML file " +
                                     "from excel file.")
    parser.add_argument("-i", nargs="?", dest="input_file_name",
                        default="data/libdatasample.xlsx", metavar="filename",
                        help="input excel file name.")
    parser.add_argument("-o", nargs="?", dest="output_file_name",
                        default="example.graphml", metavar="filename",
                        help="output file name for generated GraphML file.")
    parser.add_argument("--show", action="store_true", dest="show_graph",
                        help="Show generated graph using matplotlib.")
    parser.add_argument("--node", nargs="?", dest="node",
                        default=6, metavar="column number",
                        help="Column number of data used to generate nodes.")
    parser.add_argument("--relation", nargs="?", dest="relation",
                        default=0, metavar="column number",
                        help="Column number of data used to build relations " +
                        "between nodes.")
    return parser.parse_args()


if __name__ == "__main__":
    args = cmdParse()
    print("Reading excel file into dataframe...")
    xlsxobj = excel2Graph.excel2Graph(args.input_file_name)
    print("Creating nodes...")
    nodes = xlsxobj.createNodeList(int(args.node))
    # print("Creating relation nodes...")
    # relation = xlsxobj.createNodeList(int(args.relation))
    # edges = xlsxobj.createEdgeList(int(args.node), nodes,
    #                                {int(args.relation): relation})
    # section = xlsxobj.separateByMonth()
    print("Generating edges...")
    # edges = xlsxobj.createEdgeListSection(int(args.node), nodes,
    #                                       {int(args.relation): relation},
    #                                       (0, 1000))
    edges = xlsxobj.fastEdgeList(int(args.node), int(args.relation))
    graph = xlsxobj.createGraph(nodes, edges)
    nx.draw(graph)
    nx.write_graphml(graph, args.output_file_name)
    print("Number of edges in graph: ", graph.number_of_edges())
    if args.show_graph:
        plt.show()
