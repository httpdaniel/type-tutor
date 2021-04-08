import re

raw_text_file = open('train_rnn/84-0.txt', "r")
raw_text = raw_text_file.read()
raw_text = raw_text.split("Letter 1")[-1]
raw_text = raw_text.split("*** END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN ***")[0]
raw_text = re.sub("[^a-z ]+", " ", raw_text.lower())
raw_text = re.sub(' +', ' ', raw_text)

cleaned_text_file = open('train_rnn/frankinstein.txt', 'w')

cleaned_text_file.write(raw_text)    

cleaned_text_file.close()
raw_text_file.close()