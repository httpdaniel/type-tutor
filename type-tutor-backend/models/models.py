from flask import Flask, Response, request,render_template
import json
import bcrypt
import mysql.connector
from mysql.connector import Error
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/minisession', methods=['POST'])
def mini_session():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    incorrect_characters  = request_data.get("incorrect_characters")
    correct_characters  = request_data.get("correct_characters")
    total_occurances  = request_data.get("total_occurances")
    character_time   = request_data.get("character_time")
    character_id    = request_data.get("character_id")
    user_id     = request_data.get("user_id")



    print(incorrect_characters)
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
            database_cursor.execute("INSERT INTO `user_characters` (`incorrect_characters` , `correct_characters`  , `total_occurances` , `character_time` , `character_id` , `user_id`  ) VALUES(%s, %s, %s, %s, %s, %s);",(incorrect_characters,correct_characters, total_occurances, character_time, character_id, user_id))
            database_connection.commit()
        else:
            error = "There was a problem connecting to the database"
    except Exception as e:
        print(database_cursor.statement)
        error = "Internal server error"
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
    
    if error:
        return Response(json.dumps({"message": error }), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": "Successfully committed details"}), mimetype='application/json', status='201')





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