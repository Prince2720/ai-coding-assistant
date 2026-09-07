# 🚀 AI Coding Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-black?logo=flask)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai)](https://openai.com/)
[![Monaco](https://img.shields.io/badge/Monaco-Editor-007ACC?logo=visualstudiocode)](https://microsoft.github.io/monaco-editor/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-powered coding companion** – Generate, Explain, Debug, Convert, Document, Test, Refactor, and Analyze GitHub repositories with AI.

---

## ✨ Features

- ✅ Code Generation
- 🔍 Code Explanation
- 🐞 Bug Detection
- 🔄 Code Conversion
- 📚 Documentation Generation
- 🧪 Unit Test Generation
- 🛠️ Code Refactoring
- 📊 Quality Analysis
- 📂 GitHub Repository Analysis

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Flask, OpenAI API, GitPython, pylint, radon |
| **Frontend** | HTML5, CSS3, JavaScript, Monaco Editor |
| **Deployment** | Gunicorn, Render, Railway, Vercel |

---

## 📁 Project Structure

```text
ai-coding-assistant/
├── backend/
│   ├── app.py
│   ├── core/
│   │   ├── llm_service.py
│   │   ├── analyzer.py
│   │   └── repo_utils.py
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── screenshots/
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/Prince2720/ai-coding-assistant.git
cd ai-coding-assistant
```

### Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure `.env`

```env
OPENAI_API_KEY=your_openai_api_key
```

### Run the Application

```bash
python app.py
```

Server starts at **http://localhost:5000**

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/generate` | Generate code |
| `/api/explain` | Explain code |
| `/api/debug` | Debug code |
| `/api/convert` | Convert code |
| `/api/docs` | Generate documentation |
| `/api/tests` | Generate unit tests |
| `/api/refactor` | Refactor code |
| `/api/analyze-quality` | Analyze code quality |
| `/api/analyze-github` | Analyze GitHub repository |

---

## 🚀 Deployment (Vercel)

Create a `vercel.json` file.

```json
{
  "version": 2,
  "builds": [
    { "src": "backend/app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "backend/app.py" }
  ]
}
```

Set `OPENAI_API_KEY` in Vercel Environment Variables and deploy.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Sarvesh Kumar Shukla**

M.Sc. Computational Science & Applications (Data Science)  
Banaras Hindu University (BHU)

---

<div align="center">

### ⭐ If this project helped you, give it a Star!

Built with ❤️ by **Sarvesh Kumar Shukla**

</div>
