import os
import base64
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.exceptions import InvalidSignature

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

# RSA

KEYS_DIR = os.path.join(os.path.dirname(__file__), '../../../keys')
os.makedirs(KEYS_DIR, exist_ok=True)

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
    priv_path = os.path.join(KEYS_DIR, "rsa_private.pem")
    pub_path = os.path.join(KEYS_DIR, "rsa_public.pem")
    with open(priv_path, "wb") as f:
        f.write(priv_pem)
    with open(pub_path, "wb") as f:
        f.write(pub_pem)
    return priv_path, pub_path

def encrypt_rsa(plaintext: str) -> str:
    with open(os.path.join(KEYS_DIR, "rsa_public.pem"), "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    ct = pub_key.encrypt(
        plaintext.encode(),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(ct).decode()

def decrypt_rsa(ciphertext: str, passphrase: bytes) -> str:
    priv_path = os.path.join(KEYS_DIR, "rsa_private.pem")
    with open(priv_path, "rb") as f:
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
    priv_path = os.path.join(KEYS_DIR, "ecc_private.pem")
    pub_path = os.path.join(KEYS_DIR, "ecc_public.pem")
    with open(priv_path, "wb") as f:
        f.write(priv_pem)
    with open(pub_path, "wb") as f:
        f.write(pub_pem)
    return priv_path, pub_path

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
    except InvalidSignature:
        return False

# SHA256 Fingerprint

def sha256_fingerprint(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
