from nutslib import Nutleton
from nutslib import VerbosePrint


class SomethingDifferent:
    """Just to test VerbosePrint"""
    pass

def print_loop():
    v.print0("log level 0")
    v.print1("log level 1")
    v.print2("log level 2")
    v.print3("log level 3")


def main():
    # n = Nutleton()
    # print n.get_instance_nuts()
    # print Nutleton.class_str
    # print Nutleton.class_int


    # vprint without setting verbosity
    print "log level 1"
    print "log level 2"
    print "log level 3"
    print

    v = VerbosePrint
    print "\nSetting logging to level 1"
    v.print0("log level 0")
    v.print1("log level 1")
    v.print2("log level 2")
    v.print3("log level 3")


    # vprint after setting verbosity to 1

    # vprint after setting verbosity to 2
    # vprint after setting verbosity to 3
    # vprint after setting verbosity to 4


if __name__ == "__main__":
    main()
