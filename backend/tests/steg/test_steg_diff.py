# backend/tests/steg/test_steg_diff.py

from PIL import Image
import numpy as np

def generate_visual_diff(original_path: str, encoded_path: str, output_path: str):
    img1 = Image.open(original_path).convert('RGB')
    img2 = Image.open(encoded_path).convert('RGB')

    if img1.size != img2.size:
        raise ValueError("Image sizes do not match!")

    arr1 = np.array(img1, dtype=np.int16)
    arr2 = np.array(img2, dtype=np.int16)

    diff = np.abs(arr1 - arr2)
    summed_diff = np.sum(diff, axis=2)

    max_val = np.max(summed_diff)
    normalized = (summed_diff / max_val * 255).astype(np.uint8) if max_val > 0 else np.zeros_like(summed_diff, dtype=np.uint8)

    diff_img = np.stack([normalized]*3, axis=2)
    Image.fromarray(diff_img).save(output_path)
    print(f"✅ Diff map saved to: {output_path}")

if __name__ == '__main__':
    original_img = '../data/images/steg/sample.png'
    encoded_img  = '../data/images/steg/encoded_output.png'
    output_img   = '../data/images/steg/diff_magnitude_map.png'

    generate_visual_diff(original_img, encoded_img, output_img)