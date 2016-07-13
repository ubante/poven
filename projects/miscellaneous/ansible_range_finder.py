import re


class Pokemon():
    def __init__(self, h, r):
        self.host_str = h
        self.range_str = r

    def is_contained_in_range(self):
        # find web2.domain.com in web[1:3].domain.com
        # assume range_str contains exactly one range expression

        match_obj = re.match(r'(.*)\[(.*):(.*)\](.*)', self.range_str)
        [prefix, start, stop, suffix] = match_obj.group(1, 2, 3, 4)

        # print "prefix:", prefix
        # print "start_num:", start
        # print "stop_num:", stop
        # print "postfix:", suffix

        for i in range(int(start), int(stop)+1):
            composite_str = "{}{}{}".format(prefix, i, suffix)
            # print "comparing", composite_str
            if composite_str == self.host_str:
                return True
        return False

if __name__ == "__main__":
    host_str = "web17.domain.com"
    range_str = "web[1:99].domain.com"

    p = Pokemon(host_str, range_str)
    result = p.is_contained_in_range()

    if result:
        print "it's in there"
    else:
        print "no monsters"


