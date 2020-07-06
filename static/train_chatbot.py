import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

import matplotlib.pyplot as plt

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('intents.json').read()
intents = json.loads(data_file)

#json tip dict
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # take each word and tokenize it -> am toate cuvintele intr-o lista
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # adding documents -> de forma asta [(['Hi', 'there'], 'greeting'), (['How', 'are', 'you'], 'greeting')] și tot adaug
        documents.append((w, intent['tag']))
        # adding classes to our class list -> clasele vor contine doar intent-urile
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#aduc cuvintele la forma de baza, le ordonez crescator si inlatur duplicatele
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
# la fel fac si pentru clase
classes = sorted(list(set(classes)))

print (len(documents), "documents")
#
print (len(classes), "classes", classes)
#
print (len(words), "unique lemmatized words", words)


pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

# initializing training data
training = []
output_empty = [0] * len(classes)
for doc in documents:
    # initializing bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0] # cuvintele din interiorul unui pattern: hi there
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    # practic pun 1 daca gasesc cuvant din pattern curent in lista totala de cuvinte
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
# shuffle our features and turn into np.array
# 109 de documente (tag + pattern)
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
# acestia se numesc hiperparametri. Tot ce poate fi schimbat, functia de activare, loss function, optimizatorul,
# se pot schimba ca sa fie un alt fel de output
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
#adaug un dropout pentru a raspunde bine la datele de evaluare/test ca sa evit overfittingul
#adaug o "interpretare" noua asupra retelei atunci cand fac dropout. Practic fac drop la un nod si la conexiunile sale
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
#adaug dropout si la celalalt strat
#bias e pt a activa neuroni diferiti, ajustez greutatile conform bias-ului pt a avea diferite rezultate
model.add(Dropout(0.5))
# ultimul strat are lungimea tuturor intentiilor antrenate /labels. ca sa poata clasifica
# softmax se asigura ca toate valorile sunt cuprinse intre 0 si 1 si adaugate dau maxim 1. Sigmoid nu face la fel?
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model
epochs = 200
history = model.fit(np.array(train_x), np.array(train_y), epochs=epochs, batch_size=5, verbose=1)
model.save('chatbot_model.h5', history)


loss_train = history.history['accuracy']
loss_val = history.history['loss']
epochs = range(1,epochs+1)
plt.plot(epochs, loss_train, 'g', label='Training accuracy')
plt.plot(epochs, loss_val, 'b', label='validation accuracy')
plt.title('Training and Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
print("model created")
