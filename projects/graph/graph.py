#!/usr/bin/env python

from __future__ import print_function

import sys

from pydotting import PyGraph

"""
This is a bidirectional graph of nodes.

I found this helpful:
https://www.codefellows.org/blog/implementing-a-singly-linked-list-in-python/
https://github.com/johnshiver/algorithms/blob/master/linked_list/linked_list.py
"""


class Node(object):

    def __init__(self, data=None):
        self.parent_list = []
        self.child_list = []
        self.data = data

    def get_neighbors(self):
        return self.parent_list + self.child_list

    def get_other_neighbors(self, node):
        """
        Return all the neighbors except node.

        This is useful when subtracting the calling node during a
        recursive loop.
        :param node:
        :return:
        """
        neighbors = self.get_neighbors()
        return list(set(neighbors) - set([node]))

    def add_child(self, child_node):
        # print("{} -> {}".format(self.data, child_node.data))
        self.child_list.append(child_node)
        # child_node.add_parent(self)
        child_node.parent_list.append(self)

    def add_parent(self, parent_node):
        # print("{} => {}".format(parent_node.data, self.data))
        self.parent_list.append(parent_node)
        # parent_node.add_child(self)
        parent_node.child_list.append(self)

    def print_neighbors(self):
        print("The neighbors of {}:".format(self.data))
        [print(n.data) for n in self.get_neighbors()]
        print("")

    def print_other_neighbors(self):
        print("The other neighbors of {}:".format(self.data))
        [print(n.data) for n in self.get_other_neighbors(self)]
        print("")

    def display_stats(self):
            print("- {} has {} neighbors"
                  .format(self.data, len(self.get_neighbors())))

    def display_radially(self, caller=None):
        self.display_stats()
        for neighbor in self.get_other_neighbors(caller):
            neighbor.display_radially(self)

    def search(self, data, caller=None):
        if self.data == data:
            return self

        # print("-- in {}; searching {} neighbors"
              # .format("xx", 99))
              # .format(self.data, len(self.get_other_neighbors(caller))))

        # commenting the below line breaks the script???
        # print("- searching", self.data)

        for neighbor in self.get_other_neighbors(caller):
            return neighbor.search(data, self)


class Graph(object):

    def __init__(self):
        self.origin_node = Node("origin-node")

    def add_child_to_origin(self, child_data):
        self.origin_node.add_child(Node(child_data))

    def add_child_to(self, parent_data, child_data):
        # Make sure that child doesn't already exist
        if self.origin_node.search(child_data):
            print("{} already exists - exiting."
                  .format(child_data))
            sys.exit()

        # Find parent node
        found_node = self.origin_node.search(parent_data)

        if found_node:
            print("Found the node: ", found_node.data)

            found_node.add_child(Node(child_data))
        else:
            print("Could not find a node with data: {}"
                  .format(parent_data))

    def display(self):
        self.origin_node.display_radially()


def print_banner(message):
    print("\n---- {} ----".format(message))


def main():
    print_banner("init")
    g = Graph()
    g.display()

    print_banner("add child")
    g.add_child_to_origin("child1")
    g.display()

    print_banner("add another child")
    g.add_child_to_origin("child2")
    g.display()

    print_banner("add child the hard way")
    g.add_child_to("origin-node", "child3")
    g.display()

    print_banner("add grandchildren")
    g.add_child_to("child1", "grandchild1a")
    g.display()

    print_banner("add another grandchildren")
    g.add_child_to("child1", "grandchild1b")
    g.display()

    print_banner("adding to non-existing node")
    g.add_child_to("dne", "fakechild")

    print_banner("add many more grandchildren")
    g.add_child_to("grandchild1b", "greatgrandchild1bA")
    g.add_child_to("grandchild1a", "greatgrandchild1aA")
    g.add_child_to("grandchild1a", "greatgrandchild1aB")
    g.add_child_to("child1", "grandchild1c")
    g.display()

    pg = PyGraph()
    pg.load(g)
    outfile = pg.write_svg()
    print(outfile)

    sys.exit()

if __name__ == "__main__":
    main()