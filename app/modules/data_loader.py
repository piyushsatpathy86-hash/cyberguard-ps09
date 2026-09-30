"""
modules/data_loader.py
-----------------------
Task 2 in the CyberGuard build order: Ingestion + cache.

Responsibilities (from PS09 architecture document, Page 6 & 7):
  1. Ingest raw items from multiple sources:
       - EMAIL / SMS / URL  (text)
       - MEDIA              (image / audio / video file paths)
       - AUTH & SYSTEM LOGS (log lines)
  2. Normalise them into a common event shape.
  3. Write each event to the SQLite `events` table.
  4. Provide a local cache directory for pretrained model weights
     (so HuggingFace downloads happen once during setup, not during demo).
"""
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths and configuration
# ---------------------------------------------------------------------------

# Use central paths from app.config (keeps DB consistent with frontend)
from app.config import DB_PATH, MODEL_CACHE_DIR

# Make sure the model cache folder exists
Path(MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)

# Allowed source types (keeps data clean and predictable)
VALID_SOURCE_TYPES = {
    "email", "sms", "url",
    "image", "audio", "video",
    "auth_log", "system_log",
}

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    # This makes rows behave like dictionaries (row["column_name"])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Create all tables if they don't exist.
    Safe to call every time the app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            event_id        TEXT PRIMARY KEY,
            source_type     TEXT NOT NULL,
            raw_content_ref TEXT NOT NULL,
            received_at     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS detections (
            detection_id TEXT PRIMARY KEY,
            event_id TEXT NOT NULL REFERENCES events(event_id),
            scenario TEXT NOT NULL,
            model_used TEXT,
            confidence REAL,
            is_threat INTEGER NOT NULL,
            indicators TEXT
        );

        CREATE TABLE IF NOT EXISTS risk_scores (
            score_id TEXT PRIMARY KEY,
            detection_id TEXT NOT NULL REFERENCES detections(detection_id),
            level TEXT NOT NULL,
            score_value REAL,
            contributing_factors TEXT
        );

        CREATE TABLE IF NOT EXISTS explanations (
            explanation_id TEXT PRIMARY KEY,
            detection_id TEXT NOT NULL REFERENCES detections(detection_id),
            reasoning_text TEXT,
            evidence_list TEXT,
            generated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            rec_id TEXT PRIMARY KEY,
            detection_id TEXT NOT NULL REFERENCES detections(detection_id),
            action TEXT,
            status TEXT DEFAULT 'pending'
        );

        CREATE TABLE IF NOT EXISTS performance_log (
            run_id TEXT PRIMARY KEY,
            scenario TEXT,
            precision REAL,
            recall REAL,
            false_positive_rate REAL,
            evaluated_at TEXT
        );
    """)
    conn.commit()
    conn.close()
    print(f"[data_loader] Database ready: {DB_PATH}")


def save_event(source_type: str, raw_content_ref: str) -> str:
    """
    Insert one event into the `events` table.

    Parameters
    ----------
    source_type : str
        One of: email, sms, url, image, audio, video, auth_log, system_log.
    raw_content_ref : str
        For text sources  -> the normalised text itself.
        For media sources -> the absolute file path.
        For logs          -> the normalised log line.

    Returns
    -------
    str : the generated event_id (UUID4).
    """
    if source_type not in VALID_SOURCE_TYPES:
        raise ValueError(
            f"Unknown source_type '{source_type}'. "
            f"Allowed: {sorted(VALID_SOURCE_TYPES)}"
        )

    event_id = str(uuid.uuid4())
    received_at = datetime.now(timezone.utc).isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO events (event_id, source_type, raw_content_ref, received_at)
        VALUES (?, ?, ?, ?)
        """,
        (event_id, source_type, raw_content_ref, received_at),
    )
    conn.commit()
    conn.close()

    print(f"[data_loader] Saved {source_type} event -> {event_id}")
    return event_id


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def _normalise_text(text: str) -> str:
    """Collapse extra whitespace and strip edges."""
    return " ".join(text.split()).strip()


def _normalise_log(log_line: str) -> str:
    """Basic log normalisation: strip and collapse spaces."""
    return " ".join(log_line.split()).strip()


# ---------------------------------------------------------------------------
# Public ingestion API
# ---------------------------------------------------------------------------

def ingest_email(text: str) -> str:
    """Ingest an email body/subject (raw text)."""
    return save_event("email", _normalise_text(text))


def ingest_sms(text: str) -> str:
    """Ingest an SMS / WhatsApp message (raw text)."""
    return save_event("sms", _normalise_text(text))


def ingest_url(url: str) -> str:
    """Ingest a URL string."""
    return save_event("url", _normalise_text(url))


def ingest_media(source_type: str, file_path: str) -> str:
    """
    Ingest an image / audio / video file.
    Stores the absolute path in raw_content_ref.
    """
    if source_type not in {"image", "audio", "video"}:
        raise ValueError("ingest_media source_type must be image, audio, or video")

    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Media file not found: {abs_path}")

    return save_event(source_type, abs_path)


def ingest_auth_log(log_line: str) -> str:
    """Ingest one authentication log line (e.g. login attempt)."""
    return save_event("auth_log", _normalise_log(log_line))


def ingest_system_log(log_line: str) -> str:
    """Ingest one system / network log line."""
    return save_event("system_log", _normalise_log(log_line))


# ---------------------------------------------------------------------------
# Read helpers (used by the detection engines)
# ---------------------------------------------------------------------------

def get_event(event_id: str):
    """Fetch a single event by id. Returns a dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_events(source_type: str = None, limit: int = 100):
    """
    Fetch recent events, newest first.
    Optionally filter by source_type.
    """
    conn = get_connection()
    cursor = conn.cursor()
    if source_type:
        cursor.execute(
            "SELECT * FROM events WHERE source_type = ? "
            "ORDER BY received_at DESC LIMIT ?",
            (source_type, limit),
        )
    else:
        cursor.execute(
            "SELECT * FROM events ORDER BY received_at DESC LIMIT ?",
            (limit,),
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_events() -> int:
    """Return the total number of events stored."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS n FROM events")
    n = cursor.fetchone()["n"]
    conn.close()
    return n


# ---------------------------------------------------------------------------
# Model weight cache (so HuggingFace downloads happen once)
# ---------------------------------------------------------------------------

def get_model_cache_dir() -> str:
    """
    Return the local directory where pretrained model weights are cached.
    Detection modules should pass this to HuggingFace's `cache_dir=`.
    Example:
        from app.modules.data_loader import get_model_cache_dir
        model = AutoModel.from_pretrained("distilbert-base-uncased",
                                          cache_dir=get_model_cache_dir())
    """
    return str(MODEL_CACHE_DIR)


# ---------------------------------------------------------------------------
# Quick self-test  (run:  python -m app.modules.data_loader)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== CyberGuard data_loader self-test ===\n")

    init_db()

    # 1. Ingest a few sample events (one per source group)
    e1 = ingest_sms("URGENT: Your bank account will be blocked. "
                    "Click http://fake-bank.xyz to verify.")
    e2 = ingest_email("Dear user, please verify your password immediately "
                      "at http://paypa1-secure-login.com")
    e3 = ingest_url("http://paypa1-secure-login.com/login")
    e4 = ingest_auth_log(
        "2026-02-14T10:23:11Z user=alice ip=203.0.113.9 status=failed"
    )
    e5 = ingest_system_log(
        "2026-02-14T10:24:00Z api=/v1/transfer status=500 bytes=0"
    )

    print("\n--- All events (newest first) ---")
    for ev in get_events(limit=10):
        print(f"{ev['received_at']}  {ev['source_type']:10s}  {ev['event_id']}")

    print(f"\nTotal events stored: {count_events()}")
    print(f"Model cache dir     : {get_model_cache_dir()}")
    print("\nSelf-test complete.")