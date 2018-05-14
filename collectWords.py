

removableSymbols = "\"\',?().+&#[]=><%@/\\:^-0123456789{}|*`δβ"
wordCollection = []
wordWeight = {}
stopWords = []
stopWordsFile = open("stopwords.txt", 'r')
for line in stopWordsFile:
    stopWords.append(line[:-1])


def getPrefix(s1, s2):
    n1, n2 = len(s1), len(s2)
    mx, mn = max(n1, n2), min(n1, n2)

    threshold = min(int(0.5 * mx), mn - 1)
    if s1[:threshold] == s2[:threshold]:
        if n1 <= n2:
            return s1
        else:
            return s2
    else:
        return "not_same"

def removedLatex(line):
    ans = ""
    outside = True
    for ch in line:
        if ch == '$' and outside:
            outside = False
        elif ch == '$' and not outside:
            outside = True
        elif outside:
            ans += ch
    return ans


articleFile = open("data_crawl_article-3.txt", 'r')
cntLine = 0
for line in articleFile:
    line = removedLatex(line.lower())
    # print (line[:-1])

    #filter the line
    for ch in removableSymbols:
        line = line.replace(ch, ' ')

    words = line[:-1].split(' ')
    for word in words:
        if len(word) <= 2 or word in stopWords:
            continue
        if word not in wordWeight:
            wordCollection.append(word)
            wordWeight[word] = 1
        else:
            wordWeight[word] += 1

    # cntLine += 1
    # if cntLine == 100:
    #     break

wordCollection.append("zzz")
wordWeight["zzz"] = 0

wordCollection.sort()
tmpWord = wordCollection[0]
goodWords = []
for word in wordCollection[1:]:
    prefixWord = getPrefix(tmpWord, word)
    print (tmpWord, word, prefixWord)
    if prefixWord == "not_same":
        goodWords.append(tmpWord)
        tmpWord = word
    else:
        print (word, wordWeight[word])
        print (tmpWord, wordWeight[tmpWord])
        wordWeight[prefixWord] = wordWeight[tmpWord] + wordWeight[word]
        tmpWord = prefixWord
# for word in wordCollection:
#     print (wordWeight[word], word)

wordCollectionFile = open("wordCollection-3.txt", 'w')
for word in goodWords:
    wordCollectionFile.write(word + ':' + str(wordWeight[word]) + '\n')
wordCollectionFile.close()