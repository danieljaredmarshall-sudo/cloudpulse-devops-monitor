import os
import sqlite3
import time
from datetime import datetime, timezone

import requests

DB_PATH = os.getenv("CLOUDPULSE_DB", "cloudpulse.db")
URLS = [url.strip() for url in os.getenv("MONITOR_URLS", "https://example.com,https://www.python.org").split(",") if url.strip()]


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            status_code INTEGER,
            response_ms REAL,
            healthy INTEGER NOT NULL,
            error TEXT
        )""")


def check_url(url):
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "CloudPulse/1.0"})
        elapsed = round((time.perf_counter() - start) * 1000, 1)
        return (url, datetime.now(timezone.utc).isoformat(), response.status_code,
                elapsed, int(200 <= response.status_code < 400), None)
    except requests.RequestException as exc:
        elapsed = round((time.perf_counter() - start) * 1000, 1)
        return (url, datetime.now(timezone.utc).isoformat(), None, elapsed, 0, str(exc))


def run_checks():
    init_db()
    results = [check_url(url) for url in URLS]
    with sqlite3.connect(DB_PATH) as db:
        db.executemany("""INSERT INTO checks
            (url, checked_at, status_code, response_ms, healthy, error)
            VALUES (?, ?, ?, ?, ?, ?)""", results)
    return results


if __name__ == "__main__":
    for url, checked_at, status, ms, healthy, error in run_checks():
        print(f"{'HEALTHY' if healthy else 'ALERT'} | {url} | HTTP {status or '-'} | {ms}ms | {error or ''}")
