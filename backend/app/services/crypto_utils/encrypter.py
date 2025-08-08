import os
import base64
import json
import hashlib
import shutil
import zipfile
import qrcode
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec, dh
from cryptography.x509 import NameOID, CertificateBuilder, random_serial_number
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from datetime import datetime, timedelta

# Resolve project root and keys dir
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
KEYS_DIR = os.path.join(PROJECT_ROOT, 'backend', 'keys')
os.makedirs(KEYS_DIR, exist_ok=True)

# AES

def encrypt_aes(plaintext: str, password: str) -> str:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    pad_len = 16 - len(plaintext.encode()) % 16
    padded = plaintext.encode() + bytes([pad_len] * pad_len)
    ct = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(salt + iv + ct).decode()

def decrypt_aes(ciphertext: str, password: str) -> str:
    data = base64.b64decode(ciphertext)
    salt, iv, ct = data[:16], data[16:32], data[32:]
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ct) + decryptor.finalize()
    pad_len = padded_plain[-1]
    return padded_plain[:-pad_len].decode()

def encrypt_file_aes(filepath: str, password: str) -> str:
    with open(filepath, 'rb') as f:
        data = f.read()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    pad_len = 16 - len(data) % 16
    padded = data + bytes([pad_len] * pad_len)
    ct = encryptor.update(padded) + encryptor.finalize()
    out = filepath + ".enc"
    with open(out, "wb") as f:
        f.write(salt + iv + ct)
    return out

def decrypt_file_aes(filepath: str, password: str) -> str:
    with open(filepath, 'rb') as f:
        data = f.read()
    salt, iv, ct = data[:16], data[16:32], data[32:]
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ct) + decryptor.finalize()
    pad_len = padded_plain[-1]

    # Auto-recover original extension:
    if filepath.endswith(".enc"):
        out = filepath[:-4]  # strip `.enc`
        out_parts = os.path.splitext(out)
        out = f"{out_parts[0]}_dec{out_parts[1]}"
    else:
        out = filepath + "_dec"

    with open(out, "wb") as f:
        f.write(padded_plain[:-pad_len])
    return out

# RSA

def generate_rsa(passphrase: bytes, key_size=2048):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    priv_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(passphrase)
    )
    pub_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(os.path.join(KEYS_DIR, "rsa_private.pem"), "wb") as f:
        f.write(priv_pem)
    with open(os.path.join(KEYS_DIR, "rsa_public.pem"), "wb") as f:
        f.write(pub_pem)

def encrypt_rsa(plaintext: str) -> str:
    with open(os.path.join(KEYS_DIR, "rsa_public.pem"), "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    ct = pub_key.encrypt(
        plaintext.encode(),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(ct).decode()

def decrypt_rsa(ciphertext: str, passphrase: bytes) -> str:
    with open(os.path.join(KEYS_DIR, "rsa_private.pem"), "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=passphrase)
    ct = base64.b64decode(ciphertext)
    pt = priv_key.decrypt(
        ct,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return pt.decode()

# ECC

def generate_ecc(passphrase: bytes):
    private_key = ec.generate_private_key(ec.SECP384R1())
    priv_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(passphrase)
    )
    pub_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(os.path.join(KEYS_DIR, "ecc_private.pem"), "wb") as f:
        f.write(priv_pem)
    with open(os.path.join(KEYS_DIR, "ecc_public.pem"), "wb") as f:
        f.write(pub_pem)

def sign_ecc(message: str, passphrase: bytes) -> str:
    with open(os.path.join(KEYS_DIR, "ecc_private.pem"), "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=passphrase)
    signature = priv_key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
    return base64.b64encode(signature).decode()

def verify_ecc(message: str, signature: str) -> bool:
    with open(os.path.join(KEYS_DIR, "ecc_public.pem"), "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    try:
        pub_key.verify(base64.b64decode(signature), message.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False

# Fingerprint & QR

def sha256_fingerprint(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def create_qr_fingerprint(data: str, out_file=None):
    QR_DIR = os.path.join(PROJECT_ROOT, 'data', 'qrcode', 'encrypt')
    os.makedirs(QR_DIR, exist_ok=True)
    if out_file is None:
        out_file = os.path.join(QR_DIR, "fingerprint_qr.png")
    else:
        out_file = os.path.join(QR_DIR, out_file)

    img = qrcode.make(data)
    img.save(out_file)


# Certificate

def create_self_signed_cert(common_name: str, passphrase: bytes):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name)
    ])
    cert = CertificateBuilder().subject_name(subject).issuer_name(issuer)\
        .public_key(private_key.public_key())\
        .serial_number(random_serial_number())\
        .not_valid_before(datetime.utcnow())\
        .not_valid_after(datetime.utcnow() + timedelta(days=365))\
        .sign(private_key, hashes.SHA256())
    key_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(passphrase)
    )
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    with open(os.path.join(KEYS_DIR, "selfsigned_cert.crt"), "wb") as f:
        f.write(cert_pem)
    with open(os.path.join(KEYS_DIR, "selfsigned_key.pem"), "wb") as f:
        f.write(key_pem)

# Key Management

def list_keys():
    return os.listdir(KEYS_DIR)

def delete_key(filename: str):
    path = os.path.join(KEYS_DIR, filename)
    if os.path.exists(path):
        os.remove(path)

# Zip

def create_encrypted_zip(files: list, password: str, zipname="archive.zip"):
    ZIP_DIR = os.path.join(os.path.dirname(__file__), '../../../../data/zip/encrypt')
    os.makedirs(ZIP_DIR, exist_ok=True)
    zip_path = os.path.join(ZIP_DIR, zipname)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for f in files:
            zipf.write(f, os.path.basename(f))
    return encrypt_file_aes(zip_path, password)

def extract_encrypted_zip(enc_zip: str, password: str):
    decrypted_zip = decrypt_file_aes(enc_zip, password)  # already auto-names it `_dec.zip`
    with zipfile.ZipFile(decrypted_zip, 'r') as zipf:
        OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../../../../data/zip/decrypt')
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        zipf.extractall(OUTPUT_DIR)


# Hybrid

def hybrid_encrypt(plaintext: str) -> str:
    aes_pass = base64.b64encode(os.urandom(16)).decode()
    aes_ct = encrypt_aes(plaintext, aes_pass)
    rsa_ct = encrypt_rsa(aes_pass)
    return json.dumps({"rsa_encrypted_key": rsa_ct, "aes_encrypted_data": aes_ct})

def hybrid_decrypt(enc_json: str, passphrase: bytes) -> str:
    data = json.loads(enc_json)
    aes_pass = decrypt_rsa(data['rsa_encrypted_key'], passphrase)
    return decrypt_aes(data['aes_encrypted_data'], aes_pass)
