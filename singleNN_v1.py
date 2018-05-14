



#step 1: load tags and words
tagID = {}
wordID = {}
wordList = []
tagFile = open("tagCollection-3_single.txt", 'r')
wordFile = open("wordCollection-3.txt", 'r')
N_tag, N_word = 0, 0

for line in tagFile:
    if line[0] == '\n':
        break
    tagID[line[:-1].split(':')[0]] = N_tag
    N_tag += 1
for line in wordFile:
    if line[0] == '\n':
        break
    wordID[line[:-1].split(':')[0]] = N_word
    wordList.append(line[:-1].split(':')[0])
    N_word += 1

#step 2: prepare training and testing data
removableSymbols = "\"\',?().+&#[]=><%@/\\:^-0123456789{}|*`δβ"
stopWords = []
stopWordsFile = open("stopwords.txt", 'r')
for line in stopWordsFile:
    stopWords.append(line[:-1])
X, Y = [], []
articleFile = open("data_crawl_article-3.txt", 'r')
skillFile = open("data_crawl_skill-3.txt", 'r')

singleLine = {}
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

for id, line in enumerate(skillFile):
    if ';' in line or line[0] == '\n':
        continue

    singleLine[id] = True
    single_y = [0.0 for _ in range(N_tag)]
    line = removedParentheses(line).replace(';', ',').replace(", and", ',')
    tag = line[:-1].split(',')[0].strip()
    single_y[tagID[tag]] = 1.0
    Y.append(single_y)


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

# print (wordList)
for id, line in enumerate(articleFile):
    if id not in singleLine:
        continue

    line = removedLatex(line.lower())
    # filter the line
    for ch in removableSymbols:
        line = line.replace(ch, ' ')

    single_x = [0.0 for _ in range(N_word)]
    for word in wordList:
        if word in line:
            single_x[wordID[word]] = 1.0
    X.append(single_x)



import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# define baseline model
def baseline_model():
# create model
    model = Sequential()
    model.add(Dense(8, input_dim=1532, activation='relu'))
    model.add(Dense(49, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=baseline_model, epochs=20, batch_size=5, verbose=0)
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(estimator, np.array(X), np.array(Y), cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
