from flask import Flask, Response, request,render_template
import json
import bcrypt
import mysql.connector
from mysql.connector import Error
import jwt
from datetime import datetime, timedelta

# mysql  -h eu-cdbr-west-03.cleardb.net -P 3306  -u b1282a2123d519 -p

app = Flask(__name__)

# def calculate_avg(old_average):
#     old_avg = (new_mean * new_total_occurances - old_value ) / (old_total_occurances)
#     new_avg = (incorrect_characters['a'] * total_occurances['a'] + current_a_value) / (total_occurances['a'] + 1)
#     # do for incorrect, correct + times
#     old_values_exist = False
#     for k,v in old_correct_characters.items():
#         if v > 0:
#             old_values_exist = True
#             break

#     if old_values_exist:

def calculate_json_avg(correct_values, incorrect_values):
    incorrect_json = {}
    correct_json = {}
    total_occurrences = {}
    incorrect_sum = 0
    correct_sum =0 
    total = 0 


    for correct,incorrect in zip(correct_values.items(), incorrect_values.items()):
        average_correct = correct[1] / (correct[1] + incorrect[1])
        average_incorrect = incorrect[1] / (correct[1] + incorrect[1])
        occurrences = (correct[1] + incorrect[1])
        incorrect_json[incorrect[0]] = average_incorrect
        correct_json[correct[0]] = average_correct
        total_occurrences[incorrect[0]] = occurrences
        incorrect_sum = incorrect_sum + incorrect[1]
        correct_sum = correct_sum + correct[1]
        total = total + occurrences
    correct_avg = correct_sum/ total
    incorrect_avg = incorrect_sum/total
    return (correct_json, incorrect_json, total_occurrences, correct_avg, incorrect_avg)






        


            

            
    # get the old average for the keys (time correctness incorrectness)

# update new values for keys (time correctness incorrectness)


# @app.route('/minisession', methods=['POST'])
def mini_session_fn(request_data):
    # try:
    #     request_data = json.loads(request.data)
    # except:
    #     return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')

    
    
    incorrect_characters  = request_data.get("incorrect_characters")
    correct_characters  = request_data.get("correct_characters")
    correct_characters_avg, incorrect_characters_avg, total_occurances, correct_avg, incorrect_avg  = calculate_json_avg(correct_characters, incorrect_characters)
    character_time   = request_data.get("character_time")
    # character_id    = request_data.get("character_id")
    user_id     = request_data.get("user_id")



    # correct_characters_avg = json.dumps(correct_characters_avg)
    # incorrect_characters_avg = json.dumps(incorrect_characters_avg)
    # total_occurances  = json.dumps(total_occurances)
    # character_time = json.dumps(character_time)



    database_connection = None
    database_cursor = None
    error = None
    try:
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
        if database_connection.is_connected():
            print("Database Connected")
            database_cursor = database_connection.cursor()
            id = None
            character_id = None
            for (k,v) in correct_characters_avg.items():
                print("K is ", k)
                database_cursor.execute("SELECT character_id FROM CHARACTERS WHERE CHARACTER_NAME = '{k}' limit 1 ;".format(k = k))
                user_exists = None
                for i in database_cursor:
                    character_id = i[0]
                print(incorrect_characters_avg[k],correct_characters_avg[k], total_occurances[k], character_time[k], character_id, user_id)
                database_cursor.execute("SELECT user_id FROM og_user_characters WHERE user_id = {k} and character_id = {c};".format(k = user_id, c = character_id))
                for i in database_cursor:
                    user_exists = i[0]
                print("User exists", user_exists)

                if user_exists == None:
                    print("User exists", user_exists)
                    database_cursor.execute("INSERT INTO `OG_USER_CHARACTERS` (`incorrect_characters` , `correct_characters`  , `total_occurances` , `character_time` , `character_id` , `user_id`) VALUES(%s, %s, %s, %s, %s, %s) ;",(incorrect_characters_avg[k],correct_characters_avg[k], total_occurances[k], character_time[k], character_id, user_id ))
                else:
                    database_cursor.execute("update og_user_characters set incorrect_characters = {incorrect_characters_avg}, correct_characters  = {correct_characters_avg}, total_occurances = {total_occurances}, character_time = {character_time} where character_id = {character_id} and user_id = {user_id} ;".format(incorrect_characters_avg = incorrect_characters_avg[k],correct_characters_avg =correct_characters_avg[k], total_occurances =total_occurances[k], character_time = character_time[k], character_id = character_id, user_id = user_id  ))

                database_connection.commit()

            # database_cursor.execute("INSERT INTO `user_characters` (`incorrect_characters` , `correct_characters`  , `total_occurances` , `character_time` , `character_id` , `user_id`  ) VALUES(%s, %s, %s, %s, %s, %s);",(incorrect_characters_avg,correct_characters_avg, total_occurances, character_time, character_id, user_id))
        else:
            error = "There was a problem connecting to the database"
    except Exception as e:
        print(database_cursor.statement)
        error = "Internal server error " + e
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    
    if error:
        return error
    else:
        return None


# @app.route('/minisession', methods=['POST'])
def full_session_fn(request_data):
    # try:
    #     request_data = json.loads(request.data)
    # except:
    #     return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')

    
    
    incorrect_characters  = request_data.get("incorrect_characters")
    total_correct_characters  = request_data.get("correct_characters")
    correct_characters_avg, incorrect_characters_avg, total_occurances, correct_avg, incorrect_avg  = calculate_json_avg(correct_characters, incorrect_characters)
    character_time   = request_data.get("character_time")
    # character_id    = request_data.get("character_id")
    user_id     = request_data.get("user_id")



    # correct_characters_avg = json.dumps(correct_characters_avg)
    # incorrect_characters_avg = json.dumps(incorrect_characters_avg)
    # total_occurances  = json.dumps(total_occurances)
    # character_time = json.dumps(character_time)



    database_connection = None
    database_cursor = None
    error = None
    try:
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
        if database_connection.is_connected():
            print("Database Connected")
            database_cursor = database_connection.cursor()
            id = None
            character_id = None
            for (k,v) in correct_characters_avg.items():
                print("K is ", k)
                database_cursor.execute("SELECT character_id FROM CHARACTERS WHERE CHARACTER_NAME = '{k}' limit 1 ;".format(k = k))
                user_exists = None
                for i in database_cursor:
                    character_id = i[0]
                print(incorrect_characters_avg[k],correct_characters_avg[k], total_occurances[k], character_time[k], character_id, user_id)
                database_cursor.execute("SELECT user_id FROM testsessions WHERE user_id = {k} and character_id = {c};".format(k = user_id, c = character_id))
                for i in database_cursor:
                    user_exists = i[0]
                print("User exists", user_exists)

                if user_exists == None:
                    print("User exists", user_exists)
                    database_cursor.execute("INSERT INTO `testsessions` (`incorrect_characters` , `correct_characters`  , `total_occurances` , `character_time` , `character_id` , `user_id`) VALUES(%s, %s, %s, %s, %s, %s) ;",(incorrect_characters_avg[k],correct_characters_avg[k], total_occurances[k], character_time[k], character_id, user_id ))
                else:
                    database_cursor.execute("update testsessions set incorrect_characters = {incorrect_characters_avg}, correct_characters  = {correct_characters_avg}, total_occurances = {total_occurances}, character_time = {character_time} where character_id = {character_id} and user_id = {user_id} ;".format(incorrect_characters_avg = incorrect_characters_avg[k],correct_characters_avg =correct_characters_avg[k], total_occurances =total_occurances[k], character_time = character_time[k], character_id = character_id, user_id = user_id  ))

                database_connection.commit()

            # database_cursor.execute("INSERT INTO `user_characters` (`incorrect_characters` , `correct_characters`  , `total_occurances` , `character_time` , `character_id` , `user_id`  ) VALUES(%s, %s, %s, %s, %s, %s);",(incorrect_characters_avg,correct_characters_avg, total_occurances, character_time, character_id, user_id))
        else:
            error = "There was a problem connecting to the database"
    except Exception as e:
        print(database_cursor.statement)
        error = "Internal server error " + e
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    
    if error:
        return error
    else:
        return None




# count_letters  = {'p':20,'a':27}

# prop_wrong_chars = {'a': 12/count_letters['a'], 'p':12/count_letters['p']}



# # create a fun => set threshold for the wrong words
# wrong_words = {}

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
    app.run(port=8000, debug=True)


# CREATE TABLE User_Characters (
# 	user_characters_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
#     incorrect_characters JSON NOT NULL,
#     correct_characters JSON NOT NULL,
#     total_occurances JSON NOT NULL,
# 	character_time JSON NOT NULL,
#     CORRECT_AVERAGE FLOAT NOT NULL,
#     INCORRECT_AVERAGE FLOAT NOT NULL, 
#     character_id int NOT NULL, 
#     user_id int NOT NULL, 
# 	FOREIGN KEY (character_id) REFERENCES Characters(character_id),
#     FOREIGN KEY (user_id) REFERENCES Users(user_id)
# );