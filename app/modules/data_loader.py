"""
Task 2-3: Ingestion + DB schema.

Owns: creating/connecting to the SQLite DB, writing raw ingested events,
and the table definitions every other module reads from / writes to.

Tables (see architecture doc Section 5.1):
    events          — raw ingested item before detection
    detections      — output of phishing_detector / deepfake_detector / anomaly_detector
    risk_scores     — output of risk_scorer.py
    explanations    — output of explainability.py
    recommendations — output of response_engine.py
    performance_log — feeds Deliverable #11 (accuracy/performance evaluation)
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,          -- email | sms | url | image | video | audio | auth_log | system_log
    raw_content_ref TEXT,               -- text content or path/ref to media file
    received_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS detections (
    detection_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(event_id),
    scenario TEXT NOT NULL,             -- phishing | deepfake | anomaly
    model_used TEXT,
    confidence REAL,
    is_threat INTEGER NOT NULL,         -- 0/1
    indicators TEXT                     -- JSON-encoded list[str]
);

CREATE TABLE IF NOT EXISTS risk_scores (
    score_id TEXT PRIMARY KEY,
    detection_id TEXT NOT NULL REFERENCES detections(detection_id),
    level TEXT NOT NULL,                -- Safe | Low | Medium | High | Critical
    score_value REAL,
    contributing_factors TEXT           -- JSON-encoded list[str]
);

CREATE TABLE IF NOT EXISTS explanations (
    explanation_id TEXT PRIMARY KEY,
    detection_id TEXT NOT NULL REFERENCES detections(detection_id),
    reasoning_text TEXT,
    evidence_list TEXT,                 -- JSON-encoded list[str]
    generated_at TEXT
);

CREATE TABLE IF NOT EXISTS recommendations (
    rec_id TEXT PRIMARY KEY,
    detection_id TEXT NOT NULL REFERENCES detections(detection_id),
    action TEXT,
    status TEXT DEFAULT 'pending'       -- pending | actioned | dismissed
);

CREATE TABLE IF NOT EXISTS performance_log (
    run_id TEXT PRIMARY KEY,
    scenario TEXT,
    precision REAL,
    recall REAL,
    false_positive_rate REAL,
    evaluated_at TEXT
);
"""


@contextmanager
def get_connection(db_path: Path = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: Path = DB_PATH) -> None:
    """Create tables if they don't exist. Call once on app startup."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)


def insert_event(event_id: str, source_type: str, raw_content_ref: str, received_at: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO events (event_id, source_type, raw_content_ref, received_at) "
            "VALUES (?, ?, ?, ?)",
            (event_id, source_type, raw_content_ref, received_at),
        )


if __name__ == "__main__":
    init_db()
    print(f"DB initialized at {DB_PATH}")
