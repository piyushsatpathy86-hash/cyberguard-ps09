"""Task 8: Account takeover / login-session anomaly scenario page."""

import streamlit as st

st.set_page_config(page_title="CyberGuard — Anomaly", layout="wide")
st.title("🔐 Account Takeover / Anomaly Detection")

st.write("Feed a login/session log (from the synthetic generator or pasted manually) to analyse.")

col1, col2, col3 = st.columns(3)
user_id = col1.text_input("User ID")
ip = col2.text_input("IP address")
device_id = col3.text_input("Device ID")

if st.button("Analyse", type="primary"):
    st.info("Wire this up to modules.anomaly_detector.detect_anomaly once Task 8 is built.")
    # TODO:
    # result = detect_anomaly(event_id=..., login_record={"user_id": user_id, "ip": ip, "device_id": device_id, ...})
    # result = score_risk(result)
    # result = explain(result)
    # result = recommend_action(result)
    # render result: risk_level badge, indicators, explanation, evidence, recommended_action
