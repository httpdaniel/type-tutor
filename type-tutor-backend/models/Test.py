old_correct_characters = {
        "a": 1, 
        "b": 1, 
        "c": 1, 
        "d": 1, 
        "e": 1, 
        "f": 1, 
        "g": 1,
        "h": 1,
        "i": 1,
        "j": 1,
        "k": 1,
        "l": 1,
        "m": 1,
        "n": 1,
        "o": 1,
        "p": 1,
        "q": 1,
        "r": 1,
        "s": 1,
        "t": 1,
        "u": 1,
        "v": 1,
        "w": 1,
        "x": 1,
        "y": 1,
        "z": 1
    }
old_incorrect_characters = {
    "a": 5, 
    "b": 3, 
    "c": 1, 
    "d": 5, 
    "e": 7, 
    "f": 1, 
    "g": 1,
    "h": 1,
    "i": 1,
    "j": 1,
    "k": 1,
    "l": 1,
    "m": 1,
    "n": 1,
    "o": 1,
    "p": 1,
    "q": 1,
    "r": 1,
    "s": 1,
    "t": 1,
    "u": 1,
    "v": 1,
    "w": 1,
    "x": 1,
    "y": 1,
    "z": 1
}

def calculate_json_avg(json_values_true, json_values_false):
    incorrect_json = {}
    correct_json = {}
    for k,v in zip(json_values_true.items(), json_values_false.items()):
        average_correct = k[1] / (k[1] + v[1])
        average_incorrect = v[1] / (k[1] + v[1])
        incorrect_json[k[0]] = average_incorrect
        correct_json[k[0]] = average_correct
    return (correct_json, incorrect_json)

print(calculate_json_avg(old_correct_characters, old_incorrect_characters))