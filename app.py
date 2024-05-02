# app.py
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, abort
from web3 import Web3, HTTPProvider
from os import environ
from eth_account.messages import encode_defunct
import logging
import ipfshttpclient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY', 'very_secret_key')  # Important for session security
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

logging.basicConfig(level=logging.INFO)

# Establish a connection to an Ethereum node via Web3
web3_provider = environ.get('WEB3_PROVIDER', 'http://localhost:8545')
w3 = Web3(HTTPProvider(web3_provider))
if not w3.is_connected():
    logging.error("Failed to connect to the Ethereum node.")
else:
    logging.info("Successfully connected to the Ethereum node.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        user_address = data['address']
        signature = data['signature']
        message = data['message']

        msg = encode_defunct(text=message)

        try:
            signer = w3.eth.account.recover_message(msg, signature=signature)
            if signer.lower() == user_address.lower():
                session['user'] = user_address
                logging.info(f"User {user_address} logged in successfully.")
                return jsonify({'success': True})
            else:
                logging.warning(f"Failed login attempt for {user_address}")
                return jsonify({'success': False}), 401
        except Exception as e:
            logging.error(f"Signature recovery failed: {e}")
            return jsonify({'success': False}), 400

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return login()  # Reuse login logic for registration

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        logging.warning("Unauthorized access attempt to dashboard.")
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    if user:
        logging.info(f"User {user} logged out successfully.")
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    res = client.add(file)
    return jsonify({'message': 'File uploaded', 'hash': res['Hash']})

@app.route('/download/<hash>', methods=['GET'])
def get_file(hash):
    try:
        file_data = client.cat(hash)
        return file_data
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)