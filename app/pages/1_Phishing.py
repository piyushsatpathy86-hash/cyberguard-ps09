"""Task 6: Phishing / SMS / URL scenario page."""

import streamlit as st

st.set_page_config(page_title="CyberGuard — Phishing", layout="wide")
st.title("📧 Phishing / SMS / URL Detection")

text_input = st.text_area("Paste an email, SMS, or URL to analyse:")

if st.button("Analyse", type="primary"):
    if not text_input.strip():
        st.warning("Paste some content first.")
    else:
        st.info("Wire this up to modules.phishing_detector.detect_phishing once Task 6 is built.")
        # TODO:
        # result = detect_phishing(event_id=..., text=text_input)
        # result = score_risk(result)
        # result = explain(result)
        # result = recommend_action(result)
        # render result: risk_level badge, indicators, explanation, evidence, recommended_action
