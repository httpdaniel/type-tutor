import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import json
import mysql.connector
from mysql.connector import Error
import numpy as np
import keras
import re
from scipy import stats
import random
import math
import statistics
import tensorflow as tf

keras.backend.set_learning_phase(0)
model = keras.models.load_model('./rnn_model/model.h5')


def get_predicted_text(predictions, temperature, incorrect_characters, character_times, character_index_map, new_character):
    if new_character == " ":
        predictions[character_index_map[" "]] = 0
    most_common_predictions = predictions

    if any((incorrect_characters[v] != 0 and v != 0) for v in range(len(incorrect_characters))):
        most_common_predictions = most_common_predictions * np.array(incorrect_characters) 

    if any((character_times[v] != 0 and v != 0) for v in range(len(character_times))):
        most_common_predictions = most_common_predictions * np.array(character_times) 

    predictions = np.log(np.asarray(most_common_predictions).astype('float64')) / temperature
    exponential_predictions = np.exp(predictions)
    return np.argmax(np.random.multinomial(1, exponential_predictions / np.sum(exponential_predictions), 1))

def characters_mastered(incorrect_characters, correct_characters, wpm, inverse_character_index_map):
    characters = {}
    print(incorrect_characters)
    print(correct_characters)
    for i in range(len(incorrect_characters)):
        if (incorrect_characters[i] > 0.1 and correct_characters[i] < 0.9) or correct_characters[i] == 0:
            characters[inverse_character_index_map[i]] = 0
        else:
            characters[inverse_character_index_map[i]] = 1
    
    return characters

def is_master(incorrect_characters, wpm):
    incorrect_characters[0] = 1
    errors = np.array([i for i in incorrect_characters])
    mastered_errors = statistics.mean(errors) > 0.9 and ((errors >= 0.9).sum() == errors.size).astype(np.int)
    return mastered_errors and wpm >= 40

def min_max_normalisation(prob, character_index_map):
    prob_a = [None for i in range(len(character_index_map))]
    inverse_index_map = {}
    for k, v in character_index_map.items():
        prob_a[character_index_map[k]] = float(prob[k])
        inverse_index_map[character_index_map[k]] = k

    check_unlock_next = True

    for i in range(len(prob_a)):
        prob_a[i] = (prob_a[i] - float(min(prob_a))) / (max(prob_a) - min(prob_a))
    
    return prob_a

def generate_text(user_id, seed_sequence = None):
    word_len = 50
    wordnet_data = "" 

    with open("./train_rnn/frankinstein.txt") as wordnet_words_file:
            wordnet_data = wordnet_words_file.read()

<<<<<<< HEAD
    wordnet_data = re.sub("[^a-z ]+", "", wordnet_data)
    wordnet_data = " ".join(set(wordnet_data.split(" ")))
    
    characters = sorted(set(wordnet_data))
    characters_len = len(characters)
=======
        with open("./train_rnn/frankinstein.txt") as wordnet_words_file:
                wordnet_data = wordnet_words_file.read()
>>>>>>> main

    character_index_map = {character: characters.index(character) for character in characters}
    inverse_character_index_map = {characters.index(character): character for character in characters}
    
    database_connection = None
    database_cursor = None
    error = None
    incorrect_characters = {}
    correct_characters = {}
    character_times = {}
    try: 
        database_connection = mysql.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            database='heroku_8af8fae4116d831',
            user='b1282a2123d519',
            password='29416dad'
        )
        if database_connection.is_connected():
            database_cursor = database_connection.cursor(dictionary=True)
            database_cursor.execute("select words_per_min, incorrect_characters, correct_characters, character_time, character_name from og_user_characters inner join characters on characters.character_id = og_user_characters.character_id inner join users on og_user_characters.user_id = users.user_id where users.user_id = %s;", (user_id,))
            character_data = database_cursor.fetchall()
            for i in character_data:
                try:
                    correct_characters[i["character_name"]] = i["correct_characters"]
                    incorrect_characters[i["character_name"]] = float(i["incorrect_characters"]) / float((i["incorrect_characters"] + i["correct_characters"]))
                    character_times[i["character_name"]] = float(i["character_time"])
                except:
                    incorrect_characters[i["character_name"]] = 0
                    character_times[i["character_name"]] = 0

            wpm = character_data[0]["words_per_min"]
    except Exception as e:
        print(e)
        return "", False, {}
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()

    incorrect_characters[" "] = 1
    character_times[" "] = 1

    incorrect_characters_org = dict(incorrect_characters)
    incorrect_characters_org = min_max_normalisation(incorrect_characters_org, character_index_map)

    new_user = False
    
    for k, v in correct_characters.items():
        if v == 0 and (k == "e" or k == "a" or k == "r" or k == "i" or k == "o" or k == "t"):
            new_user = True
            incorrect_characters[k] = 1
            character_times[k] = 1

    correct_characters[" "] = 1
    
    unlocked_characters = ['e', 'a', 'r', 'i', 'o', 't' ]
    if not new_user:
        unlock_next_character = True
        found_zero_character = False
        next_character_index = 0
        unlock_seq = ['e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'l', 'c', 'u', 'd', 'p', 'm', 'h', 'g', 'b', 'f', 'y', 'w', 'k', 'v', 'x', 'z', 'j', 'q']
        for i in unlock_seq:
            if found_zero_character and incorrect_characters[i] != 0:
                unlock_next_character = False
                break
            if incorrect_characters[i] == 0 and correct_characters[i] == 0:
                found_zero_character = True
            elif incorrect_characters[i] > 0.1:
                unlock_next_character = False
                break
            else:
                next_character_index += 1
                if next_character_index < len(unlock_seq):
                    unlocked_characters.append(unlock_seq[next_character_index])
            
        if unlock_next_character  and wpm >= 40:
            if next_character_index < len(unlock_seq):
                unlocked_characters.append(unlock_seq[next_character_index])
                mean_character_weights = []
                for i in range(next_character_index-1):
                    if incorrect_characters[unlock_seq[i]] != 0:
                        mean_character_weights.append(incorrect_characters[i])
                if len(mean_character_weights):
                    incorrect_characters[unlock_seq[next_character_index]] = statistics.mean(mean_character_weights) * 2
                else: 
                    incorrect_characters[unlock_seq[next_character_index]] = 4

        min_val = min([v for k,v in incorrect_characters.items() if v > 0] or [1])

        for i in unlocked_characters:
            if incorrect_characters[i] == 0:
                incorrect_characters[i] = min_val / 3
    
    incorrect_characters = min_max_normalisation(incorrect_characters, character_index_map)
    character_times = min_max_normalisation(character_times, character_index_map)
    if not seed_sequence:
        start_index = random.randint(0, len(wordnet_data)- word_len -1)
        generated_text = wordnet_data[start_index: start_index+word_len]
    else: 
        generated_text = seed_sequence[len(seed_sequence)-word_len: len(seed_sequence)]
    
    org_text = generated_text
    all_generated_text = generated_text
    new_character = None
    for i in range(250):
        seed_data = np.zeros((1, word_len, len(characters)))
        for j in range(len(generated_text)):
            seed_data[0,j,character_index_map[generated_text[j]]] = 1.
        preds = model.predict(seed_data, batch_size=1)[0]

        net_predicted_character = characters[get_predicted_text(preds, 0.8, [1 for _ in range(characters_len)], [1 for _ in range(characters_len)], character_index_map, new_character)]

        if net_predicted_character == " ":
            new_character = " "
        else:
            new_character = characters[get_predicted_text(preds, 0.8, incorrect_characters, character_times, character_index_map, new_character)]
        generated_text += new_character

        generated_text = generated_text[1:]
        all_generated_text+= new_character
    
    org_text = " ".join(org_text.split(" "))
    all_generated_text = " ".join((all_generated_text[len(org_text):len(all_generated_text)]).split(" ")[:-2]).strip()

    correct_characters_normalised = [0 for k, v in correct_characters.items()]
    
    for k, v in correct_characters.items():
        try:
            correct_characters_normalised[character_index_map[k]] = ((v - correct_characters[min(correct_characters, key=correct_characters.get)]) / (correct_characters[max(correct_characters, key=correct_characters.get)] - correct_characters[min(correct_characters, key=correct_characters.get)]))
        except:
            correct_characters_normalised[character_index_map[k]] = 0

    mastered_chars = characters_mastered(incorrect_characters_org, correct_characters_normalised, wpm, inverse_character_index_map)
    del mastered_chars[' ']


    return (all_generated_text, int(is_master(incorrect_characters_org, wpm)), mastered_chars)



def store_session_details(request_data):
    incorrect_characters  = request_data.get("incorrect_characters")
    wpm  = request_data.get("wpm")
    correct_characters  = request_data.get("correct_characters")
    character_time   = request_data.get("character_time")
    # character_id    = request_data.get("character_id")
    user_id     = request_data.get("user_id")
    character_accuracy    = request_data.get("character_accuracy")
    totalAccuracy    = request_data.get("total_accuracy")
    #accuracy

    # correct_characters_avg = json.dumps(correct_characters_avg)
    # incorrect_characters_avg = json.dumps(incorrect_characters_avg)
    # total_occurances  = json.dumps(total_occurances)
    # character_time = json.dumps(character_time)


    database_connection = None
    database_cursor = None
    error = None
    try: 
        database_connection = mysql.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            database='heroku_8af8fae4116d831',
            user='b1282a2123d519',
            password='29416dad'
        )
        if database_connection.is_connected():
            database_cursor = database_connection.cursor(dictionary=True)

            print(user_id)
            database_cursor.execute("SELECT MAX(sessionID) as sessionID FROM sessionstats WHERE user_id = '{k}' limit 1 ;".format(k = user_id))
            lastSession = database_cursor.fetchone()
            if not lastSession["sessionID"]:
                sessionID = 1
            else:
                print(lastSession["sessionID"])
                sessionID = int(lastSession["sessionID"]) + 1

            database_cursor.execute("INSERT INTO `sessionstats` (`user_id` , `WPM`  , `sessionID`, `totalAccuracy`) VALUES(%s, %s, %s, %s) ;",(user_id, wpm, sessionID, totalAccuracy))

            database_cursor.execute("select * from Users where user_id = %s;", (user_id,))
            existing_users = database_cursor.fetchone()

            updated_test_taken = existing_users["tests_taken"] + 1

            updated_wpm = (float(existing_users["tests_taken"]) * float(existing_users["words_per_min"]) + float(wpm)) / float(updated_test_taken)

            database_cursor.execute("select * from og_user_characters inner join characters on characters.character_id = og_user_characters.character_id where user_id = %s;", (user_id,))
            character_data = database_cursor.fetchall()

            updated_character_data = []
            testsessions_data = []

            for k, v in request_data["correct_characters"].items():
                for i in character_data:
                    if i['character_name'] == k:
                        updated_correct_characters = (existing_users["tests_taken"] * i["correct_characters"] + request_data["correct_characters"][k]) / (updated_test_taken)
                        updated_incorrect_characters = (existing_users["tests_taken"] * i["incorrect_characters"] + request_data["incorrect_characters"][k]) / (updated_test_taken)
                        updated_character_times = (existing_users["tests_taken"] * i["character_time"] + request_data["character_time"][k]) / (updated_test_taken)
                        try:
                            updated_accuracy = (existing_users["tests_taken"] * i["character_accuracy"] + updated_correct_characters / (updated_incorrect_characters +updated_correct_characters)) / (updated_test_taken)
                        except:
                            updated_accuracy = 0
                        updated_character_data.append((updated_correct_characters, updated_incorrect_characters, updated_character_times, updated_accuracy, user_id, i["character_id"]))
                        testsessions_data.append((updated_correct_characters, updated_incorrect_characters, updated_character_times, updated_accuracy , user_id, i["character_id"], sessionID))
                    
            database_cursor.executemany(
                """UPDATE og_user_characters SET correct_characters = %s, incorrect_characters = %s, character_time = %s ,  character_accuracy = %s WHERE user_id = %s and og_user_characters.character_id = %s;""", 
                updated_character_data
            )

            database_cursor.executemany(
                "INSERT INTO `testsessions` (`correct_characters` , `incorrect_characters`, `character_time` , `user_id` , `character_id`,`character_accuracy`, `sessionID`) VALUES(%s, %s, %s, %s, %s, %s, %s) ;",
                testsessions_data
            )

            database_cursor.execute("UPDATE users set words_per_min = %s, tests_taken = %s;", (updated_wpm, updated_test_taken))
            database_connection.commit()

    except Exception as e:
        print(e, "error")
        return (-1, None)
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    total_errors = []
    for i in range(len(updated_character_data)):
        try:
            total_errors.append(updated_character_data[i][0] / (updated_character_data[i][0] + updated_character_data[i][1]) )
        except:
            total_errors.append(0)
    return (1, int(is_master(total_errors, wpm)))


def get_session_details(request_data):

    user_id   = request_data.get("user_id")
    try: 
        database_connection = mysql.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            database='heroku_8af8fae4116d831',
            user='b1282a2123d519',
            password='29416dad'
        )
        if database_connection.is_connected():
            database_cursor = database_connection.cursor(dictionary=True)

            database_cursor.execute("SELECT MAX(sessionID) as sessionID FROM sessionstats WHERE user_id = '{k}' limit 1 ;".format(k = user_id))
            lastSession = database_cursor.fetchone()
            if not lastSession["sessionID"]:
                return "No tests yet"
            else:
                sessionID = int(lastSession["sessionID"])

        
            database_cursor.execute("SELECT * FROM sessionstats WHERE (sessionID BETWEEN '{k}' and '{l}') and user_id = '{j}';".format(k = sessionID - 10, l = sessionID, j = user_id ))
            sessionData = database_cursor.fetchall()
            database_cursor.execute("SELECT AVG(correct_characters) AS correct_characters, AVG(incorrect_characters) AS incorrect_characters, AVG(character_accuracy) AS character_accuracy, characters.character_name FROM testsessions inner join characters on characters.character_id = testsessions.character_id where (sessionID between '{k}' and '{l}') and user_id = '{j}' group by testsessions.user_id, testsessions.character_id;".format(k = sessionID - 10, l = sessionID, j = user_id ))
            aveData = database_cursor.fetchall()


            characterDict = {}

            wpmList = []
            accList = []
            for session in sessionData:
                characterDict["session_" + str(session["sessionID"])] = {
                    "WPM": session["WPM"],
                    "totalAccuracy": session["totalAccuracy"]
                }
                if (session["WPM"] is not None):
                    wpmList.append(session["WPM"])
                if (session["totalAccuracy"] is not None):
                    accList.append(session["totalAccuracy"])                    

                for character in aveData:
                    characterDict[character["character_name"]] = {"correct_characters": character["correct_characters"], "incorrect_characters": character["incorrect_characters"], "character_accuracy": character["character_accuracy"]}

            if (len(wpmList) != 0):
                wpm_ave = sum(wpmList) / len(wpmList)
            else:
                wpm_ave = None

            if (len(accList) != 0):
                acc_ave = sum(accList) / len(accList)
            else:
                acc_ave = None

            characterDict["WPM_Average"] = wpm_ave
            characterDict["Accuracy_Average"] = acc_ave
     

            return characterDict

    except Exception as e:
        print(e, "error")
        return (-1, None)