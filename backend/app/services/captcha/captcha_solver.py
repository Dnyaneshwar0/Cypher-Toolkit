import os
import cv2
import numpy as np

# Optional imports – we handle absence gracefully
try:
    import easyocr
except Exception:
    easyocr = None

try:
    import pytesseract
    # If Windows needs explicit path, uncomment and update:
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pytesseract = None


def _preprocess(path: str) -> np.ndarray:
    """Robust preprocessing for noisy captchas."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")

    # upscale a bit
    h, w = img.shape[:2]
    scale = max(2, min(4, 1500 // max(h, w)))
    img = cv2.resize(img, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # try both OTSU and adaptive and pick the more balanced foreground
    _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bin_adap = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 31, 10)

    def score(b):
        ratio = (b < 128).mean()
        return -abs(ratio - 0.35)

    best = bin_otsu if score(bin_otsu) >= score(bin_adap) else bin_adap

    # connect fragments
    best = cv2.morphologyEx(best, cv2.MORPH_CLOSE, np.ones((2,2), np.uint8), iterations=1)

    # ensure black text on white
    if (best > 127).mean() < 0.5:
        best = 255 - best

    return best


def _easyocr_read(path: str) -> str:
    if easyocr is None:
        return ""
    reader = easyocr.Reader(["en"], gpu=False)
    results = reader.readtext(path, detail=1, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    parts = []
    for _bbox, txt, conf in results:
        if txt:
            parts.append(txt)
    return "".join(parts)


def _tesseract_read(bin_img: np.ndarray) -> str:
    if pytesseract is None:
        return ""
    # Tesseract expects RGB or grayscale; we have bin_img (grayscale)
    from pytesseract import image_to_string
    config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 --psm 7"
    text = image_to_string(bin_img, config=config)
    return "".join(ch for ch in text if ch.isalnum())


def solve_captcha(image_path: str) -> str:
    """
    Tries EasyOCR first on the original image path.
    Falls back to Tesseract on a preprocessed binarized image.
    """
    # 1) EasyOCR on original
    text_easy = _easyocr_read(image_path).strip()

    # 2) Tesseract on preprocessed
    try:
        bin_img = _preprocess(image_path)
    except Exception:
        bin_img = None

    text_tes = _tesseract_read(bin_img) if bin_img is not None else ""

    # prefer the longer non-empty string
    candidates = [t for t in [text_easy, text_tes] if t]
    return max(candidates, key=len) if candidates else ""
