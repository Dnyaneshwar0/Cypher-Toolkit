# encoder/encoder.py

import base64
import urllib.parse
import codecs

MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',
    'D': '-..',   'E': '.',     'F': '..-.',
    'G': '--.',   'H': '....',  'I': '..',
    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',
    'S': '...',   'T': '-',     'U': '..-',
    'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': '/'
}

MORSE_DECODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def encode_text(text: str, encoding_type: str) -> str:
    text_bytes = text.encode('utf-8')

    if encoding_type == "base16":
        return base64.b16encode(text_bytes).decode()
    elif encoding_type == "base32":
        return base64.b32encode(text_bytes).decode()
    elif encoding_type == "base64":
        return base64.b64encode(text_bytes).decode()
    elif encoding_type == "base85":
        return base64.b85encode(text_bytes).decode()
    elif encoding_type == "url":
        return urllib.parse.quote(text)
    elif encoding_type == "rot13":
        return codecs.encode(text, 'rot_13')
    elif encoding_type == "ascii-binary":
        return ' '.join(format(ord(c), '08b') for c in text)
    elif encoding_type == "morse":
        return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)
    else:
        raise ValueError(f"Unsupported encoding type: {encoding_type}")

def decode_text(encoded_text: str, encoding_type: str) -> str:
    text_bytes = encoded_text.encode('utf-8')

    if encoding_type == "base16":
        decoded = base64.b16decode(text_bytes)
    elif encoding_type == "base32":
        decoded = base64.b32decode(text_bytes)
    elif encoding_type == "base64":
        decoded = base64.b64decode(text_bytes)
    elif encoding_type == "base85":
        decoded = base64.b85decode(text_bytes)
    elif encoding_type == "url":
        return urllib.parse.unquote(encoded_text)
    elif encoding_type == "rot13":
        return codecs.encode(encoded_text, 'rot_13')
    elif encoding_type == "ascii-binary":
        chars = encoded_text.strip().split()
        return ''.join([chr(int(b, 2)) for b in chars])
    elif encoding_type == "morse":
        words = encoded_text.strip().split(' ')
        decoded_chars = []
        for symbol in words:
            if symbol == '/':
                decoded_chars.append(' ')
            else:
                decoded_chars.append(MORSE_DECODE_DICT.get(symbol, ''))
        return ''.join(decoded_chars)
    else:
        raise ValueError(f"Unsupported decoding type: {encoding_type}")

    try:
        return decoded.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decoded bytes could not be decoded to valid UTF-8 text.")
