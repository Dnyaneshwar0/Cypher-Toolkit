import os
from flask import Flask, send_from_directory
from .app.routes.steg_routes import steg_bp   # import your blueprint
from .app.routes.captcha_routes import captcha_bp
# Base dirs
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_BUILD = os.path.join(BASE_DIR, "frontend", "build")

# Flask app
app = Flask(__name__, static_folder=FRONTEND_BUILD, static_url_path="/")

# Register steg routes with /steg prefix
app.register_blueprint(steg_bp, url_prefix="/steg")
app.register_blueprint(captcha_bp, url_prefix="/captcha")

# Example test endpoint
@app.route("/api/test")
def api_test():
    return {"message": "Hello from Flask API!"}

# Serve React frontend
@app.route("/")
def serve_react():
    return send_from_directory(app.static_folder, "index.html")

# Handle React routing
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
