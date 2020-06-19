from flask import Flask, request
import jwt
import os
import redis
import bcrypt

app = Flask(__name__)
secret = os.environ.get('SECRET_KEY')
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if redis_client.hgetall(username):
        try:
            checked = bcrypt.checkpw(password.encode('UTF-8'), redis_client.hget(username, 'password'))
        except ValueError:
            return {
                'ok': False,
                'error': 'Invalid username/password pair'
            }
        if checked:
            role = redis_client.hget(username, 'role')
            encoded_jwt = jwt.encode({
                'username': username,
                'role': role if role else None
            }, secret, algorithm='HS256')
            return {
                'ok': True,
                'jwt': encoded_jwt.decode('UTF-8')
            }
    return {
        'ok': False,
        'error': 'Invalid username/password pair'
    }

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    role = request.get('role')
    if redis_client.hgetall(username):
        return {
            'ok': False,
            'error': 'Username already registered'
        }
    else:
        password_hash = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
        redis_client.hset(username, 'password', password_hash)
        if role:
            redis_client.hset(username, 'role', role)
        return {
            'ok': True
        }
