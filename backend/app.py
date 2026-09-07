import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

from core.llm_service import (
    generate_code, explain_code, detect_bugs,
    convert_code, generate_docs, generate_tests, refactor_code, api_key_status
)
from core.analyzer import analyze_code_quality
from core.repo_utils import clone_and_analyze_repo

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / 'frontend'
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR / 'static'),
    template_folder=str(FRONTEND_DIR / 'templates'),
)


@app.after_request
def add_cors_headers(response):
    """Add the CORS headers required by the frontend without an extra package."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ---------- API ----------
@app.route('/api/health', methods=['GET'])
def health():
    """Safe configuration check; does not disclose the API key."""
    return jsonify({'status': 'ok', 'pid': os.getpid(), **api_key_status()})


@app.route('/api/generate', methods=['POST'])
def handle_generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    language = data.get('language', 'Python')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    result = generate_code(prompt, language)
    return jsonify({'result': result})

@app.route('/api/explain', methods=['POST'])
def handle_explain():
    code = request.get_json().get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    return jsonify({'result': explain_code(code)})

@app.route('/api/debug', methods=['POST'])
def handle_debug():
    code = request.get_json().get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    return jsonify({'result': detect_bugs(code)})

@app.route('/api/convert', methods=['POST'])
def handle_convert():
    data = request.get_json()
    code = data.get('code', '')
    target = data.get('target', 'JavaScript')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    return jsonify({'result': convert_code(code, target)})

@app.route('/api/docs', methods=['POST'])
def handle_docs():
    code = request.get_json().get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    return jsonify({'result': generate_docs(code)})

@app.route('/api/tests', methods=['POST'])
def handle_tests():
    code = request.get_json().get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    return jsonify({'result': generate_tests(code)})

@app.route('/api/refactor', methods=['POST'])
def handle_refactor():
    data = request.get_json()
    code = data.get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    score, issues, complexity = analyze_code_quality(code)
    context = f"Score: {score}/100, Complexity: {complexity}, Issues: {', '.join(issues[:3])}"
    result = refactor_code(code, context)
    return jsonify({'result': result})

@app.route('/api/analyze-quality', methods=['POST'])
def handle_quality():
    code = request.get_json().get('code', '')
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    score, issues, complexity = analyze_code_quality(code)
    return jsonify({'score': score, 'complexity': complexity, 'issues': issues})

@app.route('/api/analyze-github', methods=['POST'])
def handle_github():
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'GitHub URL is required'}), 400
    result = clone_and_analyze_repo(url)
    return jsonify({'result': result})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
