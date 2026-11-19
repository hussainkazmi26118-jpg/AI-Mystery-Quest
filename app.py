import os, json, random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from game_data import DEMO_CASES
from database import init_db, save_progress, get_progress, save_history, get_history
from ai_service import GroqService

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret")
app.config["JSON_SORT_KEYS"] = False
init_db()
ai = GroqService()

def current_case():
    return session.get("case")

def safe_case(case):
    return {k:v for k,v in case.items() if k not in ("solution", "answer_key")}

@app.route("/")
def index():
    return render_template("index.html", demo=not ai.available)

@app.route("/dashboard")
def dashboard():
    history = get_history()
    progress = get_progress()
    return render_template("dashboard.html", history=history[:5], progress=progress, demo=not ai.available)

@app.route("/new-case", methods=["GET", "POST"])
def new_case():
    if request.method == "POST":
        difficulty = request.form.get("difficulty", "Standard")
        theme = request.form.get("theme", "mystery")
        case = ai.generate_case(difficulty, theme)
        if not case:
            case = random.choice(DEMO_CASES).copy()
        session["case"] = case
        session["state"] = {"evidence": [], "interviewed": [], "solved": [], "hints": 0, "score": 100, "messages": [], "stage": "Crime Scene"}
        save_progress(session.get("case"), session.get("state"))
        return redirect(url_for("investigation"))
    return render_template("new_case.html", demo=not ai.available)

@app.route("/investigation")
def investigation():
    case = current_case()
    if not case:
        flash("Start a new investigation first.", "warning")
        return redirect(url_for("new_case"))
    state = session.get("state", {})
    return render_template("investigation.html", case=safe_case(case), state=state, demo=not ai.available)

@app.route("/suspect/<int:index>", methods=["GET", "POST"])
def suspect(index):
    case = current_case()
    if not case or index >= len(case["suspects"]):
        return redirect(url_for("investigation"))
    s = case["suspects"][index]
    state = session.get("state", {})
    if request.method == "POST":
        state.setdefault("interviewed", [])
        if index not in state["interviewed"]:
            state["interviewed"].append(index)
            state["score"] = max(0, state.get("score", 100) + 5)
        session["state"] = state
        save_progress(case, state)
        flash("Interview recorded. +5 investigation points.", "success")
        return redirect(url_for("investigation"))
    return render_template("suspect.html", suspect=s, index=index, demo=not ai.available)

@app.route("/evidence/<int:index>", methods=["POST"])
def collect_evidence(index):
    case = current_case()
    state = session.get("state", {})
    if case and 0 <= index < len(case["evidence"]):
        if index not in state.setdefault("evidence", []):
            state["evidence"].append(index)
            state["score"] = state.get("score", 100) + 10
            session["state"] = state
            save_progress(case, state)
            flash("Evidence added to your case file. +10 points.", "success")
    return redirect(url_for("investigation"))

@app.route("/puzzle", methods=["GET", "POST"])
def puzzle():
    case = current_case()
    if not case:
        return redirect(url_for("new_case"))
    state = session.get("state", {})
    result = None
    if request.method == "POST":
        answer = request.form.get("answer", "").strip().lower()
        correct = case.get("puzzle", {}).get("answer", "").strip().lower()
        if answer and answer == correct:
            if "main" not in state.setdefault("solved", []):
                state["solved"].append("main")
                state["score"] = state.get("score", 100) + 25
            result = ("Correct! The puzzle is solved. +25 points.", "success")
        else:
            result = ("Not quite. Re-examine the clues and try again.", "danger")
        session["state"] = state
        save_progress(case, state)
    return render_template("puzzle.html", puzzle=case["puzzle"], result=result)

@app.route("/hint", methods=["POST"])
def hint():
    case = current_case()
    if not case:
        return jsonify({"hint": "Start an investigation first."}), 400
    state = session.get("state", {})
    level = min(3, int(request.json.get("level", 1)))
    hint_text = ai.get_hint(case, level)
    if not hint_text:
        hint_text = case["hints"][level-1]
    state["hints"] = state.get("hints", 0) + 1
    state["score"] = max(0, state.get("score", 100) - (5 * level))
    session["state"] = state
    save_progress(case, state)
    return jsonify({"hint": hint_text, "score": state["score"]})

@app.route("/chat", methods=["GET", "POST"])
def chat():
    case = current_case()
    if not case:
        return redirect(url_for("new_case"))
    state = session.get("state", {})
    answer = None
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer = ai.chat(case, question, state.get("messages", []))
            if not answer:
                answer = "Review the evidence carefully. I can help you reason through known facts, but I won't reveal the culprit outright. Which detail seems inconsistent?"
            messages = state.setdefault("messages", [])
            messages.extend([{"role":"user","content":question},{"role":"assistant","content":answer}])
            state["messages"] = messages[-12:]
            session["state"] = state
            save_progress(case, state)
    return render_template("chat.html", messages=state.get("messages", []), answer=answer)

@app.route("/final-report", methods=["GET", "POST"])
def final_report():
    case = current_case()
    if not case:
        return redirect(url_for("new_case"))
    state = session.get("state", {})
    outcome = None
    if request.method == "POST":
        chosen = request.form.get("culprit", "")
        reasoning = request.form.get("reasoning", "")
        correct = chosen == case["solution"]["culprit"]
        score = state.get("score", 100) + (50 if correct else 0)
        rank = ("Master Detective" if score >= 180 else "Senior Detective" if score >= 145 else "Skilled Detective" if score >= 110 else "Junior Investigator" if score >= 75 else "Rookie Detective")
        outcome = {"correct": correct, "culprit": case["solution"]["culprit"], "explanation": case["solution"]["explanation"], "score": score, "rank": rank}
        save_history(case["title"], score, rank, chosen, correct, reasoning)
        session.pop("case", None)
        session.pop("state", None)
    return render_template("final_report.html", case=safe_case(case), outcome=outcome)

@app.route("/history")
def history():
    return render_template("history.html", history=get_history())

@app.route("/api/status")
def status():
    return jsonify({"ai_available": ai.available, "mode": "AI" if ai.available else "Demo"})

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
