import sys
import os

# Add app/services to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "services")))

from captcha_gen import create_captcha
from captcha_solver import verify_captcha

def generate_captcha_flow():
    captcha_result = create_captcha()

    text = captcha_result["captcha_text"]
    image_bytes = captcha_result["image_bytes"]
    signature = captcha_result["signature"]

    print("\n✅ CAPTCHA Text (Answer):", text)
    print("🔒 Signature:", signature)

    # Prepare data folder path
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_folder, exist_ok=True)

    # Save image
    image_path = os.path.join(data_folder, "captcha_test.png")
    with open(image_path, "wb") as f:
        f.write(image_bytes)
    print(f"✅ CAPTCHA image saved at: {image_path}")

    # Save signature & text
    with open(os.path.join(data_folder, "captcha_signature.txt"), "w") as f:
        f.write(signature)
    with open(os.path.join(data_folder, "captcha_answer.txt"), "w") as f:
        f.write(text)
    print("✔️ Text and signature saved in data folder.\n")


def solve_captcha_flow():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    image_path = os.path.join(data_folder, "captcha_test.png")
    sig_path = os.path.join(data_folder, "captcha_signature.txt")
    ans_path = os.path.join(data_folder, "captcha_answer.txt")

    if not os.path.exists(image_path) or not os.path.exists(sig_path):
        print("\n❌ CAPTCHA not generated yet. Please generate first.\n")
        return

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    with open(sig_path, "r") as f:
        signature = f.read()

    user_text = input("\n📝 Enter CAPTCHA text to verify: ")

    if verify_captcha(image_bytes, user_text, signature):
        print("✅ Verification successful! Correct text.\n")
    else:
        print("❌ Verification failed. Incorrect text.\n")


def menu():
    while True:
        print("==== CAPTCHA MENU ====")
        print("1️⃣  Generate CAPTCHA")
        print("2️⃣  Solve CAPTCHA (verify)")
        print("3️⃣  Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            generate_captcha_flow()
        elif choice == "2":
            solve_captcha_flow()
        elif choice == "3":
            print("👋 Exiting.")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, or 3.\n")


if __name__ == "__main__":
    menu()
