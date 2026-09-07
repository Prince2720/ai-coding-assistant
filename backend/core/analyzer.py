import tempfile
import os
import re
import io
from importlib import import_module

try:
    pylint_run = import_module("pylint.lint").Run
    text_reporter = import_module("pylint.reporters.text").TextReporter
except ImportError:
    pylint_run = None
    text_reporter = None

try:
    cc_visit = import_module("radon.complexity").cc_visit
except ImportError:
    cc_visit = None

def analyze_code_quality(code):
    """Returns (score: float, issues: list, avg_complexity: float)."""
    # Complexity
    try:
        if cc_visit is None:
            raise ImportError("radon is not installed")
        blocks = cc_visit(code)
        total = sum(b.complexity for b in blocks)
        avg_complexity = total / max(1, len(blocks))
    except Exception:
        avg_complexity = 0.0

    # Pylint
    pylint_score = 10.0
    issues = []
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name

        out = io.StringIO()
        if pylint_run is None or text_reporter is None:
            raise ImportError("pylint is not installed")
        reporter = text_reporter(out)
        pylint_run([temp_path], reporter=reporter, exit=False)
        output = out.getvalue()

        match = re.search(r"Your code has been rated at ([\d.]+)/10", output)
        if match:
            pylint_score = float(match.group(1))

        for line in output.split('\n'):
            if ':' in line and any(k in line.lower() for k in ['error', 'warning', 'convention']):
                issues.append(line.strip())
        issues = issues[:10]
    except Exception as e:
        issues.append(f"Pylint analysis failed: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

    combined = (pylint_score / 10) * 100
    if avg_complexity > 15:
        combined -= 20
    elif avg_complexity > 10:
        combined -= 10
    combined = max(0, min(100, combined))

    return round(combined, 1), issues, round(avg_complexity, 2)