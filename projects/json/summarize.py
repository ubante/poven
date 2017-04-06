from __future__ import print_function

import types


def summarize_element(element, limit_string=None, space_counter=0):
    """
    If element is a list or dictionary, loop through it recursing until
    you hit the limit string.

    :param element:
    :return:
    """
    m = 2  # Space multiplier.
    space_counter += 1
    if isinstance(element, (types.StringTypes, int, long, float, complex)):
        print("{}- {}".format(" " * m * space_counter, element))
        return

    for k in element:
        if isinstance(element, list):
            print("{}- It's a list.".format(" " * m * space_counter))
            summarize_element(k, space_counter=space_counter)
        elif isinstance(element, dict):
            print("{}- {} -- It's a dict.".format(" " * m * space_counter, k))
            summarize_element(element[k], space_counter=space_counter)


def main():
    print("List of dictionaries")
    ld = [{'aaa': 111}, {'bbb': 222}, {'ccc': 333}]
    summarize_element(ld)

    print("List of numbers")
    l = [1, 2, 3, 4, 5]
    summarize_element(l)

    print("Dictionary of numbers")
    d = {'aa': 11, 'bb': 22, 'cc': 33, 'dd': 44, 'ee': 55}
    summarize_element(d)

    print("List of lists of numbers")
    ll = [l, l]
    summarize_element(ll)

    print("List of dictionaries of numbers")
    ld = [d, d]
    summarize_element(ld)

    print("Dictionary of dictionaries of numbers")
    dd = {'d1': d, 'd2': d}
    summarize_element(dd)


if __name__ == "__main__":
    main()




