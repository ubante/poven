from projects.classes.Fruit import Fruit

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


class Papple(Fruit):

    def __init__(self):
        Fruit.__init__(self, "papple")
        print "A papple isa apple"



