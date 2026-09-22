"""Central config: paths, constants, environment-driven settings."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DB_PATH = BASE_DIR / "cyberguard.db"

# Groq API — read from Streamlit secrets in-app; falls back to env var for
# local/non-Streamlit runs (e.g. batch evaluation scripts).
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"  # confirm against current Groq free-tier model list

# Only call Groq for detections at or above this risk level — conserves
# free-tier rate limit (see architecture doc, Section 5.4).
EXPLAIN_MIN_RISK_LEVEL = "Low"  # anything above "Safe"

MODEL_CACHE_DIR = BASE_DIR / ".model_cache"
