colors = "abcdebe"
hash = {}
for letter in colors:
    print letter
    if letter in hash.keys():
        hash[letter] += 10
    else:
        hash[letter] = 2

print hash


















