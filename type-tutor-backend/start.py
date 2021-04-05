from flask import Flask, Response, request,render_template
import json
import bcrypt
import mysql.connector
from mysql.connector import Error
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    email = request_data.get("email")
    password = str.encode(request_data.get("password"))
    database_connection = None
    database_cursor = None
    error = None
    try:
        database_connection = mysql.connector.connect(host='localhost',
                                            database='Touch_Typing_Tutor',
                                            user='josh',
                                            password='josh',
                                            port = 3306)
        if database_connection.is_connected():
            database_cursor = database_connection.cursor()
            database_cursor.execute("select * from Users where email = %s;", (email,))
            user = database_cursor.fetchone()
            if user and bcrypt.checkpw(password, str.encode(user[2])):
                payload = {
                    'exp':datetime.utcnow() + timedelta(days=5),
                    'sub': user[0]
                }
                token = jwt.encode(payload, "123", algorithm='HS256')
            else:
                error = "Invalid login credentials"

    except Exception:
        error = "Internal server error"
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
   
    if error:
        return Response(json.dumps({"message": error }), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": token.decode("utf-8")}), mimetype='application/json', status='200')



@app.route('/register', methods=['POST'])
def register():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')

    email = request_data.get("email")
    password = str.encode(request_data.get("password"))
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt(5))
    database_connection = None
    database_cursor = None
    error = None
    try:
        database_connection = mysql.connector.connect(host='localhost',
                                            database='Touch_Typing_Tutor',
                                            user='josh',
                                            password='josh',
                                            port = 3306)
        if database_connection.is_connected():
            database_cursor = database_connection.cursor()
            database_cursor.execute("select * from Users where email = %s;", (email,))
            existing_users = database_cursor.fetchall()
            if not list(existing_users):
                database_cursor.execute('INSERT INTO Users (email, password) VALUES (%s, %s);', (email, password_hash))
                database_connection.commit()
            else:
                error = "A user with %s already exists" % email

    except Exception as e:
        print(e)
        error = "Internal server error"
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
   
    if error:
        return Response(json.dumps({"message": error }), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": "Success registered %s" % email}), mimetype='application/json', status='201')
   

@app.route('/typing/submit', methods=['POST'])
def typing():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    if request_data.get("token") is None:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')

    try:
        payload = jwt.decode(request_data.get("token"), "123")
        user_id = payload['sub']
    except Exception:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    

    database_connection = None
    database_cursor = None
    error = None

    try:
        database_connection = mysql.connector.connect(host='localhost',
                                            database='Touch_Typing_Tutor',
                                            user='josh',
                                            password='josh',
                                            port = 3306)
        if database_connection.is_connected():
            database_cursor = database_connection.cursor(dictionary=True)
            database_cursor.execute("select * from Users where user_id = %s;", (user_id,))
            existing_users = database_cursor.fetchone()
            existing_users["words_per_min_most_recent"] = float(existing_users["words_per_min_most_recent"])
            existing_users["words_per_min"] = float(existing_users["words_per_min"])
            existing_users["words_per_min_total"] = float(existing_users["words_per_min_total"])
            print(json.dumps(existing_users, indent=4))
            if existing_users["words_per_min_total"] == 0:
                print("no info")
                words_per_min_most_recent = request_data["wpm"]
                words_per_min = request_data["wpm"]
                words_per_min_total = request_data["wpm"]
                tests_taken = 1
            else:
                tests_taken = existing_users["tests_taken"]
                words_per_min_most_recent = request_data["wpm"]
                words_per_min_total = existing_users["words_per_min_total"]
                words_per_min = (tests_taken * existing_users["words_per_min"] + words_per_min_most_recent) / (tests_taken + 1)
                tests_taken += 1

            database_cursor.execute(
            """
                UPDATE Users 
                SET words_per_min_most_recent = %s, tests_taken = %s, words_per_min_total = %s, words_per_min = %s
                where user_id = %s;
            """, (words_per_min_most_recent, tests_taken, words_per_min_total, words_per_min, user_id,)
            )
            print(words_per_min_most_recent, tests_taken, words_per_min_total, words_per_min, user_id)
            database_connection.commit()
        times = {}

        # character_times
        for k, v in request_data["character_times"]:
            pass
        # write query get sql join tables
        # insert then update

    except Exception as e:
        print(e) 
        error = "Internal server error"
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
   
   

   

    # 1 add times to database
    # 2 add errors to database
    # 3 add correct times to db


    return Response(json.dumps({"message": "success"}), mimetype='application/json', status='200')



@app.route('/seed', methods=['GET'])
def seed():
    if request.method == 'GET':
        return seed()
