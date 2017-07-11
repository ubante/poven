#!/usr/bin/env python


class BasePhone(object):

    def __init__(self):
        self.name = "haha"

    def parse(self):
        raise NotImplementedError()


class SomePhone(BasePhone):
    someStuff = 11


def main():
    print("start")
    s = SomePhone()
    print(s.name)
    s.parse()


if __name__ == "__main__":
    main()

