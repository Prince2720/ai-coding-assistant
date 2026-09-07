# 🚀 AI Coding Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-black?logo=flask)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai)](https://openai.com/)
[![Monaco](https://img.shields.io/badge/Monaco-Editor-007ACC?logo=visualstudiocode)](https://microsoft.github.io/monaco-editor/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI‑powered coding companion** – generate, explain, debug, convert, document, test, and refactor code, plus analyze GitHub repositories.

![Demo Screenshot](screenshots/demo.png)

---

## ✨ Features

- ✅ **Code Generation** – write code from natural language prompts.
- 🔍 **Code Explanation** – understand any code snippet in plain English.
- 🐞 **Bug Detection** – find and fix errors with AI‑suggested corrections.
- 🔄 **Code Conversion** – translate code between programming languages (e.g., Python → Java).
- 📚 **Documentation Generation** – auto‑generate Javadoc / docstrings.
- ✅ **Unit Test Generation** – create pytest cases for your functions.
- 🛠️ **Refactoring** – get improvement suggestions with static analysis context.
- 📊 **Quality Scoring** – measure code quality (pylint + cyclomatic complexity).
- 📂 **GitHub Repository Analysis** – clone and summarise any public repo.

---

## 🛠️ Tech Stack

| Category       | Technologies |
|----------------|--------------|
| **Backend**    | Flask, OpenAI API, pylint, radon, GitPython |
| **Frontend**   | HTML5, CSS3 (Glassmorphism), JavaScript, Monaco Editor |
| **Deployment** | Gunicorn, Render / Railway / Hugging Face Spaces / Vercel |
| **Other**      | Python‑dotenv, Flask‑CORS |

---

## 📁 Project Structure

ai-coding-assistant/
├── backend/
│ ├── app.py # Flask API entry point
│ ├── core/
│ │ ├── llm_service.py # OpenAI API wrapper with retries
│ │ ├── analyzer.py # Static code analysis (pylint, radon)
│ │ └── repo_utils.py # GitHub clone & summarisation
│ ├── .env # (not committed) API keys
│ ├── requirements.txt
│ └── Procfile # for deployment
├── frontend/
│ ├── templates/
│ │ └── index.html
│ └── static/
│ ├── style.css
│ └── script.js
├── .gitignore
├── README.md
└── LICENSE

text

---

## 🧪 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prince2720/ai-coding-assistant.git
   cd ai-coding-assistant
Set up a virtual environment (optional but recommended)

bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
Install dependencies

bash
cd backend
pip install -r requirements.txt
Add your OpenAI API key
Create a file named .env inside the backend/ folder with the following content:

text
OPENAI_API_KEY=your_secret_key_here
Run the Flask application

bash
python app.py
The server will start at http://localhost:5000.

Open your browser and enjoy the assistant!

**🎮 Usage**

Use the dropdown menu to select a feature, enter your prompt or code in the editor, and click Execute.


Feature	What it does

Generate	Write code from a description (e.g., “function to reverse a string”).
Explain	Paste any code and get a human‑friendly explanation.
Debug	Finds bugs and suggests fixes.
Convert	Converts code to another language (enter target in the field).
Docs	Generates professional docstrings/documentation.
Tests	Writes pytest test cases for your function.
Refactor	Improves code quality using static analysis context.
Quality	Shows a quality score, issues, and cyclomatic complexity.
Analyze Repo	Provide a GitHub URL – it clones and summarises Python files.

**📡 API Endpoints**

All endpoints accept POST requests with JSON payloads.

Endpoint	Payload	Response

/api/generate	{ "prompt": "...", "language": "Python" }	{ "result": "..." }

/api/explain	{ "code": "..." }	{ "result": "..." }

/api/debug	{ "code": "..." }	{ "result": "..." }

/api/convert	{ "code": "...", "target": "Java" }	{ "result": "..." }

/api/docs	{ "code": "..." }	{ "result": "..." }

/api/tests	{ "code": "..." }	{ "result": "..." }

/api/refactor	{ "code": "..." }	{ "result": "..." }

/api/analyze-quality	{ "code": "..." }	{ "score": 85, "complexity": 5, "issues": [...] }

/api/analyze-github	{ "url": "https://github.com/..." }	{ "result": "..." }


**🚀 Deployment**

You can deploy this project on Vercel, Render, Railway, Heroku, or Hugging Face Spaces.

Vercel is the recommended platform for this project – it’s fast, free for personal use, and works perfectly with Flask.

**Step 1: Create vercel.json**
In the root of your project, add a file named vercel.json with:

json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/app.py"
    }
  ],
  "env": {
    "OPENAI_API_KEY": "@openai_api_key"
  }
}

**Step 2: Set Environment Variables on Vercel**
Go to your Vercel dashboard → Settings → Environment Variables.

Add a variable named OPENAI_API_KEY/GROQ_API_KEY with your API key.

(If using the CLI, you can run vercel env add OPENAI_API_KEY/GROQ_API_KEY.)

**Step 3: Deploy**
Option A – With Git
Push your code to GitHub. On Vercel, click Add New → Project, import your repo, and Vercel will auto‑detect the config and deploy.

Option B – With Vercel CLI
Install the CLI: npm i -g vercel
Then run vercel --prod from your project root and follow the prompts.

**Step 4: Done!**
Your app will be available at a URL like https://ai-coding-assistant.vercel.app.
All API routes and the static frontend will work seamlessly.

**💡 Free tier:** Vercel’s hobby plan is generous – perfect for portfolios and demos.



After a few minutes, your app will be live!

**🤝 Contributing**

Contributions, issues, and feature requests are welcome!
Feel free to check the issues page.

**📄 License**

This project is licensed under the MIT License – see the LICENSE file for details.

**🙏 Acknowledgements**

OpenAI & DeepSeek for the powerful language models.

Monaco Editor for the rich code editing experience.

Font Awesome for the icons.

All the open‑source libraries that made this possible.

**Built with ❤️ by Prince
⭐ Star this repo if you find it useful!**

