import unittest

"""
Let's PyUnit.

http://www.drdobbs.com/testing/unit-testing-with-python/240165163
"""

class SomeTest(unittest.TestCase):

    def setUp(self):
        print "SomeTest:setUp_:begin"

        print "do something for set up"

        print "SomeTest:setUp_:end"

    def tearDown(self):
        print "SomeTest:teardown_:begin"

        print "do something for tear down"

        print "SomeTest:teardown_:end"

    def testA(self):
        print "in SomeTest:testA"

    def testB(self):
        print "in SomeTest:testB"





if __name__ == '__main__':
    unittest.main()
