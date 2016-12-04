#!/usr/bin/env python


class Node(object):

    def __init__(self):
        self.parent_list = []
        self.child_list = []
        self.data = None

    def set_data(self, data):
        self.data = data

    def add_child(self, child_node):
        self.child_list.append(child_node)

    def add_parent(self, parent_node):
        self.parent_list.append(parent_node)

    def display(self):
        print(self.data)


class Graph(object):

    def __init__(self):
        self.head_node = Node()
        self.head_node.set_data("headnode")

    def add_child_to_head(self, child_data):
        child_node = Node()
        child_node.set_data(child_data)

        self.head_node.add_child(child_node)

    def insert_child(self, parent_data, child_data):
        # Find parent node

        # Add child node
        pass

    def display(self):
        self.head_node.display()

        for child in self.head_node.child_list:
            child.display()


def main():
    g = Graph()
    g.add_child_to_head("child1")


    g.display()

if __name__ == "__main__":
    main()