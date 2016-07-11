from netaddr import IPAddress, AddrFormatError



goodip = IPAddress('1.2.3.4')

try:
    badip = IPAddress('asdf.asdf.com')
except AddrFormatError:
    print "This is a bad IP"


print "carry on"


