

class Banana:
    """
    Bananas
    """
    def __init__(self):
        self.name = "chiquita"
        self.color = "green"
        self.initialize()

    def initialize(self):
        self.color = "yellow"



# main

fruit = Banana()
print fruit.name
print fruit.color

