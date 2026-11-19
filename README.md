# AI Mystery Quest

A cinematic, AI-assisted detective investigation game built with Flask, SQLite, and Groq. It includes Demo Mode so the core game remains playable without an API key.

## Features
- Mystery case generation with Groq; curated demo cases when unavailable
- Suspect profiles and interviews
- Evidence collection and investigation scoring
- Logic puzzle with answer validation
- Three-level hint system with score deductions
- Detective AI chat with spoiler-conscious instructions
- Final culprit submission, detective ranks, and case history
- SQLite persistence for history and active game state

## Requirements
- Python 3.10+
- Optional Groq API key (Demo Mode works without it)

## Windows / VS Code setup

Open this folder in VS Code, then in PowerShell:

```powershell
python --version
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env`. Add your Groq API key to `GROQ_API_KEY`. Keep `.env` private and never commit it.

Run:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Demo Mode
If `GROQ_API_KEY` is missing or AI calls fail, case generation falls back to built-in cases. Hints and chat also have local fallback responses. Gameplay, scoring, and history remain available.

## Notes
- The included SQLite database is created automatically on first run.
- The solution is kept in the Flask session and is not sent to the investigation page.
- For deployment, set `FLASK_DEBUG=false`, use a strong `FLASK_SECRET_KEY`, and run behind a production WSGI server.
