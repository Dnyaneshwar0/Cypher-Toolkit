# from fastapi import APIRouter, Response
# from app.services.captcha_gen import create_captcha

# router = APIRouter()

# @router.get("/captcha")
# def get_captcha():
#     result = create_captcha()

#     # Save CAPTCHA text and signature for later verification
#     # (In a real system you'd store in session, DB, or Redis; here we return for demonstration)

#     headers = {
#         "X-CAPTCHA-Text": result["captcha_text"],
#         "X-CAPTCHA-Signature": result["signature"]
#     }

#     return Response(
#         content=result["image_bytes"],
#         media_type="image/png",
#         headers=headers
#     )
# backend/routes/captcha_routes.py
# backend/app/routes/captcha_routes.py
import os
from flask import Blueprint, jsonify, request, send_file
from ..services import captcha_gen, captcha_solver

captcha_bp = Blueprint("captcha", __name__, url_prefix="/captcha")

@captcha_bp.route("/health", methods=["GET"])
def health():
    return {"ok": True}

@captcha_bp.route("/generate", methods=["GET"])
def generate():
    try:
        length = int(request.args.get("len", 6))
    except Exception:
        length = 6

    cap_id, text, abs_path = captcha_gen.generate_captcha(length=length)

    return jsonify({
        "id": cap_id,
        "image_url": f"/captcha/image/{cap_id}",  # frontend will use this
        "answer_dev_only": text  # ❌ remove in production
    })

@captcha_bp.route("/image/<captcha_id>", methods=["GET"])
def image(captcha_id):
    path = captcha_gen.get_image_path(captcha_id)
    if not path:
        return jsonify({"error": "captcha not found"}), 404
    return send_file(path, mimetype="image/png", as_attachment=False)

@captcha_bp.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(silent=True) or {}
    captcha_id = data.get("id", "")
    user_text = data.get("text", "")
    ok = captcha_gen.verify_captcha(captcha_id, user_text)
    return jsonify({"ok": bool(ok)})

@captcha_bp.route("/solve", methods=["POST"])
def solve():
    """
    Accepts either JSON {id: "..."} OR a multipart file upload under 'file'.
    """
    # Case 1: posted id
    if request.is_json:
        data = request.get_json(silent=True) or {}
        captcha_id = data.get("id")
        if not captcha_id:
            return jsonify({"error": "id required"}), 400
        path = captcha_gen.get_image_path(captcha_id)
        if not path:
            return jsonify({"error": "captcha not found"}), 404
        solved = captcha_solver.solve_captcha(path)
        return jsonify({"text": solved})

    # Case 2: file upload
    if "file" in request.files:
        f = request.files["file"]
        tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads"))
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = os.path.join(tmp_dir, f"upload_{os.getpid()}_{f.filename}")
        f.save(tmp_path)
        solved = captcha_solver.solve_captcha(tmp_path)
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return jsonify({"text": solved})

    return jsonify({"error": "provide JSON {id} or a 'file' upload"}), 400
