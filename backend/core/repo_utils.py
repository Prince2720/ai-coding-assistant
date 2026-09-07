import os
import glob
import shutil
import tempfile

from core.llm_service import _call_llm


def clone_and_analyze_repo(git_url, max_files=5):
    """
    Clone and analyze a public GitHub repository.
    GitPython is imported only when needed so Vercel can start normally.
    """

    # Import GitPython lazily
    try:
        from git import Repo, GitCommandError
    except Exception:
        return (
            "⚠️ Git repository analysis is not available on this deployment "
            "because the Git executable is unavailable in the serverless environment."
        )

    temp_dir = tempfile.mkdtemp(prefix="repo_")

    try:
        if not git_url.startswith(("https://github.com/", "http://github.com/")):
            return "Please provide a valid public GitHub repository URL."

        Repo.clone_from(
            git_url,
            temp_dir,
            depth=1,
            single_branch=True
        )

        py_files = glob.glob(
            os.path.join(temp_dir, "**", "*.py"),
            recursive=True
        )

        if not py_files:
            return "No Python files found in this repository."

        summaries = []

        for file_path in py_files[:max_files]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if len(content) > 3000:
                content = content[:3000] + "\n\n... (truncated)"

            analysis = _call_llm(
                f"""
Analyze this Python file.

1. Purpose
2. Important functions/classes
3. Code quality (/10)
4. Suggestions

{content}
""",
                system="You are a senior Python reviewer."
            )

            summaries.append(
                f"## {os.path.basename(file_path)}\n\n{analysis}"
            )

        return "\n\n---\n\n".join(summaries)

    except GitCommandError as e:
        return f"Git Clone Error:\n{str(e)}"

    except Exception as e:
        return f"Repository Analysis Error:\n{str(e)}"

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)