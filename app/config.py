"""
config.py
Central config for CyberGuard — paths, constants, and env loading.
Owner: Sai
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CACHE_DIR = DATA_DIR / "cache"
DB_PATH = DATA_DIR / "cyberguard.db"

for _dir in (DATA_DIR, RAW_DATA_DIR, CACHE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Risk levels — team decision: 3 stages (not the PS's 5-stage scale)
# ---------------------------------------------------------------------------
RISK_LEVELS = ["Low", "Medium", "High"]

# Score is 0-100, summed from weighted indicators (see schemas/detection_result.py).
# Adjust these thresholds once risk_scorer.py is tested against real detector output.
RISK_THRESHOLDS = {
    "Low": (0, 40),      # inclusive lower, exclusive upper
    "Medium": (40, 70),
    "High": (70, 101),   # 101 so a perfect 100 still falls in High
}


def score_to_level(score: float) -> str:
    """Map a 0-100 risk score to Low / Medium / High."""
    for level, (low, high) in RISK_THRESHOLDS.items():
        if low <= score < high:
            return level
    return "High"  # fallback for any score >= 100


# ---------------------------------------------------------------------------
# Scenarios (must match schemas/detection_result.py's `scenario` field)
# ---------------------------------------------------------------------------
SCENARIOS = ["phishing", "deepfake", "anomaly"]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
PHISHING_MODEL_NAME = "distilbert-base-uncased"  # placeholder — swap for fine-tuned model
DEEPFAKE_MODEL_NAME = "placeholder/deepfake-detector"  # fill in once deepfake owner picks one

# ---------------------------------------------------------------------------
# GenAI (Groq) — explainability.py only calls this for non-"Low" risk results
# ---------------------------------------------------------------------------
GROQ_MODEL = "llama-3.1-8b-instant"


def get_groq_api_key() -> str:
    """
    Load the Groq API key from Streamlit secrets if available, else from
    a .env file / environment variable. Raises if neither is set.
    """
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Add it to .streamlit/secrets.toml "
            "(local) or as an environment variable (deployed)."
        )
    return key
