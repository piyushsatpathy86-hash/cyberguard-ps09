"""Central config: paths, constants, environment-driven settings."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DB_PATH = BASE_DIR / "cyberguard.db"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"
EXPLAIN_MIN_RISK_LEVEL = "Low"
MODEL_CACHE_DIR = BASE_DIR / ".model_cache"


# ===================================================================
# Groq API key loader (from team)
# Resolution order:
#   1. Streamlit secrets (works when run via `streamlit run`)
#   2. Reading .streamlit/secrets.toml directly (standalone scripts)
#   3. GROQ_API_KEY environment variable
# ===================================================================
def get_groq_key() -> str:
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

# Theme colors (dark navy)
BG_PRIMARY = "#0E1117"
BG_SECONDARY = "#1A1D24"
CARD_BG = "#1E222B"
TEXT_PRIMARY = "#FAFAFA"
TEXT_MUTED = "#9CA3AF"
ACCENT_BLUE = "#3B82F6"
ACCENT_CYAN = "#06B6D4"

# --- 3 Risk Levels only ---
RISK_COLORS = {
    "Low": "#F59E0B",       # Amber   — score 0-30
    "Medium": "#F97316",    # Orange  — score 31-60
    "High": "#EF4444",      # Red     — score 61-100
}

RISK_EMOJI = {
    "Low": "\U0001F7E1",       # 🟡
    "Medium": "\U0001F7E0",    # 🟠
    "High": "\U0001F534",      # 🔴
}

RISK_TAG = {
    "Low": "LOW",
    "Medium": "MEDIUM",
    "High": "HIGH",
}

SCENARIOS = {
    "phishing": "Phishing / SMS / URL",
    "deepfake": "Deepfake / Impersonation",
    "anomaly": "Account Takeover / Anomaly",
}