# backend/tests/crypto_utils/test_encoder_cli.py

from backend.app.services.crypto_utils import encoder

def main():
    print("\n=== Multi-Format Encoder/Decoder ===\n")

    while True:
        print("Choose Action:")
        print("  [e] Encode")
        print("  [d] Decode")
        action = input("Enter your choice (e/d): ").strip().lower()
        if action in ['e', 'd']:
            break
        print("Invalid choice. Please enter 'e' or 'd'.\n")

    text = input("\nEnter the text: ").strip()

    encoding_map = {
        "1": "base16",
        "2": "base32",
        "3": "base64",
        "4": "base85",
        "5": "url",
        "6": "rot13",
        "7": "ascii-binary",
        "8": "morse"
    }

    while True:
        print("\nSelect Encoding Type:")
        print("  [1] Base16")
        print("  [2] Base32")
        print("  [3] Base64")
        print("  [4] Base85")
        print("  [5] URL Encode")
        print("  [6] ROT13")
        print("  [7] ASCII → Binary")
        print("  [8] Morse Code")

        encoding_choice = input("Enter your choice number: ").strip()
        encoding_type = encoding_map.get(encoding_choice)

        if encoding_type:
            break
        print("Invalid encoding type. Please select a valid number from the list.\n")

    try:
        if action == "e":
            result = encoder.encode_text(text, encoding_type)
            print(f"\nEncoded Result [{encoding_type}]:\n{result}")
        else:
            result = encoder.decode_text(text, encoding_type)
            print(f"\nDecoded Result [{encoding_type}]:\n{result}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
