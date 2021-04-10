from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b1282a2123d519:29416dad@eu-cdbr-west-03.cleardb.net/models'
db = SQLAlchemy(app) 

class usermodel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    inorrect_letters = db.Column(db.Integer)
    prop_wrong_chars = db.Column(db.Float)
    letter_per_sec = db.Column(db.Integer)

if  __name__ == "__main__":
    app.run(debug=True)