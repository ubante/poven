from Results import Results


class Cat:
    def __init__(self):
        self.age = 10  # years
        self.total_results = Results()

    def age_squarer(self):
        r = Results()

        age2 = self.age * self.age
        r.add("age squared is " + str(age2))

        self.total_results.append(r)
        return r

    def age_ager(self):
        r = Results()

        r.add2("Incrementing age by one year")
        self.age += 1

        if self.age == 10:
            r.add3("Age hit a decade boundary")

        self.total_results.append(r)
        return r

# main

print_level = 1

bugger = Cat()
res = bugger.age_squarer()

for i in range(1, 12):
    res.append(bugger.age_ager())

res.display3()


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
