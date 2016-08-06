import json
import logging
from collections import defaultdict


class NestedDictionary(dict):
    """
    I want to make foo["a"]["b"] without creating foo["a"] first.

    See http://stackoverflow.com/questions/635483/what-is-the-best-way-to-implement-nested-dictionaries-in-python
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class GuiCounter:
    """
    The counter structure in JSON:
{
  "counter": 84,
  "/stats": 11,
  "/": {
    "counter": 21,
    "api": {
      "counter": 20,
      "v1": {
        "dns": {
          "host1": 1,
          "host2": 2
        },
        "inventory": {
          "host1": 5,
          "host3": 12
        }
      }
    }
  },
  "/search": 1,
  "/q": {
    "host1": 2,
    "host4": 11
  }
}

As a dictionary:
d={'counter': 84, 'stats': 11, '/': {'counter': 21, 'api': {'counter': 20, 'v1': {'dns': {
'host1': 1, 'host2': 2}, 'inventory': {'host1': 5, 'host3': 12}}}}, '/search': 1, '/q': {
'host1': 2, 'host4': 11}}

    Note that we cannot use "counter" as a "word" in the URL.

    Using defaultdict since it makes intermediate keys.
    See http://stackoverflow.com/questions/3122566/in-a-python-dict-of-dicts-how-do-you-emulate-perls-auto-vivification-behavior
    """
    def __init__(self):
        logging.debug("Initializing GuiCounter")
        self.hit_counter = 0
        # self.counter_dict = {"counter": 0, "/": {}}
        # self.counter_dict = NestedDictionary()
        # self.counter_dict["counter"] = 0
        # self.counter_dict["/"]["q"] = {}
        # self.counter_dict["/"]["search"] = 0
        # self.counter_dict["/"]["stats"] = 0
        # self.counter_dict["/"]["api"]["v1"]["all"] = {}
        # self.counter_dict["/"]["api"]["v1"]["dns"] = {}

        tree = lambda: defaultdict(tree)
        self.counter_dict = tree()
        self.counter_dict["counter"] = 0

    def _tally_path(self, path):
        pass

    def initialize_key(self, dictionary):
        pass

    def increment_counter(self, path=None):
        # Assume that the presence of value2 assumes the presence of value1,
        # and the presence of value1 assumes the presence of endpoint
        # if value2:

        print "\nTrying: " + path
        self.hit_counter += 1
        logging.debug("incrementing counter for {} to {}".format(path, self.hit_counter))

        # # if self.counter_dict["counter"]:
        # if self.counter_dict.has_key("counter"):
        #     self.counter_dict["counter"] += 1
        # else:
        #     print "initializing counter key"
        #     self.counter_dict["counter"] = 1

        words = path.split('/')
        # I'm beyond being proud
        if 2 == len(words):
            print "2: ", words
            try:
                self.counter_dict["/"][words[1]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]] = 1
        if 3 == len(words):
            print "3: ", words
            try:
                self.counter_dict["/"][words[1]][words[2]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]][words[2]] = 1
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
        if 6 == len(words):
            print "6: ", words
            try:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]][words[5]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]][words[5]] = 1
        if 7 == len(words):
            print "7: ", words
            try:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]][words[5]][words[
                    6]] += 1
            except TypeError:
                self.counter_dict["/"][words[1]][words[2]][words[3]][words[4]][words[5]][words[
                    6]] = 1




    def get_hit_counter(self):
        logging.debug("returning a count of: {}".format(self.hit_counter))
        return self.hit_counter

    def get_dict(self):
        return self.counter_dict

# main
ctr = GuiCounter()
ctr.increment_counter("/stats")
ctr.increment_counter("/search")
ctr.increment_counter("/api")
ctr.increment_counter("/q/host0")
ctr.increment_counter("/q/host0")
ctr.increment_counter("/a/b/host1")
ctr.increment_counter("/a/b/host2")
ctr.increment_counter("/a/b/c/host3")


print "\n\nTotal count:", ctr.get_hit_counter()
print "RAW:"
print ctr.get_dict()
print "\nJSON:"
print json.dumps(ctr.get_dict())

"""
@app.route("/")
@app.route("/q/<fqdn_weird_encoding>")
@app.route("/stats")
@app.route("/api/v1/all/<fqdn_weird_encoding>")
@app.route("/search")
@app.route("/api/v1/<system>/<fqdn_weird_encoding>")
"""