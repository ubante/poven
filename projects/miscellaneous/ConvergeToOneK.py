__author__ = 'ubante'

# main

startValue = 700.0
current = startValue
decrementValue = float(startValue)/250
rangeEnd = 24*2;
incrementValue = float((1000-startValue)/rangeEnd + decrementValue)
print "Using dec:%4.2f and inc:%4.2f:" % (decrementValue, incrementValue)
for i in range(1, rangeEnd):
    current = current - decrementValue + incrementValue
    print "%2d: %6.1f" % (i, current)