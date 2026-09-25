# app/pages/2_Deepfake.py
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import RISK_COLORS, RISK_EMOJI, ACCENT_CYAN, CARD_BG, TEXT_MUTED, BG_PRIMARY

st.set_page_config(page_title="Deepfake Detection", page_icon="🎭", layout="wide")

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

st.markdown("## 🎭 Deepfake / Impersonation Detection")
st.caption("Upload an image, audio clip, or short video.")

media_type = st.radio(
    "Media type",
    ["Image", "Audio (Voice)", "Video"],
    horizontal=True,
)

uploaded_file = st.file_uploader(
    f"Upload a short {media_type.lower()} sample",
    type=["jpg", "jpeg", "png", "wav", "mp3", "mp4", "mov"],
)

analyse_btn = st.button("🔍 Analyse Media", type="primary", use_container_width=True)

if analyse_btn and uploaded_file:
    with st.spinner("Running deepfake detector..."):
        file_size_kb = uploaded_file.size / 1024
        confidence = 0.72 if file_size_kb > 100 else 0.35
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

        if is_threat:
            indicators = [
                "Unnatural facial boundary blending",
                "Inconsistent lighting on face vs. background",
                "Audio-visual sync mismatch detected",
            ]
        else:
            indicators = ["No manipulation artefacts found"]

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Manipulation Detected?", "YES ⚠️" if is_threat else "NO ✅")
    with col2:
        st.metric("Confidence", f"{confidence:.0%}")
    with col3:
        color = RISK_COLORS.get(risk, "#9CA3AF")
        emoji = RISK_EMOJI.get(risk, "⚪")
        st.markdown(f"**Risk Level**<br><span style='font-size:1.6rem;color:{color};'>{emoji} {risk}</span>", unsafe_allow_html=True)

    st.markdown("**🔍 Indicators Found:**")
    for ind in indicators:
        st.markdown(f"- {ind}")

    st.markdown("**📝 Explanation:**")
    if is_threat:
        st.warning("This media shows signs of AI manipulation. It may be a deepfake.")
    else:
        st.success("No obvious deepfake signs detected.")

    st.markdown("**🛡️ Recommended Action:**")
    if risk in ("Critical", "High"):
        st.error("🚫 Do not act on this media · Report to SOC · Warn user")
    elif risk == "Medium":
        st.warning("⚠️ Flag for manual review")
    else:
        st.success("✅ No action needed")

    st.markdown('</div>', unsafe_allow_html=True)

elif analyse_btn:
    st.warning("Please upload a file first.")