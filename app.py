from flask import Flask, request
import jwt
import os
import redis

app = Flask(__name__)
secret = os.environ.get('SECRET_KEY')
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if redis_client.hgetall(username):
        if redis_client.hget(username, 'password').decode('UTF-8') == password:
            encoded_jwt = jwt.encode({'username': username}, secret, algorithm='HS256')
            return {
                'ok': True,
                'jwt': encoded_jwt.decode('UTF-8')
            }
    return {
        'ok': False
    }
