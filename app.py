import os
import sqlite3
import threading
import time

from flask import Flask, jsonify, render_template
from monitor import DB_PATH, init_db, run_checks

app = Flask(__name__)


def fetch_rows(query, args=()):
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute(query, args).fetchall()]


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.get("/api/status")
def status():
    init_db()
    latest = fetch_rows("""SELECT c.* FROM checks c INNER JOIN
        (SELECT url, MAX(id) AS last_id FROM checks GROUP BY url) x
        ON c.id = x.last_id ORDER BY c.url""")
    history = fetch_rows("SELECT * FROM checks ORDER BY id DESC LIMIT 100")
    return jsonify({"latest": latest, "history": history})


@app.get("/health")
def health():
    return jsonify({"service": "cloudpulse", "status": "ok"})


def monitoring_loop():
    while True:
        run_checks()
        time.sleep(max(10, int(os.getenv("CHECK_INTERVAL", "60"))))


if __name__ == "__main__":
    init_db()
    thread = threading.Thread(target=monitoring_loop, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
