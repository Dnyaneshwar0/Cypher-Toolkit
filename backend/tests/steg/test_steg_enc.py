from app.services import steganography

def run_encoder():
    input_img = '../data/images/steg/sample.png'
    output_img = '../data/images/steg/encoded_output.png'
    msg_file = '../data/texts/steg/long_message.txt'

    with open(msg_file, 'r', encoding='utf-8') as f:
        secret_message = f.read()

    steganography.encode_image(input_img, output_img, secret_message)
    print(f"✅ Image encoded and saved to: {output_img}")

if __name__ == '__main__':
    run_encoder()
