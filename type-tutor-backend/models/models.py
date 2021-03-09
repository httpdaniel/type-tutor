from flask import Flask, request
app = Flask(__name__)

count_letters  = {'p':20,'a':27}

prop_wrong_chars = {'a': 12/count_letters['a'], 'p':12/count_letters['p']}


# create a fun => set threshold for the wrong words
wrong_words = {}

# Sessios based according to User -> Extrack dat based on Session ? After a few sessions may not be valid => if a user is not getting a word wrong anymore
# For Any sessions -> proportion of wrong letters , wrong characters, proportion of words wrong session based -> For last 5 sections take data out -> current user based on that ( Check point)
# Get rid of irrelevant user data after checkpoint. 

# Minisessions based set of words => Adapt based on that. 
# Login based Session Adaptation
#  Cumulative Adaptation based on number of minisessions 
# Time taken to complete mini session => Variable 

# generate first letter 
# most likely letter, incorrect word usages, times
# Sequences -> Next letter, most incorrect used to generate letter, Time, Speed, lpm
def test():
    print(prop_wrong_chars)


def proportion_of_wrongWords():
    pass


if __name__ == "__main__":
    test()