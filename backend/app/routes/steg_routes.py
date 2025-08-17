# app/routes/steg_routes.py
from flask import Blueprint, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import uuid
from ..services import steganography

steg_bp = Blueprint('steg_bp', __name__)
UPLOAD_FOLDER = tempfile.gettempdir()

def _tmp_path(name_hint: str) -> str:
    base = secure_filename(name_hint or "file")
    stem, ext = os.path.splitext(base)
    if not ext:
        ext = ".bin"
    return os.path.join(UPLOAD_FOLDER, f"{stem}-{uuid.uuid4().hex}{ext}")

@steg_bp.route('/encode', methods=['POST'])
def encode():
    try:
        if 'carrier' not in request.files or 'secret' not in request.files:
            return jsonify({'error': 'carrier and secret files are required'}), 400

        carrier_file = request.files['carrier']
        secret_file = request.files['secret']

        carrier_path = _tmp_path(carrier_file.filename)
        secret_path = _tmp_path(secret_file.filename)
        output_path = _tmp_path('encoded_output.png')

        carrier_file.save(carrier_path)
        secret_file.save(secret_path)

        steganography.encode_image_in_image(carrier_path, secret_path, output_path)

        return send_file(
            output_path,
            mimetype='image/png',
            download_name='encoded_output.png',  # display inline + allows download name
            as_attachment=False,
            max_age=0
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@steg_bp.route('/decode', methods=['POST'])
def decode():
    try:
        if 'encoded' not in request.files:
            return jsonify({'error': 'encoded file is required'}), 400

        encoded_file = request.files['encoded']

        encoded_path = _tmp_path(encoded_file.filename)
        output_path = _tmp_path('decoded_output.png')

        encoded_file.save(encoded_path)

        steganography.decode_image_from_image(encoded_path, output_path)

        return send_file(
            output_path,
            mimetype='image/png',
            download_name='decoded_output.png',
            as_attachment=False,
            max_age=0
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@steg_bp.route('/diff', methods=['POST'])
def diff():
    try:
        if 'original' not in request.files or 'encoded' not in request.files:
            return jsonify({'error': 'original and encoded files are required'}), 400

        original_file = request.files['original']
        encoded_file = request.files['encoded']

        original_path = _tmp_path(original_file.filename)
        encoded_path = _tmp_path(encoded_file.filename)
        output_path = _tmp_path('diff_map.png')

        original_file.save(original_path)
        encoded_file.save(encoded_path)

        steganography.generate_diff_map_image(original_path, encoded_path, output_path)

        return send_file(
            output_path,
            mimetype='image/png',
            download_name='diff_map.png',
            as_attachment=False,
            max_age=0
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
