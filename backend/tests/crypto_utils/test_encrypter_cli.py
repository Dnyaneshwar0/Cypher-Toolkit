import json
from backend.app.services.crypto_utils import encrypter

def print_menu():
    print("\nSelect action:")
    print("1. Generate RSA keys")
    print("2. Generate ECC keys")
    print("3. AES Encrypt text")
    print("4. AES Decrypt text")
    print("5. RSA Encrypt text")
    print("6. RSA Decrypt text")
    print("7. ECC Sign")
    print("8. ECC Verify")
    print("9. AES Encrypt file")
    print("10. AES Decrypt file")
    print("11. Create encrypted zip")
    print("12. Extract encrypted zip")
    print("13. Hybrid Encrypt text")
    print("14. Hybrid Decrypt text")
    print("15. Create self-signed cert")
    print("16. List keys")
    print("17. Delete key")
    print("18. Show fingerprint")
    print("19. Generate QR fingerprint")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == '1':
            passphrase = input("RSA passphrase: ").encode()
            encrypter.generate_rsa(passphrase)
            print("RSA keys generated.")

        elif choice == '2':
            passphrase = input("ECC passphrase: ").encode()
            encrypter.generate_ecc(passphrase)
            print("ECC keys generated.")

        elif choice == '3':
            text = input("Plaintext: ")
            password = input("Password: ")
            ct = encrypter.encrypt_aes(text, password)
            print("AES Encrypted:", ct)

        elif choice == '4':
            ct = input("AES ciphertext: ")
            password = input("Password: ")
            print("Decrypted:", encrypter.decrypt_aes(ct, password))

        elif choice == '5':
            text = input("Plaintext: ")
            ct = encrypter.encrypt_rsa(text)
            print("RSA Encrypted:", ct)

        elif choice == '6':
            ct = input("RSA ciphertext: ")
            passphrase = input("Passphrase: ").encode()
            print("Decrypted:", encrypter.decrypt_rsa(ct, passphrase))

        elif choice == '7':
            msg = input("Message to sign: ")
            passphrase = input("Passphrase: ").encode()
            sig = encrypter.sign_ecc(msg, passphrase)
            print("Signature:", sig)

        elif choice == '8':
            msg = input("Message: ")
            sig = input("Signature: ")
            valid = encrypter.verify_ecc(msg, sig)
            print("Signature valid:", valid)

        elif choice == '9':
            path = input("File path: ")
            password = input("Password: ")
            out = encrypter.encrypt_file_aes(path, password)
            print("Encrypted file:", out)

        elif choice == '10':
            path = input("Encrypted file path: ")
            password = input("Password: ")
            out = encrypter.decrypt_file_aes(path, password)
            print("Decrypted file:", out)

        elif choice == '11':
            files = input("Files (comma separated): ").split(',')
            files = [f.strip() for f in files]
            password = input("Password: ")
            out = encrypter.create_encrypted_zip(files, password)
            print("Encrypted zip:", out)

        elif choice == '12':
            enc_zip = input("Encrypted zip path: ")
            password = input("Password: ")
            encrypter.extract_encrypted_zip(enc_zip, password)
            print("Zip extracted.")

        elif choice == '13':
            text = input("Plaintext: ")
            out = encrypter.hybrid_encrypt(text)
            print("Hybrid JSON:", out)

        elif choice == '14':
            data = input("Hybrid JSON: ")
            passphrase = input("Passphrase: ").encode()
            print("Decrypted:", encrypter.hybrid_decrypt(data, passphrase))

        elif choice == '15':
            cn = input("Common Name: ")
            passphrase = input("Passphrase: ").encode()
            encrypter.create_self_signed_cert(cn, passphrase)
            print("Certificate generated.")

        elif choice == '16':
            print("Keys:", encrypter.list_keys())

        elif choice == '17':
            file = input("Filename to delete: ")
            encrypter.delete_key(file)
            print("Deleted.")

        elif choice == '18':
            file = input("File path: ")
            fp = encrypter.sha256_fingerprint(file)
            print("Fingerprint:", fp)

        elif choice == '19':
            text = input("Data for QR: ")
            encrypter.create_qr_fingerprint(text)
            print("QR generated as fingerprint_qr.png")

        elif choice == '0':
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
