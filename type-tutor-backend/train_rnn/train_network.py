import keras
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import RMSprop
import re

wordnet_data = "" 

wordnet_data = "" 
with open("train_rnn/frankinstein.txt") as wordnet_words_file:
    wordnet_data = wordnet_words_file.read()


wordnet_data = re.sub("[^a-z ]+", "", wordnet_data)

word_len = 50
wordnet_data_len = len(wordnet_data)

word_samples = []
next_characters = []

for i in range(0, wordnet_data_len - word_len, 3):
    next_character_index = i + word_len
    word_samples.append(wordnet_data[i: next_character_index])
    next_characters.append(wordnet_data[next_character_index])

characters = sorted(set(wordnet_data))
characters_len = len(characters)
word_samples_len = len(word_samples)

character_index_map = {character: characters.index(character) for character in characters}

x = np.zeros((word_samples_len, word_len, characters_len), dtype=np.bool)
y = np.zeros((word_samples_len, characters_len), dtype=np.bool)

for i in range(word_samples_len):
    for j in range(len(word_samples[i])):
        x[i,j, character_index_map[word_samples[i][j]]] = 1
    y[i, character_index_map[next_characters[i]]] = 1


model = Sequential()
model.add(LSTM(64, input_shape=(word_len, characters_len)))
# model.add(LSTM(64, activation="relu"))
model.add(Dense(characters_len, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))


model.fit(x, y, batch_size=128, epochs=30)
model.save("rnn_model/model.h5")
