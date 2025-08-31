import hmac
import hashlib

# Your secret key, same as in captcha_gen
SECRET_KEY = "supersecretkey123"

def generate_signature(image_bytes, answer, secret_key=SECRET_KEY):
    data = image_bytes + answer.encode()
    signature = hmac.new(secret_key.encode(), data, hashlib.sha256).hexdigest()
    return signature

def verify_captcha(image_bytes, user_answer, received_signature, secret_key=SECRET_KEY):
    new_signature = generate_signature(image_bytes, user_answer, secret_key)
    return hmac.compare_digest(new_signature, received_signature)
