sentence = "aabbbccccccdddddddddddddddddddddddddeeeeeeeeeeeeeeefffgeeeeeeeeeeeee"
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

# approach2 that doesn't work :P
print "\n\n\n"
import operator
dict = {}
prev_char = sentence[0]
dict[sentence[0]] = 1
for char in sentence[1:]:
 if char in dict and char == prev_char:
  dict[char] = int(dict[char]) + 1
 elif char != prev_char:
  dict[char] = 1
 prev_char = char
print "champ is %s with length %d" %(max(dict.iteritems(), key=operator.itemgetter(1))[0],dict[max(dict.iteritems(), key=operator.itemgetter(1))[0]])
print dict

# approach3
print "\n\n\n"
import itertools
# sentence = "aabbbccccccddddddddddddddddddddeeeeeeeeeeeeeeefffgeeeeeeeeeeeeeeeee"
print max(len(list(y)) for (c,y) in itertools.groupby(sentence))

print "---------"
for (c,y) in itertools.groupby(sentence):
    print c, len(list(y))

print max((len(list(y)), c) for (c,y) in itertools.groupby(sentence))






