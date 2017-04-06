def afunc(alist, ctr=0, groceries=[]):
    aval = alist.pop()

    print("{}. {}".format(ctr, groceries))
    if ctr == 5:
        print("{}".format(" -> ".join(groceries)))
    else:
        ctr += 1
        # groceries.append(aval)
        afunc(alist, ctr, groceries + [aval])


alist = ["a", "b", "c", "d", "e", "F", "G"]
afunc(alist)

