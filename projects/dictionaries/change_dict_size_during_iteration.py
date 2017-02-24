d = {"one": [11, 12],
     "two": [21, 22],
     "list1": ["a", "b"],
     "list2": ["A", "B"]}

def loop(i):
    print "----------"
    print "LOOP ", i

    for outer in d:
        print
        print outer
        for inner in d[outer]:
            print inner

        if "a" in d[outer]:
            print "adding 'c'"
            the_list = d[outer]
            the_list.append('c')
            d[outer] = the_list

loop(1)
loop(2)
