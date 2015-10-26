sentence = "aabbbccccccdeeeeeeeeeefffgeeeeeeeeeeeee"
sequenceLetter = ""
sequenceCounter = 0;
longestSequenceLetter = "";
longestSequenceCounter = 0;
for letter in sentence:
    if letter == sequenceLetter:
        sequenceCounter += 1
        print "%s is at %d" % (letter, sequenceCounter)
    else:
        if sequenceCounter > longestSequenceCounter:
            longestSequenceCounter = sequenceCounter
            longestSequenceLetter = sequenceLetter
            print "%s is the new champion with length %d" % (sequenceLetter, sequenceCounter)
        sequenceCounter = 1
        sequenceLetter = letter
        print "%s is at %d" % (letter, sequenceCounter)

if sequenceCounter > longestSequenceCounter:
            longestSequenceCounter = sequenceCounter
            longestSequenceLetter = sequenceLetter
            print "%s is the new champion with length %d" % (sequenceLetter, sequenceCounter)
print "The letter %s appears %d times in a row." % (longestSequenceLetter, longestSequenceCounter)
