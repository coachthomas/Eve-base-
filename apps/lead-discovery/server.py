"""Private local opportunity review. No scraping, outreach, or external API calls."""
import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

APP = Path(__file__).parent
DB = Path(os.environ.get('EVE_LEADS_DB', str(Path.home() / '.eve' / 'opportunities.sqlite3')))
STATUSES = ['new', 'reviewed', 'contacted', 'replied', 'booked', 'paid', 'dismissed']

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute('''CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY, url TEXT UNIQUE NOT NULL, excerpt TEXT NOT NULL,
        need TEXT NOT NULL, fit TEXT NOT NULL, intent TEXT NOT NULL,
        published TEXT, retrieved TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'new',
        amount REAL, notes TEXT NOT NULL DEFAULT '')''')
    return con

def validate(data):
    url = str(data.get('url', '')).strip()
    parsed = urlsplit(url)
    if parsed.scheme not in ['http', 'https'] or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Enter a public HTTP/HTTPS source link without credentials.')
    values = {key: str(data.get(key, '')).strip() for key in ['excerpt', 'need', 'fit', 'intent', 'published']}
    if not values['excerpt'] or not values['need']:
        raise ValueError('Source excerpt and expressed need are required.')
    if values['fit'] not in ['genuine-self', 'personalized', 'uncertain']:
        raise ValueError('Select a valid offer fit.')
    if not values['intent']:
        values['intent'] = 'Unknown'
    if values['published']:
        datetime.strptime(values['published'], '%Y-%m-%d')
    return {'url': url, **values}

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/api/opportunities':
            with connect() as con:
                rows = [dict(row) for row in con.execute('SELECT * FROM opportunities ORDER BY id DESC')]
            self.reply(200, rows)
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write((APP / 'index.html').read_bytes())
        else:
            self.reply(404, {'error': 'Not found'})

    def do_POST(self):
        # Local browser writes only; refuse cross-site form submissions.
        if self.headers.get('Origin') not in [None, 'http://' + self.headers.get('Host', '')]:
            return self.reply(403, {'error': 'Cross-site writes refused'})
        if self.headers.get('Content-Type') != 'application/json':
            return self.reply(415, {'error': 'JSON required'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length > 100000 or length <= 0:
                raise ValueError('Invalid request size')
            data = json.loads(self.rfile.read(length))
            with connect() as con:
                if self.path == '/api/opportunities':
                    values = validate(data)
                    values['retrieved'] = datetime.now(timezone.utc).isoformat()
                    con.execute('INSERT INTO opportunities (url,excerpt,need,fit,intent,published,retrieved) VALUES (:url,:excerpt,:need,:fit,:intent,:published,:retrieved)', values)
                elif self.path == '/api/outcome':
                    status = data.get('status')
                    if status not in STATUSES:
                        raise ValueError('Invalid outcome')
                    amount = None
                    if status == 'paid':
                        amount = float(data.get('amount', 0))
                        if not 0 < amount < 1000000:
                            raise ValueError('Enter the actual confirmed payment amount')
                        if not str(data.get('notes', '')).strip():
                            raise ValueError('Add payment confirmation and attribution notes')
                    result = con.execute('UPDATE opportunities SET status=?,amount=?,notes=? WHERE id=?', (status, amount, str(data.get('notes', '')), int(data['id'])))
                    if result.rowcount != 1:
                        raise ValueError('Opportunity not found')
                else:
                    return self.reply(404, {'error': 'Not found'})
            self.reply(200, {'saved': True})
        except sqlite3.IntegrityError:
            self.reply(409, {'error': 'That source URL is already saved'})
        except (ValueError, TypeError, KeyError) as error:
            self.reply(400, {'error': str(error)})

if __name__ == '__main__':
    connect().close()
    print('Energy Culture opportunity review: http://127.0.0.1:8765', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
