import sys

import matplotlib

from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles

'''
For serious.
'''


def read_file(filename):
    try:
        f = open(filename)
    except IOError:
        print("Cannot open {}".format(filename))
        sys.exit()

    elements = set()
    for line in f:
        elements.add(line.strip())

    return elements


def write_to_file():
    pass


def make_diagram(a_set, b_set, c_set):
    # Find the size of elements unique to a set
    a_only_set = a_set - b_set - c_set
    b_only_set = b_set - c_set - a_set
    c_only_set = c_set - a_set - b_set
    print("{} elements in only A: {}".format(len(a_only_set), a_only_set))
    print("{} elements in only B: {}".format(len(b_only_set), b_only_set))
    print("{} elements in only C: {}".format(len(c_only_set), c_only_set))

    # Find the intersections between each pair of systems.
    ab_set = a_set & b_set - c_set
    ac_set = a_set & c_set - b_set
    bc_set = b_set & c_set - a_set
    print("{} elements in both A & B: {}".format(len(ab_set), ab_set))
    print("{} elements in both A & C: {}".format(len(ac_set), ac_set))
    print("{} elements in both B & C: {}".format(len(bc_set), bc_set))

    # Find the intersections between all the systems.
    abc_set = a_set & b_set & c_set
    print("{} elemements in all sets: {}\n".format(len(abc_set), abc_set))

    # Find the union of all the systems.
    union_set = a_set | b_set | c_set
    print("There are {} unique elements in the sets.".format(len(union_set)))

    # Something about python framework blah blah blah.
    matplotlib.use('TkAgg')

    # Set the size of the regions.  Not sure about the logic behind the
    # ordering here.
    s = (
        len(a_only_set),
        len(b_only_set),
        len(ab_set),
        len(c_only_set),
        len(ac_set),
        len(bc_set),
        len(abc_set)
    )

    # This is the diagram object that we will twiddle.
    v = venn3(subsets=s, set_labels=('A', 'B', 'C'))

    # The labels will be the size of the regions.  With three groups,
    # there will be seven regions.
    v.get_label_by_id('100').set_text(len(a_only_set))
    v.get_label_by_id('010').set_text(len(b_only_set))
    v.get_label_by_id('110').set_text(len(ab_set))
    v.get_label_by_id('001').set_text(len(c_only_set))
    v.get_label_by_id('101').set_text(len(ac_set))
    v.get_label_by_id('011').set_text(len(bc_set))
    v.get_label_by_id('111').set_text(len(abc_set))

    # Make some cosmetic settings.
    venn3_circles(subsets=s, linestyle='dotted')

    # Create the window with the graph
    plt.show()

    # Write the results out to files.  Should I wrap all of this into an
    # object?
    write_to_file()


def main():
    """
    This is where the magic happens.

    Stay classy with just three sets.
    :return:
    """

    # Read in the input files.
    a_set = read_file("systemA.txt")
    b_set = read_file("systemB.txt")
    c_set = read_file("systemC.txt")

    # Make the diagram.
    make_diagram(a_set, b_set, c_set)


if __name__ == "__main__":
    main()
