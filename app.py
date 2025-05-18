from flask import Flask
from auth import register, login
from encrypt import encrypt_message, decrypt_message

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    return register()

@app.route('/login', methods=['POST'])
def login_user():
    return login()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    return encrypt_message()

@app.route('/decrypt', methods=['POST'])
def decrypt():
    return decrypt_message()

if __name__ == '__main__':
    app.run(debug=True)
