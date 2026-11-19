import sqlite3, json, os
DB_PATH = os.path.join(os.path.dirname(__file__), "mystery_quest.db")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY CHECK(id=1), case_json TEXT NOT NULL, state_json TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, case_title TEXT, score INTEGER,
            rank TEXT, chosen_culprit TEXT, correct INTEGER, reasoning TEXT, completed_at TEXT)""")

def save_progress(case, state):
    if not case: return
    with connect() as con:
        con.execute("INSERT OR REPLACE INTO progress(id,case_json,state_json) VALUES(1,?,?)",
                    (json.dumps(case), json.dumps(state)))

def get_progress():
    with connect() as con:
        row = con.execute("SELECT case_json,state_json FROM progress WHERE id=1").fetchone()
        return dict(row) if row else None

def save_history(title, score, rank, culprit, correct, reasoning):
    with connect() as con:
        con.execute("""INSERT INTO history(case_title,score,rank,chosen_culprit,correct,reasoning,completed_at)
        VALUES(?,?,?,?,?,?,?)""", (title, score, rank, culprit, int(correct), reasoning, __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")))

def get_history():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM history ORDER BY id DESC").fetchall()]
