from somethinglib import Bird


class Thing:
    some_bird = Bird("birdname")

    def __init__(self):
        # Thing.some_bird = "blahblah"
        pass

    # @classmethod
    def print_some_string(self):
        # print some_string
        print Thing.some_bird
        # Thing.some_bird = "something else"
        Thing.some_bird = Bird("newbird")
        print Thing.some_bird


def main():
    t = Thing()
    t.print_some_string()


if __name__ == "__main__":
    main()