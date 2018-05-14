import numpy as np



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

X = np.array(X)
Y = np.array(Y)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Part 2 - Now let's make the ANN!

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(2048, kernel_initializer = 'uniform', activation = 'relu', input_dim = 1532))

# Adding the second hidden layer
classifier.add(Dense(1024, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(512, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(256, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(128, kernel_initializer = 'uniform', activation = 'relu'))
# Adding the output layer
classifier.add(Dense(49, kernel_initializer = 'uniform', activation = 'softmax'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 25, epochs = 100)

# Part 3 - Making the predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print (cm)
