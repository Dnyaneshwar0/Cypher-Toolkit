# app/services/steganography.py

from PIL import Image
import numpy as np
from io import BytesIO
import struct
import os

DELIMITER = b"<<<<CY-END>>>>"

def _bytes_to_bits(data: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in data)

def _bits_to_bytes(bits: str) -> bytes:
    byte_chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return bytes(int(chunk, 2) for chunk in byte_chunks)

def encode_image(input_path: str, output_path: str, message: str) -> None:
    img = Image.open(input_path).convert('RGB')
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
    Image.fromarray(encoded.astype(np.uint8)).save(output_path, format='PNG')

def decode_image(image_path: str) -> str:
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img).reshape(-1, 3)

    bits = ''.join(str(int(pixel[c]) & 1) for pixel in arr for c in range(3))
    raw = _bits_to_bytes(bits)
    if DELIMITER not in raw:
        raise ValueError("Delimiter not found in decoded data.")
    return raw.split(DELIMITER)[0].decode('utf-8')

def encode_image_in_image(carrier_path, secret_path, output_path):
    carrier = Image.open(carrier_path).convert('RGB')
    secret = Image.open(secret_path).convert('RGB')

    buf = BytesIO()
    secret.save(buf, format='PNG')
    img_bytes = buf.getvalue()

    header = struct.pack('>II', secret.width, secret.height)
    payload = header + img_bytes + DELIMITER
    bitstring = _bytes_to_bits(payload)

    arr = np.array(carrier)
    flat = arr.reshape(-1, 3)
    if len(bitstring) > flat.size:
        raise ValueError("Secret image too large to hide.")

    for i, bit in enumerate(bitstring):
        # flat[i // 3][i % 3] = (flat[i // 3][i % 3] & ~1) | int(bit)
        flat[i // 3][i % 3] = (flat[i // 3][i % 3] & 0xFE) | int(bit)


    Image.fromarray(flat.reshape(arr.shape)).save(output_path, format='PNG')

def decode_image_from_image(encoded_path, output_path):
    arr = np.array(Image.open(encoded_path).convert('RGB')).reshape(-1, 3)
    bits = ''.join(str(px[c] & 1) for px in arr for c in range(3))
    data = _bits_to_bytes(bits)

    end = data.find(DELIMITER)
    if end == -1:
        raise ValueError("Delimiter not found.")
    width, height = struct.unpack('>II', data[:8])
    img_bytes = data[8:end]

    Image.open(BytesIO(img_bytes)).resize((width, height)).save(output_path, format='PNG')

# -----------------------
# 📊 Diff Map Generators
# -----------------------

def generate_diff_map_image(original_path, encoded_path, output_path):
    img1 = Image.open(original_path).convert('RGB')
    img2 = Image.open(encoded_path).convert('RGB')

    if img1.size != img2.size:
        raise ValueError("Image sizes do not match!")

    arr1 = np.array(img1, dtype=np.int16)
    arr2 = np.array(img2, dtype=np.int16)
    diff = np.abs(arr1 - arr2)
    summed = np.sum(diff, axis=2)
    norm = (summed / np.max(summed) * 255).astype(np.uint8) if np.max(summed) > 0 else np.zeros_like(summed, dtype=np.uint8)

    diff_img = np.stack([norm]*3, axis=2)
    Image.fromarray(diff_img).save(output_path)
    print(f"✅ Image diff saved to: {output_path}")

def generate_diff_map_text(original_txt, decoded_txt, carrier_img_path, output_img_path):
    with open(original_txt, 'r', encoding='utf-8') as f1, open(decoded_txt, 'r', encoding='utf-8') as f2:
        original = f1.read().encode('utf-8')
        decoded = f2.read().encode('utf-8')

    max_len = max(len(original), len(decoded))
    original += b' ' * (max_len - len(original))
    decoded  += b' ' * (max_len - len(decoded))

    diff_array = np.abs(np.frombuffer(original, dtype=np.uint8) - np.frombuffer(decoded, dtype=np.uint8))
    img = Image.open(carrier_img_path)
    w, h = img.size
    total_pixels = w * h

    if len(diff_array) < total_pixels:
        diff_array = np.pad(diff_array, (0, total_pixels - len(diff_array)), constant_values=0)
    else:
        diff_array = diff_array[:total_pixels]

    normalized = (diff_array / diff_array.max() * 255).astype(np.uint8) if diff_array.max() > 0 else diff_array
    diff_img = np.stack([normalized.reshape((h, w))]*3, axis=2)
    Image.fromarray(diff_img).save(output_img_path)
    print(f"✅ Text diff saved to: {output_img_path}")
