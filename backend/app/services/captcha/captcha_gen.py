# import random
# import string
# import io
# import hashlib
# import hmac

# from PIL import Image, ImageDraw, ImageFont, ImageFilter

# # -----------------------------
# # CONFIG PARAMETERS
# # -----------------------------
# CAPTCHA_LENGTH = 15
# CAPTCHA_WIDTH = 420
# CAPTCHA_HEIGHT = 61
# FONT_SIZE = 40
# SECRET_KEY = "supersecretkey123"

# # Adjust this path to your system font path
# FONT_PATH = "C:/Windows/Fonts/Arial.ttf"  # On Windows
# # FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # On Linux

# def generate_signature(image_bytes, answer, secret_key=SECRET_KEY):
#     data = image_bytes + answer.encode()
#     signature = hmac.new(secret_key.encode(), data, hashlib.sha256).hexdigest()
#     return signature

# def verify_captcha(image_bytes, user_answer, received_signature, secret_key=SECRET_KEY):
#     new_signature = generate_signature(image_bytes, user_answer, secret_key)
#     return hmac.compare_digest(new_signature, received_signature)
# # -----------------------------
# # Generate random CAPTCHA text
# # -----------------------------
# def generate_captcha_text(length=CAPTCHA_LENGTH):
#     chars = string.ascii_letters + string.digits
#     return ''.join(random.choices(chars, k=length))

# # -----------------------------
# # Render CAPTCHA image
# # -----------------------------
# def render_captcha_image(text):
#     image = Image.new('RGB', (CAPTCHA_WIDTH, CAPTCHA_HEIGHT), (255, 255, 255))
#     font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
#     draw = ImageDraw.Draw(image)

#     char_width = (CAPTCHA_WIDTH - 40) // CAPTCHA_LENGTH

#     for i, char in enumerate(text):
#         char_img = Image.new('RGBA', (char_width + 20, CAPTCHA_HEIGHT), (255, 255, 255, 0))
#         char_draw = ImageDraw.Draw(char_img)

#         char_color = (random.randint(0, 120), random.randint(0, 120), random.randint(0, 120))
#         char_draw.text((10, 0), char, font=font, fill=char_color)

#         rotated = char_img.rotate(random.randint(-3, 3), expand=1)

#         x = 20 + i * char_width
#         y = random.randint(10, 25)

#         image.paste(rotated, (x, y), rotated)

#     # Add curved lines
#     for _ in range(5):
#         points = [
#             (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
#             (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
#             (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
#             (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT)),
#         ]
#         draw.line(points, fill=(random.randint(120, 255), random.randint(120, 255), random.randint(120, 255), 150), width=random.randint(2, 4))

#     # Add noise dots
#     for _ in range(700):
#         xy = (random.randint(0, CAPTCHA_WIDTH), random.randint(0, CAPTCHA_HEIGHT))
#         draw.point(xy, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

#     image = image.filter(ImageFilter.GaussianBlur(0.5))

#     return image

# # -----------------------------
# # Generate HMAC signature
# # -----------------------------
# def generate_signature(image_bytes, answer, secret_key=SECRET_KEY):
#     data = image_bytes + answer.encode()
#     signature = hmac.new(secret_key.encode(), data, hashlib.sha256).hexdigest()
#     return signature

# # -----------------------------
# # Create CAPTCHA (main function)
# # -----------------------------
# def create_captcha():
#     text = generate_captcha_text()
#     image = render_captcha_image(text)

#     img_bytes_io = io.BytesIO()
#     image.save(img_bytes_io, format='PNG')
#     img_bytes = img_bytes_io.getvalue()

#     signature = generate_signature(img_bytes, text)

#     return {
#         "captcha_text": text,
#         "image": image,
#         "signature": signature,
#         "image_bytes": img_bytes,
#     }

# # -----------------------------
# # Test (Run standalone)
# # -----------------------------
# if __name__ == "__main__":
#     result = create_captcha()
#     print("CAPTCHA Text (Answer):", result["captcha_text"])
#     print("Signature:", result["signature"])

#     # Save image to disk so you can check
#     with open(r"C:\Projects\Cypher-Toolkit\backend\app\data\captcha_test.png", "wb") as f:
#         f.write(result["image_bytes"])
#     print("CAPTCHA image saved as captcha_test.png")
import os
import io
import uuid
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- Paths ----
# Current file is assumed inside backend/app/services/captcha or similar
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# Go up three levels from current file to project root, assuming backend is one folder inside root
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..",".."))

# Then point DATA_DIR outside backend, directly under project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

IMG_DIR = os.path.join(DATA_DIR, "images", "captcha")
os.makedirs(IMG_DIR, exist_ok=True) 

# In-memory store: {captcha_id: correct_text}
CAPTCHA_STORE = {}

CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"  # no easily confused chars

def _random_text(length: int = 15) -> str:
    return "".join(random.choice(CHARS) for _ in range(length))

def _noise(draw: ImageDraw.Draw, w: int, h: int):
    # dots
    for _ in range(600):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        draw.point((x, y), fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    # lines
    for _ in range(15):
        x1, y1 = random.randint(0,w-1), random.randint(0,h-1)
        x2, y2 = random.randint(0,w-1), random.randint(0,h-1)
        draw.line((x1,y1,x2,y2), fill=(random.randint(80,200), 0, random.randint(80,200)), width=random.randint(1,3))

def generate_captcha(length: int = 15):
    """
    Creates a noisy CAPTCHA image, saves it under /backend/data/images/captcha/<id>.png,
    stores the answer in-memory, and returns (id, text, abs_path).
    """
    text = _random_text(length)
    w, h = 610, 100

    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    # choose a system font if PIL can't find a ttf
    try:
        # Use a common font that usually exists; adjust path if you ship a custom font.
        font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        font = ImageFont.load_default()

    # draw text with slight per-char offset
    x = 20
    for ch in text:
        y_jitter = random.randint(-5, 10)
        draw.text((x, 30 + y_jitter), ch, font=font, fill=(random.randint(0,50), random.randint(0,50), random.randint(0,50)))
        x += 40 + random.randint(-3, 5)

    _noise(draw, w, h)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))

    captcha_id = uuid.uuid4().hex
    abs_path = os.path.join(IMG_DIR, f"{captcha_id}.png")
    img.save(abs_path, "PNG")

    CAPTCHA_STORE[captcha_id] = text
    return captcha_id, text, abs_path


def get_image_path(captcha_id: str) -> str:
    path = os.path.join(IMG_DIR, f"{captcha_id}.png")
    return path if os.path.exists(path) else ""


def verify_captcha(captcha_id: str, user_text: str) -> bool:
    correct = CAPTCHA_STORE.get(captcha_id)
    if correct is None:
        return False
    return (user_text or "").strip().lower() == correct.lower()

