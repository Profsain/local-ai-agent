import sqlite3
from .config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT, content TEXT)")

def add_message(session_id, role, content):
    with sqlite3.connect(DB_PATH) as c:
        c.execute("INSERT INTO messages(session_id,role,content) VALUES(?,?,?)", (session_id,role,content))

def get_messages(session_id, limit=20):
    with sqlite3.connect(DB_PATH) as c:
        rows = c.execute("SELECT role,content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?", (session_id,limit)).fetchall()
    rows.reverse()
    return [{"role": r, "content": x} for r,x in rows]
