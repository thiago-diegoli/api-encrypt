import hashlib
import json
from flask import request, jsonify
from auth import authenticate_request

STEP_FILE = 'storage/steps.txt'

def load_steps():
    try:
        with open(STEP_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_steps(steps):
    with open(STEP_FILE, 'w') as f:
        json.dump(steps, f)

def caesar_cipher(text, step, decrypt=False):
    if decrypt:
        step = -step
    return ''.join([chr((ord(char) + step) % 256) for char in text])

def encrypt_message():
    user = authenticate_request()
    if not user:
        return jsonify({'message': 'Token inválido'}), 401

    data = request.get_json()
    message = data.get('message')
    step = data.get('step')

    if not isinstance(step, int):
        return jsonify({'message': 'O passo deve ser um número inteiro'}), 400

    encrypted = caesar_cipher(message, step)
    step_hash = hashlib.sha256(str(step).encode()).hexdigest()

    steps = load_steps()
    steps[step_hash] = step
    save_steps(steps)

    return jsonify({'encrypted_message': encrypted, 'step_hash': step_hash}), 200

def decrypt_message():
    user = authenticate_request()
    if not user:
        return jsonify({'message': 'Token inválido'}), 401

    data = request.get_json()
    message = data.get('message')
    step_hash = data.get('step_hash')

    steps = load_steps()
    step = steps.get(step_hash)

    if step is None:
        return jsonify({'message': 'Passo não encontrado'}), 404

    decrypted = caesar_cipher(message, step, decrypt=True)
    return jsonify({'decrypted_message': decrypted}), 200
