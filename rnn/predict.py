import numpy as np
import keras
import re
from scipy import stats
import random

model = keras.models.load_model('model.h5')
word_len = 100

wordnet_data = "" 
with open("./wordnet_words.txt") as wordnet_words_file:
    wordnet_data = wordnet_words_file.read()



wordnet_data = re.sub("[^a-z ]+", "", wordnet_data)
dist = " ".join(set(wordnet_data.split(" ")))

first_letters_dist = {

}


for i in dist:
    if len(i):
        if i[0] not in first_letters_dist:
            first_letters_dist[i[0]] = 0
        first_letters_dist[i[0]] += 1



characters = sorted(set(wordnet_data))
characters_len = len(characters)

character_index_map = {character: characters.index(character) for character in characters}

# # most likely words replace with users error should all start with 1 and use this
prob = { 
    "m":3.0129, "h":3.0034, "g":2.4705, 
    "b":2.0720, "f":1.8121, "y":1.7779,
    "w":1.2899, "k":1.1016, "v":1.0074,
    "x":0.2902, "z":0.2722, "j":0.1965,
    "q":0.1962, "e":11.1607, "a":8.4966,
    "r":7.5809, "i":7.5448, "o":7.1635,
    "t":6.9509, "n":6.6544, "s":5.7351,
    "l":5.4893, "c":4.5388, "u":3.6308,
    "d":3.3844, "p":3.1671, " ": 0.1
}


prob_a = [None for i in range(len(character_index_map))]
first_letter_a = [None for i in range(len(character_index_map))]
for k, v in character_index_map.items():
    prob_a[character_index_map[k]] = prob[k]
    first_letter_a[character_index_map[k]] = first_letters_dist[k]

prob_a = [(i - min(prob_a)) / (max(prob_a) - min(prob_a)) for i in prob_a]
first_letter_a = [(i - min(first_letter_a)) / (max(first_letter_a) - min(first_letter_a)) for i in first_letter_a]

def get_predicted_text(predictions, temperature):
    most_common_predictions = predictions 
    predictions = np.log(np.asarray(most_common_predictions).astype('float64')) / temperature
    exponential_predictions = np.exp(predictions)
    return np.argmax(np.random.multinomial(1, exponential_predictions / np.sum(exponential_predictions), 1))



generated_text = "cu"

# random.choices(list(characters), weights=np.array(first_letter_a) * np.array(prob_a), k=1)[0]

for i in range(99):
    seed_data = np.zeros((1, word_len, characters_len))
    for j in range(len(generated_text)):
        seed_data[0,j,character_index_map[generated_text[j]]] = 1.
    preds = model.predict(seed_data)[0]
    new_character = characters[get_predicted_text(preds, 0.8)]
    generated_text +=new_character
    prob_a[character_index_map[new_character]] /= 2

print(generated_text)
