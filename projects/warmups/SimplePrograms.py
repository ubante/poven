'''
This is from https://wiki.python.org/moin/SimplePrograms
'''

print("Hello, world!")

print
import os
import sys
print(os.path.dirname(sys.executable))

# name = raw_input("What is your name?\n")
print
name = "tired of inputting"
print "Hi, %s." % name

# list?
print
friends = ["john", "patrick", "gar", "mikey"]
for i, name in enumerate(friends):
    print "iteration {iteration} is {name}".format(iteration=i, name=name)

# tuple
print
parents, babies = (1, 1)
while babies < 100:
    print "This generation has {0} babies and {0} parents".format(babies, parents)
    parents, babies = (babies, parents + babies)

# functions
print
def greet(name):
    print "Hello", name

greet("Jack")
greet("Jill")
greet("Bob")

# regex
print
import re
for test_string in ["555-1212", "123-456", "123-45678", "123-4567 ", "ILL-EGAL"]:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        print test_string, 'is a valid US number'
    else:
        print test_string, 'rejected'

# dictionaries
print
prices = {"apple": 0.40, "banana": 0.50}