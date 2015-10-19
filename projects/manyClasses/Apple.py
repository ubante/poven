class Apple:
    count = 0

    def __init__(self):
        print "Have an apple"
        self.incrementCount()

    def incrementCount(self):
        self.count = self.count + 1

    def printState(self):

        if 1 == self.count:
            print "You have 1 apple"
            return

        print "You have %s apples" % self.count

class Papple:

    def __init__(self):
        print "A papple isa apple"