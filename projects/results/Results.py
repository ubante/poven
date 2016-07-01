class Results:
    """
    There are three different result levels.

    (1) this is what you normally expect
    (2) debug
    (3) this gets printed when it gets recorded

    Use (3) for things you want to see in realtime.

    """
    def __init__(self):
        self.lines = []
        self.lines.append((2, "Start results"))

    def _add(self, message, log_level=1):
        self.lines.append((log_level, message))
        # print "adding::", log_level, message

    def add(self, some_string):
        self._add(some_string, log_level=1)

    def add1(self, some_string):
        self._add(some_string, log_level=1)

    def add2(self, some_string):
        self._add(some_string, log_level=2)

    def add3(self, some_string):
        self._add(some_string, log_level=3)
        print some_string

    def _display(self, log_level=1):
        for tuple in self.lines:
            # print tuple
            if tuple[0] <= log_level:
                print tuple[1]

    def display(self):
        self._display(1)

    def display1(self):
        self._display(1)

    def display2(self):
        self._display(2)

    def display3(self):
        self._display(3)

    def extend(self, some_results):
        self.lines.extend(some_results.lines)

    def get_size(self):
        return len(self.lines)

    def dump(self):
        print "\nHere's the results dump:"
        for line in self.lines:
            print line
