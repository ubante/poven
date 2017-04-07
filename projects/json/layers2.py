from pprint import pprint

d = {'a': 1, 'b': 2, 'c': 3}
dd = {'A': d, 'B': d, 'C': d}
ddd = {'X': dd, 'Y': dd, 'Z': dd}
dddd = {'J': ddd, 'K': ddd, 'L': ddd}

print("-" * 40)
pprint(dddd)

print("-" * 40)
pprint(dddd['J'])
pprint(dddd['J']['Y'])

dddd['M'] = {}
dddd['M']['MM'] = "some other thing"
dddd['J']['Y']['host1'] = "something something"

print("-" * 40)
pprint(dddd)

h = {'J': {'X': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3}},
           'Y': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3},
                 'asdf': 'asdfasdasdf'},
           'Z': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3},
                 'host1': 'ig-deploy'}},
     'K': {'X': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3}},
           'Y': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': 'install some package',
                 'C': {'a': 1, 'b': 2, 'c': 3}},
           'Z': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3}}},
     'L': {'X': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3}},
           'Y': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3}},
           'Z': {'A': {'a': 1, 'b': 2, 'c': 3},
                 'B': {'a': 1, 'b': 2, 'c': 3},
                 'C': {'a': 1, 'b': 2, 'c': 3},
                 'asdf': 'afdawefasdfawefw'}}}

J = {'X': {'A': {'a': 1, 'b': 2, 'c': 3},
           'B': {'a': 1, 'b': 2, 'c': 3},
           'C': {'a': 1, 'b': 2, 'c': 3}},
     'Y': {'A': {'a': 1, 'b': 2, 'c': 3},
           'B': {'a': 1, 'b': 2, 'c': 3},
           'C': {'a': 1, 'b': 2, 'c': 3},
           'asdf': 'asdfasdasdf'},
     'Z': {'A': {'a': 1, 'b': 2, 'c': 3},
           'B': {'a': 1, 'b': 2, 'c': 3},
           'C': {'a': 1, 'b': 2, 'c': 3},
           'host1': 'ig-deploy'}}

Y = {'A': {'a': 1, 'b': 2, 'c': 3},
     'B': {'a': 1, 'b': 2, 'c': 3},
     'C': {'a': 1, 'b': 2, 'c': 3},
     'asdf': 'asdfasdasdf'}

print("-" * 40)
pprint(h)

layers = [h, J, Y]
