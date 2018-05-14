"""
Collect all the tags
Rule:
1. separated by ',' ';' ", and"
2. remove which inside ()
"""

tagFile = open("data_crawl_skill-3.txt", 'r')
tagCollection = []
tagWeight = {}

def removedParentheses(line):
    ans = ""
    outside = True
    for ch in line:
        if ch == '(':
            outside = False
        elif ch == ')':
            outside = True
        elif outside:
            ans += ch
    return ans


for line in tagFile:
    line = removedParentheses(line).replace(';', ',').replace(", and", ',')
    tags = line[:-1].split(',')

    for i in range(len(tags)):
        tag = tags[i].strip()
        if tag not in tagWeight:
            tagCollection.append(tag)
            tagWeight[tag] = 1
        else:
            tagWeight[tag] += 1



tagCollection.sort()

#save the tag collection
tagCollectionFile = open("tagCollection-3.txt", 'w')
for tag in tagCollection:
    tagCollectionFile.write(tag + ':' + str(tagWeight[tag]) + '\n')
tagCollectionFile.close()