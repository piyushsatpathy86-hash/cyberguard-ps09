# app/pages/1_Phishing.py
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import RISK_COLORS, RISK_EMOJI, ACCENT_BLUE, CARD_BG, TEXT_MUTED, BG_PRIMARY

st.set_page_config(page_title="Phishing Detection", page_icon="🎣", layout="wide")

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
    .indicator-pill {{
        display: inline-block;
        background: #2A2E38;
        color: #FAFAFA;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px 4px 4px 0;
        font-size: 0.85rem;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🎣 Phishing / SMS / URL Detection")
st.caption("Paste an SMS, email body, or URL. The AI classifier will analyse it.")

input_type = st.radio(
    "What are you checking?",
    ["SMS / WhatsApp Message", "Email Body", "URL / Link"],
    horizontal=True,
)

sample_text = st.text_area(
    "Paste the content here",
    height=140,
    placeholder="Example: Dear customer, your SBI account will be blocked. Click here to update KYC: http://sbi-kyc-update.xyz/login",
)

analyse_btn = st.button("🔍 Analyse Threat", type="primary", use_container_width=True)

if analyse_btn and sample_text.strip():
    with st.spinner("Running NLP classifier..."):
        text_lower = sample_text.lower()
        indicators = []
        confidence = 0.15

        if any(w in text_lower for w in ["urgent", "immediately", "block", "expire", "kyc"]):
            indicators.append("Urgency / pressure language")
            confidence += 0.25
        if any(w in text_lower for w in ["http://", "https://", ".xyz", ".tk", "bit.ly"]):
            indicators.append("Suspicious URL / shortener")
            confidence += 0.20
        if any(w in text_lower for w in ["otp", "password", "pin", "cvv"]):
            indicators.append("Credential request")
            confidence += 0.25
        if any(w in text_lower for w in ["sbi", "hdfc", "icici", "bank", "paytm"]):
            indicators.append("Brand impersonation (bank)")
            confidence += 0.15

        confidence = min(confidence, 0.99)
        is_threat = confidence > 0.5

        if confidence > 0.8:
            risk = "Critical"
        elif confidence > 0.6:
            risk = "High"
        elif confidence > 0.4:
            risk = "Medium"
        elif confidence > 0.2:
            risk = "Low"
        else:
            risk = "Safe"

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Threat Detected?", "YES ⚠️" if is_threat else "NO ✅")
    with col2:
        st.metric("Confidence", f"{confidence:.0%}")
    with col3:
        color = RISK_COLORS.get(risk, "#9CA3AF")
        emoji = RISK_EMOJI.get(risk, "⚪")
        st.markdown(f"**Risk Level**<br><span style='font-size:1.6rem;color:{color};'>{emoji} {risk}</span>", unsafe_allow_html=True)

    if indicators:
        st.markdown("**🔍 Indicators Found:**")
        pills = "".join([f'<span class="indicator-pill">{i}</span>' for i in indicators])
        st.markdown(pills, unsafe_allow_html=True)
    else:
        st.info("No strong indicators found. This looks safe.")

    st.markdown("**📝 Explanation:**")
    if is_threat:
        st.warning("This message shows classic phishing signs. It uses urgency and a suspicious link to trick you. **Do not click the link.**")
    else:
        st.success("No major phishing indicators detected. Still stay cautious.")

    st.markdown("**🛡️ Recommended Action:**")
    if risk in ("Critical", "High"):
        st.error("🚫 Block URL · Quarantine message · Warn user · Notify SOC")
    elif risk == "Medium":
        st.warning("⚠️ Flag for manual review · Warn user")
    elif risk == "Low":
        st.info("ℹ️ Log and monitor")
    else:
        st.success("✅ No action needed")

    st.markdown('</div>', unsafe_allow_html=True)

elif analyse_btn:
    st.warning("Please paste some text first.")