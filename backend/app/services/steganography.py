# app/services/steganography.py

from PIL import Image
import numpy as np

DELIMITER = b"<<<END>>>"

def _bytes_to_bits(data: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in data)

def _bits_to_bytes(bits: str) -> bytes:
    byte_chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return bytes(int(chunk, 2) for chunk in byte_chunks)

def encode_image(input_path: str, output_path: str, message: str) -> None:
    img = Image.open(input_path)
    img = img.convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape

    msg_bytes = message.encode('utf-8') + DELIMITER
    bitstring = _bytes_to_bits(msg_bytes)
    capacity = h * w * 3
    if len(bitstring) > capacity:
        raise ValueError(f"Message too large: {len(bitstring)} bits > {capacity} capacity")

    flat = arr.reshape(-1, 3)
    bit_idx = 0
    for pixel in flat:
        for c in range(3):
            if bit_idx < len(bitstring):
                pixel[c] = (int(pixel[c]) & ~1) | int(bitstring[bit_idx])
                bit_idx += 1

    encoded = flat.reshape((h, w, 3))
    out_img = Image.fromarray(encoded.astype(np.uint8))
    out_img.save(output_path, format='PNG')

def decode_image(image_path: str) -> str:
    img = Image.open(image_path)
    img = img.convert('RGB')
    arr = np.array(img)
    flat = arr.reshape(-1, 3)

    bits = ''.join(str(int(pixel[c]) & 1) for pixel in flat for c in range(3))
    raw = _bits_to_bytes(bits)
    if DELIMITER not in raw:
        raise ValueError("Delimiter not found in decoded data.")
    msg_bytes = raw.split(DELIMITER)[0]
    return msg_bytes.decode('utf-8')
