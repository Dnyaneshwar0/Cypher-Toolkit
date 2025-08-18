# app/routes/encrypt_routes.py
from flask import Blueprint, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import uuid
import json
from ..services.crypto_utils import encrypter

encrypt_bp = Blueprint('encrypt_bp', __name__)
UPLOAD_FOLDER = tempfile.gettempdir()

def _tmp_path(name_hint: str) -> str:
    base = secure_filename(name_hint or "file")
    stem, ext = os.path.splitext(base)
    if not ext:
        ext = ".bin"
    return os.path.join(UPLOAD_FOLDER, f"{stem}-{uuid.uuid4().hex}{ext}")

@encrypt_bp.route('/text/aes', methods=['POST'])
def encrypt_text_aes():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'password' not in data:
            return jsonify({'error': 'text and password are required'}), 400
        
        encrypted = encrypter.encrypt_aes(data['text'], data['password'])
        return jsonify({'encrypted_text': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/text/aes/decrypt', methods=['POST'])
def decrypt_text_aes():
    try:
        data = request.get_json()
        if not data or 'encrypted_text' not in data or 'password' not in data:
            return jsonify({'error': 'encrypted_text and password are required'}), 400
        
        decrypted = encrypter.decrypt_aes(data['encrypted_text'], data['password'])
        return jsonify({'decrypted_text': decrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/file/aes', methods=['POST'])
def encrypt_file_aes():
    try:
        if 'file' not in request.files or 'password' not in request.form:
            return jsonify({'error': 'file and password are required'}), 400

        file = request.files['file']
        password = request.form['password']
        
        input_path = _tmp_path(file.filename)
        file.save(input_path)
        
        encrypted_path = encrypter.encrypt_file_aes(input_path, password)
        
        return send_file(
            encrypted_path,
            download_name=f"{file.filename}.enc",
            as_attachment=True,
            max_age=0
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/file/aes/decrypt', methods=['POST'])
def decrypt_file_aes():
    try:
        if 'file' not in request.files or 'password' not in request.form:
            return jsonify({'error': 'file and password are required'}), 400

        file = request.files['file']
        password = request.form['password']
        
        input_path = _tmp_path(file.filename)
        file.save(input_path)
        
        decrypted_path = encrypter.decrypt_file_aes(input_path, password)
        
        return send_file(
            decrypted_path,
            download_name=os.path.basename(decrypted_path),
            as_attachment=True,
            max_age=0
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/keys/generate/rsa', methods=['POST'])
def generate_rsa_keys():
    try:
        data = request.get_json()
        if not data or 'passphrase' not in data:
            return jsonify({'error': 'passphrase is required'}), 400
        
        passphrase = data['passphrase'].encode()
        key_size = data.get('key_size', 2048)
        
        encrypter.generate_rsa(passphrase, key_size)
        return jsonify({'message': 'RSA keys generated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/text/rsa', methods=['POST'])
def encrypt_text_rsa():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'text is required'}), 400
        
        encrypted = encrypter.encrypt_rsa(data['text'])
        return jsonify({'encrypted_text': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/text/rsa/decrypt', methods=['POST'])
def decrypt_text_rsa():
    try:
        data = request.get_json()
        if not data or 'encrypted_text' not in data or 'passphrase' not in data:
            return jsonify({'error': 'encrypted_text and passphrase are required'}), 400
        
        passphrase = data['passphrase'].encode()
        decrypted = encrypter.decrypt_rsa(data['encrypted_text'], passphrase)
        return jsonify({'decrypted_text': decrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/text/hybrid', methods=['POST'])
def encrypt_text_hybrid():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'text is required'}), 400
        
        encrypted = encrypter.hybrid_encrypt(data['text'])
        return jsonify({'encrypted_data': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/text/hybrid/decrypt', methods=['POST'])
def decrypt_text_hybrid():
    try:
        data = request.get_json()
        if not data or 'encrypted_data' not in data or 'passphrase' not in data:
            return jsonify({'error': 'encrypted_data and passphrase are required'}), 400
        
        passphrase = data['passphrase'].encode()
        decrypted = encrypter.hybrid_decrypt(data['encrypted_data'], passphrase)
        return jsonify({'decrypted_text': decrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@encrypt_bp.route('/keys/list', methods=['GET'])
def list_keys():
    try:
        keys = encrypter.list_keys()
        return jsonify({'keys': keys})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
