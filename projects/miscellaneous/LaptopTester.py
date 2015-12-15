import re

cookbook = "prefix-shortc-thing"
print "Cookbook is", cookbook
shorts = ["shorta", "shortb", "shortc"]

expectedPrefix = "prefix-short-"
expectedPrefixes = []
for short in shorts:
    expectedPrefixes.append("prefix-%s-" % short)

cookbookBeginning = re.search('(prefix-.*-)', cookbook).groups()[0]
# cookbookBeginningList = re.search('(prefix-.*-)', cookbook)
# cookbookBeginning = cookbookBeginningList.groups()[0]
print "% starts with %s" % (cookbook, cookbookBeginning)

print "\nThis is the simple approach:"
if cookbook.startswith(expectedPrefix):
    print "good"
else:
    print "bad"

print "\nAnd the better approach:"
if cookbookBeginning in expectedPrefixes:
    print "good"
else:
    print "bad"

print "this is %ssss" % "X"







