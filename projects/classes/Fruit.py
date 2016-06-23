class Fruit:

    def __init__(self, name):
        self.name = name
        self.count = 0

    def increment_count(self):
        self.count += 1

    def print_status(self):
        print "-- You have %d %ss" % (self.count, self.name)




