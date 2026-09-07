import os
import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from backend/.env (for local development)
load_dotenv()

# -----------------------------
# Import Project Modules
# -----------------------------
from backend.core.llm_service import (
    generate_code,
    explain_code,
    detect_bugs,
    convert_code,
    generate_docs,
    generate_tests,
    refactor_code,
    api_key_status,
)

from backend.core.analyzer import analyze_code_quality
from backend.core.repo_utils import clone_and_analyze_repo

# -----------------------------
# Project Paths
# -----------------------------
BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

# -----------------------------
# Flask App
# -----------------------------
app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR / "templates"),
    static_folder=str(FRONTEND_DIR / "static"),
)

CORS(app)

# -----------------------------
# CORS Headers
# -----------------------------
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# -----------------------------
# Frontend Routes
# -----------------------------
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR / "templates", "index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR / "static", filename)


# -----------------------------
# Health Check API
# -----------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        **api_key_status()
    })


# -----------------------------
# Generate Code
# -----------------------------
@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True)

    prompt = data.get("prompt", "")
    language = data.get("language", "Python")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = generate_code(prompt, language)
    return jsonify({"result": result})


# -----------------------------
# Explain Code
# -----------------------------
@app.route("/api/explain", methods=["POST"])
def api_explain():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    return jsonify({"result": explain_code(code)})


# -----------------------------
# Debug Code
# -----------------------------
@app.route("/api/debug", methods=["POST"])
def api_debug():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    return jsonify({"result": detect_bugs(code)})


# -----------------------------
# Convert Code
# -----------------------------
@app.route("/api/convert", methods=["POST"])
def api_convert():
    data = request.get_json(force=True)

    code = data.get("code", "")
    target = data.get("target", "Java")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    return jsonify({"result": convert_code(code, target)})


# -----------------------------
# Documentation Generation
# -----------------------------
@app.route("/api/docs", methods=["POST"])
def api_docs():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    return jsonify({"result": generate_docs(code)})


# -----------------------------
# Unit Test Generation
# -----------------------------
@app.route("/api/tests", methods=["POST"])
def api_tests():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    return jsonify({"result": generate_tests(code)})


# -----------------------------
# Refactor Code
# -----------------------------
@app.route("/api/refactor", methods=["POST"])
def api_refactor():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    score, issues, complexity = analyze_code_quality(code)

    context = (
        f"Code Quality Score: {score}/100\n"
        f"Cyclomatic Complexity: {complexity}\n"
        f"Top Issues: {', '.join(issues[:5])}"
    )

    result = refactor_code(code, context)

    return jsonify({"result": result})


# -----------------------------
# Code Quality Analysis
# -----------------------------
@app.route("/api/analyze-quality", methods=["POST"])
def api_quality():
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    score, issues, complexity = analyze_code_quality(code)

    return jsonify({
        "score": score,
        "complexity": complexity,
        "issues": issues,
    })


# -----------------------------
# GitHub Repository Analysis
# -----------------------------
@app.route("/api/analyze-github", methods=["POST"])
def api_github():
    data = request.get_json(force=True)
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "GitHub URL is required"}), 400

    result = clone_and_analyze_repo(url)

    return jsonify({"result": result})


# -----------------------------
# Error Handlers
# -----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500


# -----------------------------
# Local Development
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)