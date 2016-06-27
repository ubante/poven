class Base(object):
    def __init__(self):
        self.lowest_score = 1
        self.classname = type(self).__name__
        self.reponame = "/a/b/" + self.classname
        # self.full_directory = self.


class ChildA(Base):
    def __init__(self, directory):
        super(ChildA, self).__init__()
        self.highest_score = 99
        self.directory = directory
        self.long_dir = "/a/b/" + self.directory + "/" + type(self).__name__


class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()
        self.highest_score = 83
        self.long_dir = "/x/y/" + type(self).__name__


class Results():
    pass


# can we add fields to a class?
class Map():
    def __init__(self):
        self.results = Results()

    def set_location(self):
        self.results.location = "SF"
        print "in set_location:", self.results.location

    def get_location(self):
        return self.results.location # ignore the Unresolved attribute blah blah blah
        # return "asdf"


directory = "c"
mChild = ChildA(directory)
print "Low: ", mChild.lowest_score
print "High:", mChild.highest_score

print "Classname: ", mChild.classname
print "RepoName:  ", mChild.reponame
print "LongName:  ", mChild.long_dir


qChild = ChildB()
print "Low: ", qChild.lowest_score
print "High:", qChild.highest_score

print "Classname: ", qChild.classname
print "RepoName:  ", qChild.reponame
print "LongName:  ", qChild.long_dir

print
aMap = Map()
aMap.set_location()
print "Location:  ", aMap.get_location()



