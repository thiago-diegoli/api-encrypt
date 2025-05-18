import jwt
import bcrypt
import json
import os
from flask import request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
USERS_FILE = 'storage/users.txt'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Dados não fornecidos'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Nome de usuário e senha são obrigatórios'}), 400

    users = load_users()

    if username in users:
        return jsonify({'message': 'Usuário já existe'}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username not in users:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if not bcrypt.checkpw(password.encode(), users[username].encode()):
        return jsonify({'message': 'Senha incorreta'}), 401

    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(hours=2)}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}), 200

def authenticate_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    else:
        token = auth_header
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
