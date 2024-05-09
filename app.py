# app.py
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, abort, send_file, Response
from web3 import Web3, HTTPProvider
from os import environ
from eth_account.messages import encode_defunct
import logging
import ipfshttpclient
import io
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
        return redirect(url_for('login'))
    user_address = session['user']  # Retrieve the user address from the session
    return render_template('dashboard.html', user_address=user_address)


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
    hash_value = res['Hash']
    return render_template('upload.html', hash=hash_value)

@app.route('/download', methods=['GET'])
def show_download_page():
    # This route just renders the download page.
    return render_template('download.html')

@app.route('/download/file', methods=['GET'])
def download_file():
    hash_value = request.args.get('hash')
    if not hash_value:
        return jsonify({'error': 'No hash provided'}), 400
    
    try:
        file_data = client.cat(hash_value)
        return send_file(
            io.BytesIO(file_data),
            mimetype='application/octet-stream',  # Ensures the browser treats it as a binary file
            as_attachment=True,
            download_name=f"{hash_value}.ipfs"  # Suggests a default filename for the download
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404
if __name__ == '__main__':
    app.run(debug=True, port=5000)