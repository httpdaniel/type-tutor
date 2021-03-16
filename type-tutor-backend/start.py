# from flask import Flask, request
# app = Flask(__name__)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         return register()
#     else:
#         return showRegistration()


# @app.route('/seed', methods=['GET'])
# def seed():
#     if request.method == 'GET':
#         return seed()


from flask import Flask, Response, request,render_template
import json
import bcrypt
import mysql.connector
from mysql.connector import Error
import jwt
from datetime import datetime, timedelta
import models.models

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    email = request_data.get("email")
    password = str.encode(request_data.get("password"))
    print(email)
    print(password)
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
            database_cursor.execute("select * from Users where email = %s;", (email,))
            print("This worked")
            user = database_cursor.fetchone()
            print(user)
            if user and bcrypt.checkpw(password, str.encode(user[2])):
                print("Also here")
                payload = {
                    'exp':datetime.utcnow() + timedelta(days=5),
                    'sub': user[0]
                }
                print(payload)
                token = jwt.encode(payload, "123", algorithm='HS256')
                print(token)
            else:
                error = "Invalid login credentials"

    except Exception as e:
        print(database_cursor.statement)
        error = "Internal server error" % e
    finally:
        if database_connection and database_connection.is_connected():
            if database_cursor:
                database_cursor.close()
            database_connection.close()
   
    if error:
        return Response(json.dumps({"message": error }), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": token.decode("utf-8")}), mimetype='application/json', status='200')
   
    
@app.route('/typing', methods=['POST'])
def typing():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')

    if request_data.get("token") is None:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')

    try:
        payload = jwt.decode(request_data.get("token"), "123")
        print(payload['sub'])
    except Exception:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    
    return Response(json.dumps({"message": "success"}), mimetype='application/json', status='200')



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
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
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
        return Response(json.dumps({"message": "Success registered %s" % email}), mimetype='application/json', status='201')
   


@app.route('/seed', methods=['GET'])
def seed():
    if request.method == 'GET':
        return seed()


if __name__ == "__main__":
    app.run(port=8000, debug=True)
