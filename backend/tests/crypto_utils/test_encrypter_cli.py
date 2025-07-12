import json
import base64
from backend.app.services.crypto_utils import encrypter

def print_menu():
    print("\nChoose action:")
    print("1. Generate RSA keys")
    print("2. Generate ECC keys")
    print("3. AES Encrypt text")
    print("4. AES Decrypt text")
    print("5. RSA Encrypt text")
    print("6. RSA Decrypt text")
    print("7. Show key fingerprint")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter choice number: ").strip()

        if choice == '1':
            passphrase = input("Enter passphrase for RSA private key: ").encode()
            encrypter.generate_rsa(passphrase)
            print("RSA keys generated and saved.")

        elif choice == '2':
            passphrase = input("Enter passphrase for ECC private key: ").encode()
            encrypter.generate_ecc(passphrase)
            print("ECC keys generated and saved.")

        elif choice == '3':
            plaintext = input("Enter plaintext to AES encrypt: ")
            password = input("Enter password for AES key derivation: ")
            ciphertext = encrypter.encrypt_aes(plaintext, password)
            print("Encrypted AES ciphertext (base64):")
            print(ciphertext)

        elif choice == '4':
            ciphertext = input("Enter base64 AES ciphertext to decrypt: ")
            password = input("Enter password for AES key derivation: ")
            try:
                plaintext = encrypter.decrypt_aes(ciphertext, password)
                print("Decrypted AES plaintext:")
                print(plaintext)
            except Exception as e:
                print(f"Decryption failed: {e}")

        elif choice == '5':
            plaintext = input("Enter plaintext to RSA encrypt: ")
            try:
                ciphertext = encrypter.encrypt_rsa(plaintext)
                print("RSA Encrypted ciphertext (base64):")
                print(ciphertext)
            except Exception as e:
                print(f"RSA encryption failed: {e}")

        elif choice == '6':
            ciphertext = input("Enter base64 RSA ciphertext to decrypt: ")
            passphrase = input("Enter passphrase for RSA private key: ").encode()
            try:
                plaintext = encrypter.decrypt_rsa(ciphertext, passphrase)
                print("RSA Decrypted plaintext:")
                print(plaintext)
            except Exception as e:
                print(f"RSA decryption failed: {e}")

        elif choice == '7':
            key_path = input("Enter path to key file: ").strip()
            try:
                fingerprint = encrypter.sha256_fingerprint(key_path)
                print(f"SHA256 Fingerprint:\n{fingerprint}")
            except Exception as e:
                print(f"Failed to get fingerprint: {e}")

        elif choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
