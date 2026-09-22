"""
Task 5: Command Dashboard entry point.

Component F of the PS: events analysed, threats detected, category, risk
level, attack timeline, targeted users/services, recommended actions,
incident status.
"""

import streamlit as st

from app.modules.data_loader import get_connection, init_db

st.set_page_config(page_title="CyberGuard — Command Dashboard", layout="wide")

init_db()

st.title("🛡️ CyberGuard — Command Dashboard")
st.caption("AI-Powered Cyber Threat, Phishing & Digital Impersonation Detection and Response · PS09")

col1, col2, col3, col4 = st.columns(4)

with get_connection() as conn:
    total_events = conn.execute("SELECT COUNT(*) AS c FROM events").fetchone()["c"]
    total_threats = conn.execute("SELECT COUNT(*) AS c FROM detections WHERE is_threat = 1").fetchone()["c"]
    critical = conn.execute("SELECT COUNT(*) AS c FROM risk_scores WHERE level = 'Critical'").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) AS c FROM recommendations WHERE status = 'pending'").fetchone()["c"]

col1.metric("Events Analysed", total_events)
col2.metric("Threats Detected", total_threats)
col3.metric("Critical Risk", critical)
col4.metric("Pending Actions", pending)

st.divider()
st.info(
    "Use the sidebar to open a scenario page: **Phishing**, **Deepfake**, or **Anomaly**. "
    "Attack timeline and category breakdown go here once detections start flowing in."
)

# TODO: attack timeline chart, category mix chart, targeted users/services
# table, incident status board — build once at least one scenario has live
# data flowing through the pipeline (see docs/BUILD_ORDER.md Task 10).
