from app.services import steganography

def run_decoder():
    encoded_img = '../data/images/steg/encoded_output.png'
    output_msg = '../data/texts/steg/decoded_message.txt'

    message = steganography.decode_image(encoded_img)

    with open(output_msg, 'w', encoding='utf-8') as f:
        f.write(message)

    print("🔍 Extracted message:", message)
    print(f"✅ Message also written to: {output_msg}")

if __name__ == '__main__':
    run_decoder()
