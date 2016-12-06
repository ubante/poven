#!/usr/bin/env python

from __future__ import print_function

import os
import pydot
import sys


class PyGraph(object):

    def __init__(self, name="defaultpydotname"):
        self.pygraph = pydot.Dot(name)
        self.destination_svg_filename = "pygraph.svg"

    def add_edge(self, string1, string2):
        self.pygraph.add_edge(pydot.Edge(string1, string2))

    def add_node(self, string1):
        self.pygraph.add_node(pydot.Node(string1))

    def write_svg(self):
        self.pygraph.write_svg(self.destination_svg_filename)

        return "file://{}".format(os.path.abspath(self.destination_svg_filename))

    def load(self, graph):
        # origin = graphname.origin_node
        # [self.add_edge(origin.data, n.data) for n in origin.get_neighbors()]

        # for edge in graphname.get_edges():
        #     self.add_edge(edge)

        [self.add_edge(e[0], e[1]) for e in graph.get_edges()]



def main():

    p = PyGraph()
    p.add_edge("a", "b")
    p.add_node("soaloney")
    out = p.write_svg()
    print(out)

if __name__ == "__main__":
    main()
