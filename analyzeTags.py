
tagCollection = []

tagCollectionFile = open("tagCollection-3.txt", 'r')
for line in tagCollectionFile:
    line = line[:-1].split(':')
    tagCollection.append((int(line[1]), line[0]))

tagCollection.sort()
for tag in tagCollection:
    print (tag)