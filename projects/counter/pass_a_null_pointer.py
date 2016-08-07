import json
from collections import defaultdict


class Thing:
    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.counter_dict = tree()

    def _increment1(self, words):
        try:
            self.counter_dict["/"][words[1]][words[2]] += 1
        except TypeError:
            self.counter_dict["/"][words[1]][words[2]] = 1

    def increment1(self, words):
        if 2 == len(words):
            print "2: ", words
            try:
                self.counter_dict["/"][words[1]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]] = 1
        if 3 == len(words):
            print "3: ", words
            self._increment1(words)

            # try:
            #     self.counter_dict["/"][words[1]][words[2]] += 1
            # except TypeError:
            #     self.counter_dict["/"][words[1]][words[2]] = 1
        if 4 == len(words):
            print "4: ", words
            try:
                self.counter_dict["/"][words[1]][words[2]][words[3]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]][words[2]][words[3]] = 1
        if 5 == len(words):
            print "5: ", words
            try:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]] = 1

    def increment(self, words):
        pass

    def to_string(self):
        return json.dumps(self.counter_dict)

    def run(self):
        print "\nEmpty:"
        print self.to_string()

        self.increment1(["a", "b", "host1"])
        print "\nhost1:"
        print self.to_string()



t = Thing()
t.run()

"""

host1:
{"/": {"b": {"host1": 1}}}

"""