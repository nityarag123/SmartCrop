"""SmartCrop Flask application factory."""
import os

from flask import Flask, jsonify, send_from_directory

from config import Config

_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

_PUBLIC_PAGES = {
    "": "index.html",
    "index.html": "index.html",
    "login.html": "login.html",
    "register.html": "register.html",
}


def create_app(config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    # Always return clean JSON errors — never expose stack traces to farmers.
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["DEBUG"] = False

    # Database
    from .models.db import init_store
    init_store(app.config["USE_LOCAL_FALLBACK"], app.config["LOCAL_STORE_PATH"])

    # Seed reference data (idempotent)
    from .seed import seed
    seed()

    # API blueprints
    from .routes import auth, profile, weather, crop, soil, pest, chat, calendar, schemes, dashboard
    for bp in (
        auth.bp, profile.bp, weather.bp, crop.bp, soil.bp, pest.bp,
        chat.bp, calendar.bp, schemes.bp, dashboard.bp,
    ):
        app.register_blueprint(bp, url_prefix="/api")

    # Security headers
    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if request_is_api():
            response.headers["Cache-Control"] = "no-store"
        return response

    # JSON errors
    @app.errorhandler(404)
    def not_found(_error):
        if request_is_api():
            return jsonify({"error": "Not found"}), 404
        return send_from_directory(_FRONTEND_DIR, "404.html") if os.path.exists(os.path.join(_FRONTEND_DIR, "404.html")) else ("Not found", 404)

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "File too large (max 10 MB)."}), 413

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unhandled error: %s", error)
        if request_is_api():
            return jsonify({"error": "An unexpected error occurred. Please try again."}), 500
        return "An unexpected error occurred.", 500

    # Frontend static pages
    @app.route("/")
    def frontend_index():
        return send_from_directory(_FRONTEND_DIR, "index.html")

    @app.route("/<path:path>")
    def frontend_pages(path):
        full = os.path.join(_FRONTEND_DIR, path)
        if os.path.isfile(full):
            return send_from_directory(_FRONTEND_DIR, path)
        if os.path.isfile(full + ".html"):
            return send_from_directory(_FRONTEND_DIR, path + ".html")
        return send_from_directory(_FRONTEND_DIR, "404.html") if os.path.exists(os.path.join(_FRONTEND_DIR, "404.html")) else ("Not found", 404)

    # Expose storage status for the frontend footer/debug
    from .models.db import get_storage_label
    app.jinja_env.globals["storage_label"] = get_storage_label

    return app


def request_is_api():
    from flask import request
    return request.path.startswith("/api")
