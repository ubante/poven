import random
"""
Trump asked:

Given a 12/12 C'Thun, opponent only has a 6/6 mob, what are the odds of killing the mob?
"""


def does_hit():
    if random.randint(0, 1):
        return True
    else:
        return False


def does_mob_live():
    mob_health = 6

    for i in range(1, 12 + 1):
        if mob_health > 0:
            if does_hit():
                mob_health -= 1
        print "Turn {}: health = {}".format(i, mob_health)
        print mob_health,

    if mob_health > 0:
        print "It lives."
        return True
    else:
        print "It dies."
        return False


if __name__ == "__main__":
    iteration_max = 1000
    win_count = 0
    for i in range(0, iteration_max):
        if does_mob_live():
            win_count += 1

    print "\n{}/{} mob lives".format(win_count, iteration_max)


"""
376/1000 mob lives
3846/10000 mob lives
38785/100000 mob lives
"""