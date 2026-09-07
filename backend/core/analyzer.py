import io
import os
import re
import tempfile
from importlib import import_module

# -----------------------------
# Optional Imports
# -----------------------------
try:
    pylint_run = import_module("pylint.lint").Run
    text_reporter = import_module("pylint.reporters.text").TextReporter
except Exception:
    pylint_run = None
    text_reporter = None

try:
    cc_visit = import_module("radon.complexity").cc_visit
except Exception:
    cc_visit = None


# -----------------------------
# Code Quality Analyzer
# -----------------------------
def analyze_code_quality(code: str):
    """
    Analyze Python code quality using Radon and Pylint.

    Returns:
        score (float): Overall quality score out of 100.
        issues (list): List of pylint issues.
        complexity (float): Average cyclomatic complexity.
    """

    issues = []
    pylint_score = 10.0
    avg_complexity = 0.0

    # -----------------------------
    # Cyclomatic Complexity
    # -----------------------------
    try:
        if cc_visit:
            blocks = cc_visit(code)

            if blocks:
                total_complexity = sum(block.complexity for block in blocks)
                avg_complexity = total_complexity / len(blocks)

    except Exception as e:
        issues.append(f"Radon analysis failed: {str(e)}")

    # -----------------------------
    # Pylint Analysis
    # -----------------------------
    temp_file = None

    try:
        if pylint_run is None or text_reporter is None:
            raise Exception("Pylint is not installed.")

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as file:
            file.write(code)
            temp_file = file.name

        pylint_output = io.StringIO()
        reporter = text_reporter(pylint_output)

        pylint_run(
            [temp_file],
            reporter=reporter,
            exit=False,
        )

        output = pylint_output.getvalue()

        score_match = re.search(
            r"rated at ([\d\.-]+)/10",
            output,
            re.IGNORECASE,
        )

        if score_match:
            pylint_score = float(score_match.group(1))

        for line in output.splitlines():
            lower = line.lower()

            if any(
                keyword in lower
                for keyword in [
                    "error",
                    "warning",
                    "convention",
                    "refactor",
                    "unused",
                ]
            ):
                issues.append(line.strip())

        issues = issues[:10]

    except Exception as e:
        issues.append(f"Pylint analysis failed: {str(e)}")

    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

    # -----------------------------
    # Combined Quality Score
    # -----------------------------
    score = max(0, min(100, pylint_score * 10))

    if avg_complexity > 15:
        score -= 20
    elif avg_complexity > 10:
        score -= 10
    elif avg_complexity > 5:
        score -= 5

    score = max(0, min(100, score))

    return round(score, 1), issues, round(avg_complexity, 2)