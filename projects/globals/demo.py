myGlobal = 5


def func1():
    myGlobal = 42


def func2():
    print myGlobal


def func3():
    global myGlobal
    myGlobal = 24


def func4():
    print myGlobal


def main():
    func1()
    func2()
    func3()
    func4()

if __name__ == "__main__":
    main()