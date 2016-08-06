"""
You shouldn't use both a field and a method called is_present.

http://stackoverflow.com/questions/12614334/typeerror-bool-object-is-not-callable
"""


class Soda():

    # The leading underscore is sufficient to distinguish it from the method name.
    def __init__(self):
        self._is_present = True

    def is_present(self):
        return self._is_present


print "Yo"
s = Soda()

if s._is_present:
    print "Soda is present"
else:
    print "Soda is not present"

if s.is_present():
    print "Soda is present via method"
else:
    print "Soda is not present via method"

if s._is_present:
    print "2 Soda is present"
else:
    print "2 Soda is not present"

if s.is_present():
    print "2 Soda is present via method"
else:
    print "2 Soda is not present via method"


