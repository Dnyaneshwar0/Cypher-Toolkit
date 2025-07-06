import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.captcha_gen import create_captcha
from app.services.captcha_solver import verify_captcha

def test_captcha_workflow():
    # Generate CAPTCHA
    captcha_result = create_captcha()

    text = captcha_result["captcha_text"]
    image_bytes = captcha_result["image_bytes"]
    signature = captcha_result["signature"]

    print("Generated CAPTCHA Text:", text)
    print("Signature:", signature)

    # Save image to data folder
    data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "data"))
    os.makedirs(data_folder, exist_ok=True)  # Create if doesn't exist

    image_path = os.path.join(data_folder, "captcha_test.png")
    with open(image_path, "wb") as f:
        f.write(image_bytes)
    print(f"✅ CAPTCHA image saved at: {image_path}")

    # Positive case
    is_valid = verify_captcha(image_bytes, text, signature)
    assert is_valid, "Expected valid verification with correct text"
    print("✅ Correct text verification passed.")

    # Negative case
    wrong_text = text[:-1] + "X"
    is_invalid = verify_captcha(image_bytes, wrong_text, signature)
    assert not is_invalid, "Expected verification to fail with wrong text"
    print("✅ Wrong text verification correctly failed.")

if __name__ == "__main__":
    test_captcha_workflow()
    print("🎉 All tests completed successfully!")
