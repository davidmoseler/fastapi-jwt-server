from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f"User(name={self.name})"

db.create_all()

user = User(name='fulano')
db.session.add(user)
db.session.commit()

@app.route('/', methods=['POST'])
def authenticate(json=None):
    user = User.query.first()
    return {
        'name': user.name
    }
