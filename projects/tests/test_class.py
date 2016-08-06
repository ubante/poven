import unittest

"""
https://docs.python.org/2/library/unittest.html
"""


class Widget():
    def __init__(self, s):
        self.name = s
        self.x = 50
        self.y = 50

    def dispose(self):
        pass

    def size(self):
        return self.x, self.y

    def resize(self, x, y):
        self.x = x
        self.y = y


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
        self.widget = None

    def test_default_size(self):
        self.assertEqual(self.widget.size(), (50, 50),
                         'incorrect default size')

    def test_resize(self):
        self.widget.resize(100, 150)
        self.assertEqual(self.widget.size(), (100, 150),
                         'wrong size after resize')
