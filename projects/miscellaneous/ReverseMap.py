__author__ = 'ubante'

"""
You have a list of objects, each have two fields, x & y.  Make a dictionary where the keys are the y's
and the values are a list of the x's with that y.

input:
x1,y1
x2,y2
x3,y3
x4,y3
x5,y5

output:
y1: x1
y2: x2
y3: x3,x4
y5: x5
"""

class Thing():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x is %s, y is %s" % (self.x, self.y)

# main
listThings = []
listThings.append(Thing("x1","y1"))
listThings.append(Thing("x2","y2"))
listThings.append(Thing("x3","y3"))
listThings.append(Thing("x4","y3"))
listThings.append(Thing("x5","y5"))

for thing in listThings:
    print thing

# here's the action
reversedThings = {}
for thing in listThings:
    # print thing.x
    if thing.y in reversedThings:
        reversedThings[thing.y].extend(thing.x)
    else:
        reversedThings[thing.y] = [thing.x]

print reversedThings


# {'y1': ['x1'], 'y3': ['x3'], 'y2': ['x2'], 'y5': ['x5']}
# {'y1': ['x1'], 'y3': ['x3', 'x4'], 'y2': ['x2'], 'y5': ['x5']}
