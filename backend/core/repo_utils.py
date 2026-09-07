import os
import glob
import shutil
import tempfile

from git import Repo, GitCommandError
from backend.core.llm_service import _call_llm


def clone_and_analyze_repo(git_url, max_files=5):
    """
    Clone a public GitHub repository into a temporary directory,
    summarize up to `max_files` Python files using the LLM,
    and automatically clean up temporary files.
    """

    temp_dir = tempfile.mkdtemp(prefix="repo_")

    try:
        # Validate GitHub URL
        if not git_url.startswith(("https://github.com/", "http://github.com/")):
            return "Please provide a valid public GitHub repository URL."

        # Clone repository
        Repo.clone_from(
            git_url,
            temp_dir,
            depth=1,
            single_branch=True
        )

        # Find Python files
        py_files = glob.glob(
            os.path.join(temp_dir, "**", "*.py"),
            recursive=True
        )

        if not py_files:
            return "No Python (.py) files found in this repository."

        summaries = []

        for file_path in py_files[:max_files]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()

                # Limit prompt size
                if len(content) > 3000:
                    content = content[:3000] + "\n\n... (truncated)"

                prompt = f"""
You are an expert Python code reviewer.

Analyze this Python file and provide:

1. Purpose of the file.
2. Main classes/functions.
3. Code quality score (out of 10).
4. Suggestions for improvement.

Python File:

{content}
"""

                analysis = _call_llm(
                    prompt,
                    system="You are a senior Python software architect."
                )

                summaries.append(
                    f"## 📄 {os.path.basename(file_path)}\n\n{analysis}\n"
                )

            except Exception as file_error:
                summaries.append(
                    f"## 📄 {os.path.basename(file_path)}\n\nError reading file: {str(file_error)}\n"
                )

        return (
            f"# GitHub Repository Analysis\n\n"
            f"Repository: {git_url}\n\n"
            f"Python files analyzed: {min(len(py_files), max_files)}\n\n"
            + "\n---\n".join(summaries)
        )

    except GitCommandError as git_error:
        return f"Git Clone Error:\n{str(git_error)}"

    except Exception as error:
        return f"Repository Analysis Error:\n{str(error)}"

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)