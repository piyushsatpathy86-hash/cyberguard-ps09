"""Central config: paths, constants, environment-driven settings."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DB_PATH = BASE_DIR / "cyberguard.db"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "openai/gpt-oss-20b"
EXPLAIN_MIN_RISK_LEVEL = "Low"
MODEL_CACHE_DIR = BASE_DIR / ".model_cache"

# ===================================================================
# Risk scoring (backend) -- team decision: 3 stages, Low/Medium/High
# ===================================================================
RISK_LEVELS = ["Low", "Medium", "High"]

# Score is 0-100, summed from weighted indicators (see schemas/detection_result.py).
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


def get_groq_api_key() -> str:
    """
    Load the Groq API key, trying (in order):
      1. Streamlit secrets (works when actually run via `streamlit run`)
      2. Reading .streamlit/secrets.toml directly (works for standalone
         scripts/tests, e.g. `python -m modules.explainability`)
      3. The GROQ_API_KEY environment variable
    Raises if none of these have it set.
    """
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    try:
        import toml
        secrets_path = BASE_DIR.parent / ".streamlit" / "secrets.toml"
        if secrets_path.exists():
            secrets = toml.load(secrets_path)
            if "GROQ_API_KEY" in secrets:
                return secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if GROQ_API_KEY:
        return GROQ_API_KEY

    raise RuntimeError(
        "GROQ_API_KEY not found. Add it to .streamlit/secrets.toml "
        "(local) or as an environment variable (deployed)."
    )


# ===================================================================
# UI / Dashboard Settings (frontend team)
# ===================================================================
APP_NAME = "CyberGuard AI"
APP_TAGLINE = "AI-Powered Cyber Threat Detection & Response"
APP_VERSION = "1.0.0"

# --- Theme colors (dark navy) ---
BG_PRIMARY = "#0E1117"
BG_SECONDARY = "#1A1D24"
CARD_BG = "#1E222B"
TEXT_PRIMARY = "#FAFAFA"
TEXT_MUTED = "#9CA3AF"
ACCENT_BLUE = "#3B82F6"
ACCENT_CYAN = "#06B6D4"

# Risk colors
SAFE_GREEN = "#10B981"
LOW_YELLOW = "#F59E0B"
MEDIUM_ORANGE = "#F97316"
HIGH_RED = "#EF4444"
CRITICAL_PURPLE = "#8B5CF6"

RISK_COLORS = {
    "Safe": SAFE_GREEN,
    "Low": LOW_YELLOW,
    "Medium": MEDIUM_ORANGE,
    "High": HIGH_RED,
    "Critical": CRITICAL_PURPLE,
}

RISK_EMOJI = {
    "Safe": "\u2705",
    "Low": "\U0001F7E1",
    "Medium": "\U0001F7E0",
    "High": "\U0001F534",
    "Critical": "\U0001F7E3",
}

SCENARIOS = {
    "phishing": "Phishing / SMS / URL",
    "deepfake": "Deepfake / Impersonation",
    "anomaly": "Account Takeover / Anomaly",
}
