# app/pages/3_Anomaly.py
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import RISK_COLORS, RISK_EMOJI, ACCENT_CYAN, CARD_BG, TEXT_MUTED, BG_PRIMARY

st.set_page_config(page_title="Anomaly Detection", page_icon="🔍", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG_PRIMARY}; }}
    .result-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 24px;
        border: 1px solid #2A2E38;
        margin-top: 16px;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🔍 Account Takeover / Login Anomaly Detection")
st.caption("Enter login/session details. The system will check for suspicious patterns.")

with st.form("anomaly_form"):
    col1, col2 = st.columns(2)
    with col1:
        user = st.text_input("Username / Email", placeholder="e.g. rahul@company.com")
        ip_address = st.text_input("Login IP Address", placeholder="e.g. 192.168.1.45")
        location = st.text_input("Location (City, Country)", placeholder="e.g. Bhubaneswar, India")
    with col2:
        device = st.text_input("Device ID / User-Agent", placeholder="e.g. Chrome on Windows")
        failed_attempts = st.number_input("Failed login attempts (last hour)", min_value=0, max_value=50, value=0)
        time_of_day = st.time_input("Login time", value=datetime.now().time())

    submitted = st.form_submit_button("🔍 Analyse Login", type="primary", use_container_width=True)

if submitted and user:
    with st.spinner("Running IsolationForest + rules..."):
        score = 0.0
        indicators = []

        if failed_attempts > 10:
            score += 0.35
            indicators.append(f"High failed attempts ({failed_attempts}) — password spraying")
        elif failed_attempts > 5:
            score += 0.15
            indicators.append(f"Elevated failed attempts ({failed_attempts})")

        if "russia" in location.lower() or "unknown" in location.lower():
            score += 0.30
            indicators.append("Unusual / high-risk location")

        hour = time_of_day.hour
        if hour < 6 or hour > 23:
            score += 0.15
            indicators.append("Login outside normal working hours")

        if "unknown" in device.lower() or not device.strip():
            score += 0.15
            indicators.append("Unrecognised device")

        score = min(score, 0.99)
        is_threat = score > 0.4

        if score > 0.8:
            risk = "Critical"
        elif score > 0.6:
            risk = "High"
        elif score > 0.4:
            risk = "Medium"
        elif score > 0.2:
            risk = "Low"
        else:
            risk = "Safe"

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Anomaly Detected?", "YES ⚠️" if is_threat else "NO ✅")
    with col2:
        st.metric("Anomaly Score", f"{score:.0%}")
    with col3:
        color = RISK_COLORS.get(risk, "#9CA3AF")
        emoji = RISK_EMOJI.get(risk, "⚪")
        st.markdown(f"**Risk Level**<br><span style='font-size:1.6rem;color:{color};'>{emoji} {risk}</span>", unsafe_allow_html=True)

    if indicators:
        st.markdown("**🔍 Anomaly Indicators:**")
        for ind in indicators:
            st.markdown(f"- {ind}")
    else:
        st.success("No anomalous patterns found in this login.")

    st.markdown("**📝 Explanation:**")
    if is_threat:
        st.warning("This login shows patterns consistent with account takeover.")
    else:
        st.success("Login looks normal based on the provided details.")

    st.markdown("**🛡️ Recommended Action:**")
    if risk in ("Critical", "High"):
        st.error("🚫 Force re-authentication · Revoke active sessions · Notify user & SOC")
    elif risk == "Medium":
        st.warning("⚠️ Require re-auth · Flag for manual review")
    elif risk == "Low":
        st.info("ℹ️ Monitor this account closely")
    else:
        st.success("✅ No action needed")

    st.markdown('</div>', unsafe_allow_html=True)

elif submitted:
    st.warning("Please enter at least a username.")