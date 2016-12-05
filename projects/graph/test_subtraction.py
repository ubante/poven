from __future__ import print_function


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
            print("-", self.data)

    def xdisplay_radially(self):
        self.display_stats()
        neighbors = self.get_neighbors()
        for neighbor in neighbors:
            neighbor.display_radially()

    def display_radially(self, caller=None):
        self.display_stats()
        for neighbor in self.get_other_neighbors(caller):
            neighbor.display_radially(self)



a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")
f = Node("f")
g = Node("g")
h = Node("h")
i = Node("i")
j = Node("j")
k = Node("k")
l = Node("l")
m = Node("m")
n = Node("n")

a.add_child(b)
a.add_child(c)
f.add_child(g)
f.add_parent(d)
d.add_child(e)
d.add_parent(b)

# a.print_neighbors()
c.add_child(h)
c.add_child(i)
i.add_parent(l)

a.print_neighbors()
d.print_neighbors()

# d.display_stats()
d.display_radially()  # qed