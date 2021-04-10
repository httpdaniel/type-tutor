from flask import Flask, Response, request,render_template
import json
import bcrypt
import mysql.connector
from mysql.connector import Error
import jwt
from datetime import datetime, timedelta
import models.models 
import models.usermodel as user_model

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
    token = ""
    try:
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
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
        else:
            error = "error connecting to database"
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
    except Exception as e:
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

                database_cursor.execute("select * from Users where email = %s;", (email,))
                user_id = database_cursor.fetchone()[0]
                
                database_cursor.execute("select character_id from characters")
                characters = database_cursor.fetchall()

                database_cursor.executemany("""
                        INSERT INTO og_user_characters (
                            incorrect_characters, correct_characters, total_occurances, character_time, character_id, user_id
                        ) VALUES (0, 0, 0, 0, %s, %s);
                    """, [(i[0], user_id) for i in characters ])

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


@app.route('/submit', methods=['POST'])
def submit():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    

    try:
        payload = jwt.decode(request_data.get("token"), "123")
        user_id = payload['sub']
        email = request_data.get("email")
        error = None
        database_connection = None
        database_cursor = None
        try:
            database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                                database='heroku_8af8fae4116d831',
                                                user='b1282a2123d519',
                                                password='29416dad')
            if database_connection.is_connected():
                database_cursor = database_connection.cursor()
                database_cursor.execute("select * from Users where email = %s;", (email,))
                user = database_cursor.fetchone()
                if (not user) or  (not user[0] == user_id):
                    return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
        except Exception as e:
            print(database_cursor.statement)
            error = "Internal server error" % e
        finally:
            if database_connection and database_connection.is_connected():
                if database_cursor:
                    database_cursor.close()
                database_connection.close()
        if error: 
            return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    except Exception as e:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    
    request_data["user_id"] = user_id

    response, master = user_model.store_session_details(request_data)

    if(not response):
        return Response(json.dumps({"message": response }), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": "Successfully committed details", "master": master}), mimetype='application/json', status='201')




@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    email = request_data.get("email")
    password = str.encode(request_data.get("password"))
    token = request_data.get("token")
    database_connection = None
    database_cursor = None
    error = None
    try:
        payload = jwt.decode(token, "123")
        user_id = payload['sub']
        
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
        if database_connection.is_connected():
            database_cursor = database_connection.cursor()
            database_cursor.execute("select * from Users where email = %s;", (email,))
            user = database_cursor.fetchone()
            if user and user[0] == user_id and bcrypt.checkpw(password, str.encode(user[2])):
                database_cursor.execute("DELETE FROM og_user_characters where user_id = %s;", (user_id,))
                database_cursor.execute("DELETE FROM users where user_id = %s;", (user_id,))
                database_connection.commit()

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
        return Response(json.dumps({"message": "successfully deleted account"}), mimetype='application/json', status='200')
   

@app.route('/update_password', methods=['PUT'])
def update_password():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    email = request_data.get("email")
    old_password = str.encode(request_data.get("old_password"))
    password = str.encode(request_data.get("password"))
    token = request_data.get("token")
    database_connection = None
    database_cursor = None
    error = None
    try:
        payload = jwt.decode(token, "123")
        user_id = payload['sub']
        
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
        if database_connection.is_connected():
            database_cursor = database_connection.cursor()
            database_cursor.execute("select * from Users where email = %s;", (email,))
            user = database_cursor.fetchone()
            if user and user[0] == user_id and bcrypt.checkpw(old_password, str.encode(user[2])):
                password_hash = bcrypt.hashpw(password, bcrypt.gensalt(5))
                database_cursor.execute('UPDATE Users set password = %s where user_id = %s;', (password_hash, user_id))
                database_connection.commit()

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
        return Response(json.dumps({"message": "successfully deleted account"}), mimetype='application/json', status='200')
   


@app.route('/update_email', methods=['PUT'])
def email():
    try:
        request_data = json.loads(request.data)
    except:
        return Response(json.dumps({'message': "Invalid JSON data"}), mimetype='application/json', status='400')
    
    old_email = request_data.get("old_email")
    email = request_data.get("email")
    password = str.encode(request_data.get("password"))
    token = request_data.get("token")
    database_connection = None
    database_cursor = None
    error = None
    try:
        payload = jwt.decode(token, "123")
        user_id = payload['sub']
        database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                            database='heroku_8af8fae4116d831',
                                            user='b1282a2123d519',
                                            password='29416dad')
        if database_connection.is_connected():
            database_cursor = database_connection.cursor()
            database_cursor.execute("select * from Users where email = %s;", (old_email,))
            user = database_cursor.fetchone()
            if user and user[0] == user_id and bcrypt.checkpw(password, str.encode(user[2])):
                database_cursor.execute("select * from Users where email = %s;", (email,))
                user_exists = database_cursor.fetchone()
                
                if not user_exists:
                    database_cursor.execute('UPDATE Users set email = %s where user_id = %s;', (email, user_id))
                    database_connection.commit()
                else:
                    error = "A user already exists with this email"

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
        return Response(json.dumps({"message": "successfully deleted account"}), mimetype='application/json', status='200')
   

@app.route('/generate_text', methods=['GET'])
def generate_text():
    token = request.args.get('token')
    email = request.args.get('email')
    
    try:
        payload = jwt.decode(token, "123")
        user_id = payload['sub']
        error = None
        database_connection = None
        database_cursor = None
        try:
            database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                                database='heroku_8af8fae4116d831',
                                                user='b1282a2123d519',
                                                password='29416dad')
            if database_connection.is_connected():
                database_cursor = database_connection.cursor()
                database_cursor.execute("select * from Users where email = %s;", (email,))
                user = database_cursor.fetchone()
                if (not user) or  (not user[0] == user_id):
                    return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
        except Exception as e:
            print(database_cursor.statement)
            error = "Internal server error" % e
        finally:
            if database_connection and database_connection.is_connected():
                if database_cursor:
                    database_cursor.close()
                database_connection.close()
        if error: 
            return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
   
    except Exception as e:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    
    generated_text, master, mastered_characters = user_model.generate_text(user_id)
    
    return Response(json.dumps({"text": generated_text, "master": master, "mastered_characters": mastered_characters}), mimetype='application/json', status='201')

@app.route('/generate_next_sequence', methods=['GET'])
def generate_next_sequence():
    token = request.args.get('token')
    email = request.args.get('email')
    text = request.args.get('text')
    
    try:
        payload = jwt.decode(token, "123")
        user_id = payload['sub']
        error = None
        database_connection = None
        database_cursor = None
        try:
            database_connection = mysql.connector.connect(host='eu-cdbr-west-03.cleardb.net',
                                                database='heroku_8af8fae4116d831',
                                                user='b1282a2123d519',
                                                password='29416dad')
            if database_connection.is_connected():
                database_cursor = database_connection.cursor()
                database_cursor.execute("select * from Users where email = %s;", (email,))
                user = database_cursor.fetchone()
                if (not user) or  (not user[0] == user_id):
                    return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
        except Exception as e:
            print(database_cursor.statement)
            error = "Internal server error" % e
        finally:
            if database_connection and database_connection.is_connected():
                if database_cursor:
                    database_cursor.close()
                database_connection.close()
        if error: 
            return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
   
    except Exception as e:
        return Response(json.dumps({'message': "Unauthorised"}), mimetype='application/json', status='400')
    
    generated_text, master, mastered_characters = user_model.generate_text(user_id, text)
    
    return Response(json.dumps({"text": generated_text, "master": master, "mastered_characters": mastered_characters}), mimetype='application/json', status='201')



if __name__ == "__main__":
    app.run(port=8000, debug=True)
