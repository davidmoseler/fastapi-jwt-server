from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)
secret = os.environ.get('SECRET_KEY')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f"User(name={self.name})"

@app.route('/', methods=['POST'])
def authenticate(json=None):
    user = User.query.first()
    encoded_jwt = jwt.encode({'name': user.name}, secret, algorithm='HS256')
    return {
        'jwt': encoded_jwt.decode('UTF-8')
    }
