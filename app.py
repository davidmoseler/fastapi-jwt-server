from fastapi import FastAPI
import jwt
import os
import redis
import bcrypt
from pydantic import BaseModel

app = FastAPI()
secret = os.environ.get('SECRET_KEY')
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))

class User(BaseModel):
    username: str
    password: str

class NewUser(User):
    role: str

@app.post('/authenticate')
async def authenticate(user: User):
    print(user)
    if redis_client.hgetall(user.username):
        try:
            checked = bcrypt.checkpw(user.password.encode('UTF-8'), redis_client.hget(user.username, 'password'))
        except ValueError:
            return {
                'ok': False,
                'error': 'Invalid username/password pair'
            }
        if checked:
            role = redis_client.hget(user.username, 'role')
            encoded_jwt = jwt.encode({
                'username': user.username,
                'role': role.decode('UTF-8') if role else None
            }, secret, algorithm='HS256')
            return {
                'ok': True,
                'jwt': encoded_jwt.decode('UTF-8')
            }
    return {
        'ok': False,
        'error': 'Invalid username/password pair'
    }

@app.post('/register')
async def register(user: NewUser):
    if redis_client.hgetall(user.username):
        return {
            'ok': False,
            'error': 'Username already registered'
        }
    else:
        password_hash = bcrypt.hashpw(user.password.encode('UTF-8'), bcrypt.gensalt())
        redis_client.hset(user.username, 'password', password_hash)
        if user.role:
            redis_client.hset(user.username, 'role', user.role)
        return {
            'ok': True
        }
