#!/usr/bin/env python

import argparse
import logging
import sys
import yaml

import matplotlib

from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles

'''
This will take three files and make a Venn diagram.

The filenames will be used as the titles and each file should be a
singlet list.

Example:
  ./generator.py -f systemA.txt,systemB.txt,systemC.txt -vv
'''


def read_file(filename):
    try:
        f = open(filename)
    except IOError as ioe:
        logging.fatal("Cannot open {}; exiting.".format(filename))
        logging.debug(ioe)
        sys.exit()

    elements = set()
    for line in f:
        elements.add(line.strip())

    return elements


def write_to_file(region_dict, outputfile):
    print("Writing to {}:".format(outputfile))
    logging.debug(region_dict)

    with open(outputfile, 'w') as outfile:
        yaml.dump(region_dict, outfile, default_flow_style=True)


def make_diagram(a_set, b_set, c_set, filenames):

    # Find the size of elements unique to a set
    a_only_set = a_set - b_set - c_set
    b_only_set = b_set - c_set - a_set
    c_only_set = c_set - a_set - b_set
    print("{} elements in only {}: {}".format(len(a_only_set), filenames[0], a_only_set))
    print("{} elements in only {}: {}".format(len(b_only_set), filenames[1], b_only_set))
    print("{} elements in only {}: {}".format(len(c_only_set), filenames[2], c_only_set))

    # Record this for later writing.
    region_dict = {}
    region_dict['only'] = {}
    region_dict['only'][filenames[0]] = a_only_set
    region_dict['only'][filenames[1]] = b_only_set
    region_dict['only'][filenames[2]] = c_only_set

    # Find the intersections between each pair of systems.
    ab_set = a_set & b_set - c_set
    ac_set = a_set & c_set - b_set
    bc_set = b_set & c_set - a_set
    print("{} elements in both {} & {}: {}"
          .format(len(ab_set), filenames[0], filenames[1], ab_set))
    print("{} elements in both {} & {}: {}"
          .format(len(ac_set), filenames[0], filenames[2], ac_set))
    print("{} elements in both {} & {}: {}"
          .format(len(bc_set), filenames[1], filenames[2], bc_set))

    region_dict['double'] = {}
    region_dict['double']["{}_and_{}".format(filenames[0], filenames[1])] = ab_set
    region_dict['double']["{}_and_{}".format(filenames[0], filenames[2])] = ac_set
    region_dict['double']["{}_and_{}".format(filenames[1], filenames[2])] = bc_set

    # Find the intersections between all the systems.
    abc_set = a_set & b_set & c_set
    print("{} elements in all sets: {}\n".format(len(abc_set), abc_set))

    region_dict['common'] = {}
    region_dict['common']['all'] = abc_set

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
    # v = venn3(subsets=s, set_labels=('A', 'B', 'C'))
    v = venn3(subsets=s, set_labels=filenames)

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

    return region_dict


def main():
    """
    This is where the magic happens.

    Stay classy with just three sets.
    :return:
    """
    parser = argparse.ArgumentParser(description="Make a Venn Diagaram.")
    parser.add_argument("-f", "--files",
                         help="Comma separated list of three files to graph.")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    parser.add_argument("-o", "--outputfile",
                        help="(optional) Write out results to OUTPUTFILE.")
    args = parser.parse_args()

    # Let there be debug.
    if args.verbose >= 2:
        args.verbose = 2
        logging_level = logging.DEBUG
    elif args.verbose == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    stdout_sh = logging.StreamHandler(sys.stdout)
    stdout_sh.setLevel(logging.DEBUG)
    stdout_formatter = logging.Formatter('%(levelname)s - %(message)s')
    stdout_sh.setFormatter(stdout_formatter)
    root_logger.addHandler(stdout_sh)

    # Exit if we get no files.
    if not args.files:
        logging.fatal("No given filenames.")
        parser.print_usage()
        parser.exit(1)

    filenames = args.files.split(',')
    logging.debug("Given {} {} {}.".format(filenames[0], filenames[1], filenames[2]))

    # Read in the input files.
    a_set = read_file(filenames[0])
    b_set = read_file(filenames[1])
    c_set = read_file(filenames[2])

    # Make the diagram.
    results = make_diagram(a_set, b_set, c_set, filenames)

    if args.outputfile:
        write_to_file(results, args.outputfile)

if __name__ == "__main__":
    main()

"""
$ ./generator.py -f systemA.txt,systemB.txt,systemC.txt -vv -o outfile.yaml
DEBUG - Given systemA.txt systemB.txt systemC.txt.
2 elements in only systemA.txt: set(['cowA2', 'cowA1'])
4 elements in only systemB.txt: set(['cowB2', 'cowB3', 'cowB1', 'cowB4'])
7 elements in only systemC.txt: set(['cowC1', 'cowC3', 'cowC2', 'cowC5', 'cowC4', 'cowC7', 'cowC6'])
2 elements in both systemA.txt & systemB.txt: set(['cowAB2', 'cowAB1'])
1 elements in both systemA.txt & systemC.txt: set(['cowAC1'])
0 elements in both systemB.txt & systemC.txt: set([])
4 elements in all sets: set(['cowABC4', 'cowABC2', 'cowABC3', 'cowABC1'])

There are 20 unique elements in the sets.
Writing to outfile.yaml:
DEBUG - {'double': {'systemB.txt_and_systemC.txt': set([]), 'systemA.txt_and_systemB.txt': set(['cowAB2', 'cowAB1']), 'systemA.txt_and_systemC.txt': set(['cowAC1'])}, 'only': {'systemA.txt': set(['cowA2', 'cowA1']), 'systemC.txt': set(['cowC1', 'cowC3', 'cowC2', 'cowC5', 'cowC4', 'cowC7', 'cowC6']), 'systemB.txt': set(['cowB2', 'cowB3', 'cowB1', 'cowB4'])}, 'common': {'all': set(['cowABC4', 'cowABC2', 'cowABC3', 'cowABC1'])}}
"""






