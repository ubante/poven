'''
This is from https://wiki.python.org/moin/SimplePrograms
'''

print("Hello, world!")

import os
import sys
print(os.path.dirname(sys.executable))

# name = raw_input("What is your name?\n")
name = "tired of inputting"
print "Hi, %s." % name

# list?
friends = ["john", "patrick", "gar", "mikey"]
for i, name in enumerate(friends):
    print "iteration {iteration} is {name}".format(iteration=i, name=name)

# tuple
parents, babies = (1, 1)
while babies < 100:
    print "This generation has {0} babies and {0} parents".format(babies, parents)
    parents, babies = (babies, parents + babies)