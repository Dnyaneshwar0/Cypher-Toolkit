# backend/tests/steg/test_steg_msgdiff.py

from PIL import Image
import numpy as np

def load_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_text_diff_image(original_path: str, decoded_path: str, image_dim: tuple, output_path: str):
    original_text = load_text(original_path)
    decoded_text  = load_text(decoded_path)

    orig_bytes = original_text.encode('utf-8')
    dec_bytes  = decoded_text.encode('utf-8')

    max_len = max(len(orig_bytes), len(dec_bytes))
    orig_bytes += b' ' * (max_len - len(orig_bytes))
    dec_bytes  += b' ' * (max_len - len(dec_bytes))

    diff_array = np.abs(np.frombuffer(orig_bytes, dtype=np.uint8) - np.frombuffer(dec_bytes, dtype=np.uint8))

    if diff_array.max() > 0:
        normalized = (diff_array / diff_array.max() * 255).astype(np.uint8)
    else:
        normalized = diff_array.astype(np.uint8)

    img_width, img_height = image_dim
    total_pixels = img_width * img_height
    if len(normalized) < total_pixels:
        normalized = np.pad(normalized, (0, total_pixels - len(normalized)), constant_values=0)
    else:
        normalized = normalized[:total_pixels]

    diff_img = np.stack([normalized.reshape((img_height, img_width))]*3, axis=2)
    Image.fromarray(diff_img).save(output_path)
    print(f"✅ Text diff image saved to: {output_path}")

if __name__ == '__main__':
    original_msg_path = '../data/texts/steg/long_message.txt'
    decoded_msg_path  = '../data/texts/steg/decoded_message.txt'
    image_dimensions  = (300, 200)
    output_diff_img   = '../data/images/steg/message_diff_map.png'

    generate_text_diff_image(original_msg_path, decoded_msg_path, image_dimensions, output_diff_img)
