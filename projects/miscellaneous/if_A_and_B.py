"""
There's A, B, and other.  Other is, like, everything.
"""

def is_similar(p, q):
    return is_different(p, q)

    print "Comparing {} and {}:".format(p, q),
    # if ("a" == p) and ("b" == q):
    if (("a" == p) and ("b" == q)) or (("a" == q) and ("b" == p)):
        print "False"
        return False
    else:
        print "True"
        return True


def is_different(p, q):
    print "Comparing {} to {}:".format(p, q),
    if (("a" == p) and ("b" == q)) or (("a" == q) and ("b" == p)):
        print "different"
        return True
    else:
        print "same"
        return False


a1 = "a"
a2 = "a"
b1 = "b"
b2 = "b"
x = "x"
y = "y"
ll = "ll"

# if is_similar(a1, a2):
#     print "same"
# else:
#     print "different"

is_similar(a1, a2)
is_similar(a1, b1)
is_similar(a1, b2)
is_similar(a1, x)
is_similar(y, x)
is_similar(ll, x)
is_similar(x, x)
is_similar(b2, x)


