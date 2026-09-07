import os
import time
from pathlib import Path
from openai import OpenAI, RateLimitError, APIError

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
# Always load the backend's own .env, regardless of the directory from which
# Python was launched.
load_dotenv(dotenv_path=ENV_FILE, override=True)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def api_key_status():
    """Return safe diagnostics without ever returning credential material."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    return {
        "env_file": str(ENV_FILE),
        "env_file_exists": ENV_FILE.is_file(),
        "provider": "Groq",
        "model": MODEL,
        "api_key_configured": bool(api_key),
        "api_key_is_placeholder": api_key == "your_groq_key_here",
        "api_key_format_looks_valid": api_key.startswith("gsk_") and len(api_key) > 20,
    }


def _get_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_key_here":
        return None
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

def _call_llm(prompt, system="You are a senior software engineer.", max_retries=2):
    client = _get_client()
    if client is None:
        return "Groq API key is not configured. Add GROQ_API_KEY to backend/.env and restart the backend."
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
                timeout=30
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            # Groq uses this exception for both short-lived rate limits and
            # exhausted project quota. Retrying an exhausted quota only makes
            # the user wait, so return the real action required immediately.
            error_code = getattr(e, "code", None)
            if error_code == "insufficient_quota" or "insufficient_quota" in str(e):
                return (
                    "Groq API quota is exhausted. Check your Groq account limits "
                    "to the project associated with this API key, then try again."
                )
            if attempt == max_retries - 1:
                return f"Groq rate limit reached: {str(e)}"
            time.sleep(1)
        except APIError as e:
            print(f"Groq API error: {e}")
            if attempt == max_retries - 1:
                return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    return "Failed after multiple retries."

def generate_code(prompt, lang="Python"):
    return _call_llm(f"Write {lang} code for: {prompt}. Return only the code, no explanations.")

def explain_code(code):
    return _call_llm(f"Explain this code in simple terms for a beginner:\n{code}")

def detect_bugs(code):
    return _call_llm(f"Find bugs and provide fixes:\n{code}")

def convert_code(code, target):
    return _call_llm(f"Convert this code to {target}:\n{code}")

def generate_docs(code):
    return _call_llm(f"Generate professional docstrings and documentation:\n{code}")

def generate_tests(code):
    return _call_llm(f"Generate pytest test cases:\n{code}")

def refactor_code(code, context=""):
    prompt = f"""
    Context from static analysis: {context}
    Original code:
    {code}
    Provide a refactored version that improves readability, performance, and maintainability. Return only the new code.
    """
    return _call_llm(prompt)
