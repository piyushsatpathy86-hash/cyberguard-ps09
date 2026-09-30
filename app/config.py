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
# UI / Dashboard Settings
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
    "Low": "🟡",
    "Medium": "🟠",
    "High": "🔴",
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