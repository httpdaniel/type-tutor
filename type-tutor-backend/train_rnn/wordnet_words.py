from nltk.corpus import wordnet as wn

wordnet_words_file = open('wordnet_words.txt', 'a')
words  = set(i for i in wn.words() if len(i) > 4)

dist = {}

first_word = True
for word in wn.words():
    if len(word) not in dist:
        dist[len(word)] = 0
    dist[len(word)] += 1
    if len(word) > 4:
        if not first_word:
            wordnet_words_file.write(" ")    
        wordnet_words_file.write(word)
        first_word = False

wordnet_words_file.close()
print(dist)