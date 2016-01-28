import sys, getopt, re

"""
This will either dump the current relationships or add a new relationship.
"""


def usage():
    usagemessage = '''
Usage: runner.py -d
       runner.py -s SERVICENAME [-l LABELNAME] [-p PARENTNAME]
       runner.py -r RULE

In the first form, the -d option dumps the list of services and their relationships.

In the second form, SERVICENAME should be a unique name.  You can use -d to see if SERVICENAME already exists.  If you
want SERVICENAME to be displayed with a different label, you can use the optional -l option.  If the service is has no
dependencies and blocks no other services, then you do not need to use the -p option.  If the service depends on
another service, use the -p option.  If you do not know the parent service's name use the -d option to find it.

In the third form, RULE will be human grammar.  The below sytax is currently acceptable:
   * PropA exists in ColoA
   * PropA exists in (ColoA, ColoB, UHM)
   * PropA needs no other property
   * PropA in ColoA needs PropB in ColoB
   * PropA needs PropB in same colo
'''

    print (usagemessage)
    sys.exit()

def dump_services():
    pass

def main(argv):
    servicename = ""
    labelname = ""
    parentname = ""
    opts = []
    try:
        opts, args = getopt.getopt(argv,"hds:l:p:")
    except getopt.GetoptError:
        # print 'test.py -i <inputfile> -o <outputfile>'
        # sys.exit(2)
        usage()
    for opt, arg in opts:
        if opt == '-h':
            # print 'test.py -i <inputfile> -o <outputfile>'
            # sys.exit()
            usage()
        elif opt in ("-d"):
            dump_services()
        elif opt in ("-s"):
            servicename = arg
        elif opt in ("-l"):
            labelname = arg
        elif opt in ("-p"):
            parentname = arg

    # Case with no other options
    if not labelname and not servicename and not parentname:
        usage()

    # if labelname and not servicename or :
    if not servicename and (parentname or labelname):
        print ("You need to include a SERVICENAME.")
        usage()

    print ("You gave a service name of %s" % servicename)
    if labelname:
        print ("- with a label name of %s" % labelname)
    if parentname:
        print ("- with a parent name of %s" % parentname)



if __name__ == "__main__":
   main(sys.argv[1:])
