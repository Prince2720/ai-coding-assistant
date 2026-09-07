import os
import tempfile
import shutil
import glob
from git import Repo, GitCommandError
from .llm_service import _call_llm

def clone_and_analyze_repo(git_url, max_files=5):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(git_url, temp_dir, depth=1, single_branch=True)

        py_files = glob.glob(f"{temp_dir}/**/*.py", recursive=True)
        if not py_files:
            return "No Python files found in this repository."

        summary = []
        count = 0
        for file_path in py_files:
            if count >= max_files:
                break
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if len(content) > 3000:
                    content = content[:3000] + "\n... (truncated)"
                prompt = f"Summarize the purpose of this file and rate its code quality (out of 10):\n\n{content}"
                file_summary = _call_llm(prompt, system="You are a code reviewer.")
                summary.append(f"**{os.path.basename(file_path)}**:\n{file_summary}\n")
                count += 1
            except Exception as e:
                summary.append(f"**{os.path.basename(file_path)}**: Error reading - {str(e)}\n")

        return f"Analyzed {count} files from {git_url}:\n\n" + "\n".join(summary)

    except GitCommandError as e:
        return f"Git error: {str(e)}"
    except Exception as e:
        return f"Error analyzing repo: {str(e)}"
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)