import re


def contains2(network_mask_string, query_ip):
    m = re.search("(.*)/(.*)", network_mask_string)
    network_string = m.group(1)
    network_binary = ''.join([bin(int(x) + 256)[3:] for x in network_string.split('.')])
    network_decimal = int(network_binary, 2)
    print "network_decimal:", network_decimal

    mask_cidr = m.group(2)
    print "Mask is:", mask_cidr
    mask_decimal = 0
    for i in range(0, int(mask_cidr)):
        mask_decimal += pow(2, 31-i)
    print "This is mask_decimal:", mask_decimal
    start_decimal = network_decimal & mask_decimal
    print "This is start_decimal:", start_decimal

    print "binary: {}, decimal: {}".format(network_binary, network_decimal)
    print "Looking between {} and xxxx".format(network_string)
    return True


def contains(network_mask_string, ip_string):
    search = re.search("(.*)/(.*)", network_mask_string)
    network_string = search.group(1)
    network_binary_string = ''.join([bin(int(x) + 256)[3:] for x in network_string.split('.')])
    network_binary = bin(int(network_binary_string, base=2))
    network_decimal = int(network_binary, 2)
    print "network_binary: {} ({}) {}".format(network_binary, network_decimal, network_string)

    mask_cidr = search.group(2)
    mask_decimal = 0
    for i in range(0, int(mask_cidr)):
        mask_decimal += pow(2, 31 - i)
    mask_binary = bin(mask_decimal)
    print "mask_binary   : {} ({}) {}".format(mask_binary, mask_decimal, mask_cidr)

    un_mask_decimal = 0
    for i in range(int(mask_cidr), 32):
        un_mask_decimal += pow(2, 31 - i)
    un_mask_binary = bin(un_mask_decimal)
    print "un_mask_binary: {} ({})".format(un_mask_binary, un_mask_decimal)

    start_decimal = network_decimal & mask_decimal
    start_binary = bin(start_decimal)
    print "start_binary  : {} ({})".format(start_binary, start_decimal)

    stop_decimal = network_decimal | un_mask_decimal
    stop_binary = bin(stop_decimal)
    print "stop_binary   : {} ({})".format(stop_binary, stop_decimal)

    ip_binary_string = ''.join([bin(int(x) + 256)[3:] for x in ip_string.split('.')])
    ip_binary = bin(int(ip_binary_string, base=2))
    ip_decimal = int(ip_binary, 2)
    print "ip_binary     : {} ({}) {}".format(ip_binary, ip_decimal, ip_string)

    if (start_decimal < ip_decimal) and (ip_decimal < stop_decimal):
        return True
    else:
        return False

lines = ["stuff 1.2.3.4/8 and 200.3.2.0/28 post",
         "more stuff 10.128.0.0/9 and 200.3.2.0/30 more post"]

# print lines

ip = "10.200.3.4"
network_regex = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}")
for line in lines:
    print "\n--", line
    for m in re.finditer(network_regex, line):
        found_network_string = line[m.start():m.end()]
        print "\nfound:", found_network_string, m.start(), m.end()

        if contains(found_network_string, ip):
            print "FOUND:", line


