from Results import Results


class Cat:
    def __init__(self):
        self.age = 3  # years
        self.total_results = Results()

    def age_squarer(self):
        r = Results()

        age2 = self.age * self.age
        r.add("age squared is " + str(age2))

        self.total_results.extend(r)
        return r

    def age_ager(self):
        r = Results()

        r.add2("Incrementing age by one year from " + str(self.age))
        self.age += 1

        if self.age == 10:
            r.add3("Age hit a decade boundary")

        self.total_results.extend(r)
        # print "age is {} and results size is {}".format(self.age,
        #                                                 self.total_results.get_size())
        return r

# main

print_level = 3

bugger = Cat()
res = bugger.age_squarer()

for i in range(1, 12):
    res.extend(bugger.age_ager())

# res.display3()


if print_level == 1:
    print "\nLevel 1"
    res.display()
elif print_level == 2:
    print "\nLevel 2"
    res.display2()
elif print_level == 3:
    print "\nLevel 3"
    res.display3()
else:
    print "unknown print_level"

# res.dump()

"""
1:
Age hit a decade boundary

Level 1
age squared is 9

2:
Age hit a decade boundary

Level 2
Start results
age squared is 9
Start results
Incrementing age by one year from 3
Start results
Incrementing age by one year from 4
Start results
Incrementing age by one year from 5
Start results
Incrementing age by one year from 6
Start results
Incrementing age by one year from 7
Start results
Incrementing age by one year from 8
Start results
Incrementing age by one year from 9
Start results
Incrementing age by one year from 10
Start results
Incrementing age by one year from 11
Start results
Incrementing age by one year from 12
Start results
Incrementing age by one year from 13

3:
Age hit a decade boundary

Level 3
Start results
age squared is 9
Start results
Incrementing age by one year from 3
Start results
Incrementing age by one year from 4
Start results
Incrementing age by one year from 5
Start results
Incrementing age by one year from 6
Start results
Incrementing age by one year from 7
Start results
Incrementing age by one year from 8
Start results
Incrementing age by one year from 9
Age hit a decade boundary
Start results
Incrementing age by one year from 10
Start results
Incrementing age by one year from 11
Start results
Incrementing age by one year from 12
Start results
Incrementing age by one year from 13


"""