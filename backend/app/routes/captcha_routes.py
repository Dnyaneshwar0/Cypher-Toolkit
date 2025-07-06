from fastapi import APIRouter, Response
from app.services.captcha_gen import create_captcha

router = APIRouter()

@router.get("/captcha")
def get_captcha():
    result = create_captcha()

    # Save CAPTCHA text and signature for later verification
    # (In a real system you'd store in session, DB, or Redis; here we return for demonstration)

    headers = {
        "X-CAPTCHA-Text": result["captcha_text"],
        "X-CAPTCHA-Signature": result["signature"]
    }

    return Response(
        content=result["image_bytes"],
        media_type="image/png",
        headers=headers
    )
