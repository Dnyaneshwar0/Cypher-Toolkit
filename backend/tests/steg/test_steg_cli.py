import os
from backend.app.services import steganography as steg
import os
print("cwd:", os.getcwd())

DATA_DIR = 'data'
IMG_DIR  = f'{DATA_DIR}/images/steg'
TXT_DIR  = f'{DATA_DIR}/texts/steg'

def clean_outputs():
    targets = [
        f'{IMG_DIR}/encoded_output.png',
        f'{IMG_DIR}/diff_map_text.png',
        f'{IMG_DIR}/diff_map_image.png',
        f'{IMG_DIR}/hidden_secret_output.png',
        f'{TXT_DIR}/decoded_message.txt'
    ]
    for path in targets:
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑️  Removed: {path}")

def encode_text_message():
    print("cwd:", os.getcwd())
    input_img = f'{IMG_DIR}/sample.png'
    output_img = f'{IMG_DIR}/encoded_output.png'
    secret_msg = f'{TXT_DIR}/long_message.txt'

    with open(secret_msg, 'r', encoding='utf-8') as f:
        message = f.read()

    steg.encode_image(input_img, output_img, message)
    print("✅ Text message encoded.")

def decode_text_message():
    output_img = f'{IMG_DIR}/encoded_output.png'
    decoded_msg = f'{TXT_DIR}/decoded_message.txt'

    message = steg.decode_image(output_img)
    with open(decoded_msg, 'w', encoding='utf-8') as f:
        f.write(message)

    print("✅ Text message decoded.")

def encode_image_in_image():
    carrier_img = f'{IMG_DIR}/sample.png'
    secret_img = f'{IMG_DIR}/secret.png'
    output_img = f'{IMG_DIR}/encoded_output.png'

    steg.encode_image_in_image(carrier_img, secret_img, output_img)
    print("✅ Secret image encoded inside carrier.")

def decode_image_from_image():
    encoded_img = f'{IMG_DIR}/encoded_output.png'
    hidden_output = f'{IMG_DIR}/hidden_secret_output.png'

    steg.decode_image_from_image(encoded_img, hidden_output)
    print("✅ Secret image decoded from encoded image.")

def generate_diff_map_image():
    original = f'{IMG_DIR}/sample.png'
    encoded = f'{IMG_DIR}/encoded_output.png'
    diff_out = f'{IMG_DIR}/diff_map_image.png'

    steg.generate_diff_map_image(original, encoded, diff_out)

def generate_diff_map_text():
    original_txt = f'{TXT_DIR}/long_message.txt'
    decoded_txt = f'{TXT_DIR}/decoded_message.txt'
    carrier_img = f'{IMG_DIR}/sample.png'
    diff_out = f'{IMG_DIR}/diff_map_text.png'

    steg.generate_diff_map_text(original_txt, decoded_txt, carrier_img, diff_out)

def main_menu():
    while True:
        print("\n=== Cypher Toolkit Steganography CLI ===")
        print("1. Encode Text Message into Image")
        print("2. Decode Text Message from Image")
        print("3. Encode Image inside Image")
        print("4. Decode Image from Image")
        print("5. Generate Image Diff Map")
        print("6. Generate Text Diff Map")
        print("7. Clean Output Files")
        print("8. Exit")

        choice = input("Select an option: ").strip()

        try:
            if choice == '1':
                encode_text_message()
            elif choice == '2':
                decode_text_message()
            elif choice == '3':
                encode_image_in_image()
            elif choice == '4':
                decode_image_from_image()
            elif choice == '5':
                generate_diff_map_image()
                print("✅ Image diff map generated.")
            elif choice == '6':
                generate_diff_map_text()
                print("✅ Text diff map generated.")
            elif choice == '7':
                clean_outputs()
            elif choice == '8':
                print("Exiting")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main_menu()
