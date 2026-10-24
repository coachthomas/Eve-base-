"""Eve 0.1 local-only prototype. Python 3.11+, stdlib only.
Requires Ollama running separately with an installed chat model.
Never expose this server to the internet; no authentication is implemented.
"""
import json
import os
import sqlite3
import urllib.request
import urllib.error
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = Path(__file__).resolve().parent
DB = Path(os.environ.get("EVE_DB_PATH", str(APP / "private" / "eve.sqlite3")))
CONSTITUTION = ROOT / "docs" / "constitution.md"
MODEL = os.environ.get("EVE_MODEL", "granite4:micro")
OLLAMA_URL = os.environ.get("EVE_OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
HOST = "127.0.0.1"
PORT = int(os.environ.get("EVE_PORT", "8765"))
MAX_MESSAGE = 4000

def db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, role TEXT NOT NULL CHECK(role IN ('user','assistant')), content TEXT NOT NULL, created_at TEXT NOT NULL)")
    conn.commit()
    return conn

def history():
    with db() as conn:
        return [{"role": r, "content": c} for r, c in conn.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 60").fetchall()[::-1]]

def save(role, content):
    with db() as conn:
        conn.execute("INSERT INTO messages(role,content,created_at) VALUES (?,?,?)", (role, content, datetime.now(timezone.utc).isoformat()))
        conn.commit()

def reply(text):
    system = ("You are Eve, an Energy Culture AI prototype. Follow the constitution below. "
              "Tell the truth; do not claim an action occurred unless verified. "
              "Do not manipulate, pigeonhole, or invent facts. "
              "Conversation history is stored locally, but durable fact learning and independent action are not yet implemented.\n\n"
              + CONSTITUTION.read_text(encoding="utf-8"))
    messages = [{"role": "system", "content": system}] + history() + [{"role": "user", "content": text}]
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": False}).encode()
    request = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as res:
        result = json.load(res)
    answer = result.get("message", {}).get("content", "")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Model returned an empty response")
    return answer

class Handler(BaseHTTPRequestHandler):
    def respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            body = (APP / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/history":
            self.respond(200, {"messages": history(), "model": MODEL})
        elif self.path == "/api/health":
            self.respond(200, {"server": "running", "model_configured": MODEL, "model_verified": False})
        else:
            self.respond(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/chat":
            return self.respond(404, {"error": "Not found"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n < 1 or n > 12000:
                return self.respond(413, {"error": "Invalid request length"})
            obj = json.loads(self.rfile.read(n))
            prompt = obj.get("message")
            if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > MAX_MESSAGE:
                return self.respond(400, {"error": "Enter a message under 4000 characters"})
            # Only record a successful user/assistant exchange.
            answer = reply(prompt.strip())
            save("user", prompt.strip())
            save("assistant", answer)
            self.respond(200, {"answer": answer})
        except (urllib.error.URLError, TimeoutError) as exc:
            self.respond(503, {"error": "Local model unavailable; check Ollama and EVE_MODEL. No message saved."})
        except Exception:
            self.respond(500, {"error": "Chat failed; no completed exchange recorded. See server logs."})

if __name__ == "__main__":
    print(f"Eve local prototype at http://{HOST}:{PORT}; model={MODEL}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
