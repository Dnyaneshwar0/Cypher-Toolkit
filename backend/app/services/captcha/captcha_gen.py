import random
import string
import io
import hashlib
import hmac

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# -----------------------------
# CONFIG PARAMETERS
# -----------------------------
CAPTCHA_LENGTH = 15
CAPTCHA_WIDTH = 420
CAPTCHA_HEIGHT = 61
FONT_SIZE = 40
SECRET_KEY = "supersecretkey123"

# Adjust this path to your system font path
FONT_PATH = "C:/Windows/Fonts/Arial.ttf"  # On Windows
# FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # On Linux

# -----------------------------
# Generate random CAPTCHA text
# -----------------------------
def generate_captcha_text(length=CAPTCHA_LENGTH):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# -----------------------------
# Render CAPTCHA image
# -----------------------------
def render_captcha_image(text):
    image = Image.new('RGB', (CAPTCHA_WIDTH, CAPTCHA_HEIGHT), (255, 255, 255))
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(image)

    char_width = (CAPTCHA_WIDTH - 40) // CAPTCHA_LENGTH

    for i, char in enumerate(text):
        char_img = Image.new('RGBA', (char_width + 20, CAPTCHA_HEIGHT), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)

        char_color = (random.randint(0, 120), random.randint(0, 120), random.randint(0, 120))
        char_draw.text((10, 0), char, font=font, fill=char_color)

        rotated = char_img.rotate(random.randint(-3, 3), expand=1)

        x = 20 + i * char_width
        y = random.randint(10, 25)

        image.paste(rotated, (x, y), rotated)

    # Add curved lines
    for _ in range(5):
        points = [
            (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
            (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
            (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
            (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
        ]
        draw.line(points, fill=(random.randint(120, 255), random.randint(120, 255), random.randint(120, 255), 150), width=random.randint(2, 4))

    # Add noise dots
    for _ in range(700):
        xy = (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT))
        draw.point(xy, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    image = image.filter(ImageFilter.GaussianBlur(0.5))

    return image

# -----------------------------
# Generate HMAC signature
# -----------------------------
def generate_signature(image_bytes, answer, secret_key=SECRET_KEY):
    data = image_bytes + answer.encode()
    signature = hmac.new(secret_key.encode(), data, hashlib.sha256).hexdigest()
    return signature

# -----------------------------
# Create CAPTCHA (main function)
# -----------------------------
def create_captcha():
    text = generate_captcha_text()
    image = render_captcha_image(text)

    img_bytes_io = io.BytesIO()
    image.save(img_bytes_io, format='PNG')
    img_bytes = img_bytes_io.getvalue()

    signature = generate_signature(img_bytes, text)

    return {
        "captcha_text": text,
        "image": image,
        "signature": signature,
        "image_bytes": img_bytes,
    }

# -----------------------------
# Test (Run standalone)
# -----------------------------
if __name__ == "__main__":
    result = create_captcha()
    print("CAPTCHA Text (Answer):", result["captcha_text"])
    print("Signature:", result["signature"])

    # Save image to disk so you can check
    with open(r"C:\Projects\Cypher-Toolkit\backend\app\data\captcha_test.png", "wb") as f:
        f.write(result["image_bytes"])
    print("CAPTCHA image saved as captcha_test.png")