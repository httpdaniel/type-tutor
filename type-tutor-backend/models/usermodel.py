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

def get_predicted_text(predictions, temperature, incorrect_characters, character_times, character_index_map):
    most_common_predictions = predictions 
    # * np.array(incorrect_characters) * np.array(character_times)
    predictions = np.log(np.asarray(most_common_predictions).astype('float64')) / temperature
    exponential_predictions = np.exp(predictions)
    return np.argmax(np.random.multinomial(1, exponential_predictions / np.sum(exponential_predictions), 1))

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
        # if prob_a[i] == 0 and (inverse_index_map[i] == "e" or inverse_index_map[i] == "n" or inverse_index_map[i] == "i" or inverse_index_map[i] == "t" or inverse_index_map[i] == "r"):
        #     check_unlock_next = False
        # prob_a[i] = 1
    
    # unlock_seq = ['e', 'n', 'i', 't', 'r', 'l', 's', 'a', 'u', 'o', 'd', 'y', 'c', 'h', 'g', 'm', 'p', 'b', 'k', 'v', 'w', 'f', 'z', 'x', 'q', 'j']
    return prob_a

def generate_text(user_id):
    print(user_id)
    from keras import backend as K 
    K.clear_session()

    word_len = 100
    wordnet_data = "" 
    model = keras.models.load_model('./rnn_model/model.h5')

    with open("./train_rnn/wordnet_words.txt") as wordnet_words_file:
            wordnet_data = wordnet_words_file.read()

    wordnet_data = re.sub("[^a-z ]+", "", wordnet_data)
    dist = " ".join(set(wordnet_data.split(" ")))
    first_letters_dist = {
    }
    wordnet_data = dist
    for i in dist:
        if len(i):
            if i[0] not in first_letters_dist:
                first_letters_dist[i[0]] = 0
            first_letters_dist[i[0]] += 1

    characters = sorted(set(wordnet_data))
    characters_len = len(characters)

    character_index_map = {character: characters.index(character) for character in characters}
    
    database_connection = None
    database_cursor = None
    error = None
    incorrect_characters = {}
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
                    incorrect_characters[i["character_name"]] = float(i["incorrect_characters"]) / float((i["incorrect_characters"] + i["correct_characters"]))
                    character_times[i["character_name"]] = float(i["character_time"])
                except:
                    incorrect_characters[i["character_name"]] = 0
                    character_times[i["character_name"]] = 0

            wpm = character_data[0]["words_per_min"]

    except Exception as e:
        print(e)
        return "", False
        pass
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    
    fresh_start = False
    for k, v in incorrect_characters.items():
        if v == 0 and (k == "e" or k == "n" or k == "i" or k == "t" or k == "r"):
            fresh_start = True
            incorrect_characters[k] = 1

    incorrect_characters[" "] = 0.01
    character_times[" "] = 0.01

    if not fresh_start and wpm >= 40:
        unlock_next_character = False
        found_zero_character = False
        next_character_index = 0
        unlock_seq = ['e', 'n', 'i', 't', 'r', 'l', 's', 'a', 'u', 'o', 'd', 'y', 'c', 'h', 'g', 'm', 'p', 'b', 'k', 'v', 'w', 'f', 'z', 'x', 'q', 'j']
        for i in unlock_seq:
            if found_zero_character and incorrect_characters[i] != 0:
                unlock_next_character = False
                break
            if incorrect_characters[i] == 0:
                found_zero_character = True
            elif i > 0.1:
                unlock_next_character = False
                break
            else:
                next_character_index += 1
            
        if unlock_next_character:
            mean_character_weights = []
            for i in range(next_character_index-1):
                if v != 0:
                    mean_character_weights.append(incorrect_characters[i])
            incorrect_characters[unlock_seq[next_character_index]] = statistics.mean(mean_character_weights)

    incorrect_characters = min_max_normalisation(incorrect_characters, character_index_map)
    character_times = min_max_normalisation(character_times, character_index_map)

    print(character_times)
    print(incorrect_characters)

    all_generated_text = "a"
    
    for _ in range(1):
        generate_text = all_generated_text.split(" ")[-1] + " "
        print(generate_text)
        for i in range(100 - len(generate_text)):
            if len(generate_text.split(" ")[-1]) >= 6:
                add_space_prob = len(generate_text.split(" ")[-1])*0.1
                add_space = random.choices(["", " "], weights=[1 - add_space_prob, add_space_prob ] , k=1 )
                if add_space == " " or add_space_prob > 1.1:
                    generate_text += " "
                    continue

            seed_data = np.zeros((1, word_len, characters_len))
            for j in range(len(generate_text)):
                seed_data[0,j,character_index_map[generate_text[j]]] = 1.
            
            preds = model.predict(seed_data)[0]
            new_character = characters[get_predicted_text(preds, 0.6, incorrect_characters, character_times, character_index_map)]
            generate_text += new_character

        all_generated_text = generate_text if len(all_generated_text) == 1 else " ".join(all_generated_text.split(" ")[:-2]) + generate_text
    
    K.clear_session()
    print(all_generated_text)
    return (all_generated_text, int(is_master(incorrect_characters, wpm)))



def store_session_details(request_data):
    incorrect_characters  = request_data.get("incorrect_characters")
    wpm  = request_data.get("wpm")
    correct_characters  = request_data.get("correct_characters")
    character_time   = request_data.get("character_time")
    user_id = request_data.get("user_id")

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

            database_cursor.execute("SELECT MAX(sessionID) as sessionID FROM testsessions WHERE user_id = '{k}' limit 1 ;".format(k = user_id))
            lastSession = database_cursor.fetchone()
            if not lastSession["sessionID"]:
                sessionID = 1
            else:
                sessionID = int(lastSession) + 1

            database_cursor.execute("INSERT INTO `sessionstats` (`user_id` , `WPM`  , `sessionID`) VALUES(%s, %s, %s) ;",(user_id, wpm, sessionID))

            database_cursor.execute("select * from Users where user_id = %s;", (user_id,))
            existing_users = database_cursor.fetchone()

            updated_test_taken = existing_users["tests_taken"] + 1
            updated_wpm = (existing_users["tests_taken"] * existing_users["words_per_min"] + wpm) / (updated_test_taken)
            
            database_cursor.execute("select * from og_user_characters inner join characters on characters.character_id = og_user_characters.character_id where user_id = %s;", (user_id,))
            character_data = database_cursor.fetchall()
            updated_character_data = []
            testsessions_data = []
            for k, v in request_data["correct_characters"].items():
                for i in character_data:
                    if i['character_name'] == k:
                        updated_correct_characters = (existing_users["tests_taken"] * i["correct_characters"] + request_data["correct_characters"][k]) / (updated_test_taken)
                        updated_incorrect_characters = (existing_users["tests_taken"] * i["incorrect_characters"] + request_data["incorrect_characters"][k]) / (updated_test_taken)
                        updated_character_times = (existing_users["tests_taken"] * i["character_time"] + request_data["character_times"][k]) / (updated_test_taken)
                        updated_character_data.append((updated_correct_characters, updated_incorrect_characters, updated_character_times, user_id, i["character_id"]))
                        testsessions_data.append((updated_correct_characters, updated_incorrect_characters, updated_character_times, user_id, i["character_id"], sessionID))
                    
            database_cursor.executemany(
                """UPDATE og_user_characters SET correct_characters = %s, incorrect_characters = %s, character_time = %s WHERE user_id = %s and og_user_characters.character_id = %s;""", 
                updated_character_data
            )

            database_cursor.executemany(
                "INSERT INTO `testsessions` (`correct_characters` , `incorrect_characters`, `character_time` , `user_id` , `character_id`, `sessionID`) VALUES(%s, %s, %s, %s, %s, %s) ;",
                testsessions_data
            )

            database_cursor.execute("UPDATE users set words_per_min = %s, tests_taken = %s;", (updated_wpm, updated_test_taken,))
            database_connection.commit()

    except Exception as e:
        print(e, "error")
        return (-1, None)
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    total_errors = [updated_character_data[i][0] / (updated_character_data[i][0] + updated_character_data[i][1]) for i in range(len(updated_character_data))]
    return (1, int(is_master(total_errors, wpm)))