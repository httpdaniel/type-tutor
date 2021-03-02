from flask import Flask, request
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register()
    else:
        return showRegistration()


@app.route('/seed', methods=['GET'])
def seed():
    if request.method == 'GET':
        return seed()
