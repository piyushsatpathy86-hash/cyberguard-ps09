# app/Home.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import (
    APP_NAME, APP_TAGLINE, APP_VERSION,
    RISK_COLORS, RISK_EMOJI, SCENARIOS,
    ACCENT_BLUE, ACCENT_CYAN, BG_PRIMARY, CARD_BG, TEXT_MUTED
)

st.set_page_config(
    page_title=f"{APP_NAME} — Command Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG_PRIMARY}; }}
    section[data-testid="stSidebar"] {{
        background-color: #15181E;
        border-right: 1px solid #2A2E38;
    }}
    .kpi-card {{
        background: linear-gradient(145deg, {CARD_BG}, #232833);
        border: 1px solid #2A2E38;
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
        box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }}
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 700;
        margin: 6px 0 2px 0;
    }}
    .kpi-label {{
        font-size: 0.85rem;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .section-header {{
        font-size: 1.3rem;
        font-weight: 600;
        margin: 28px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #2A2E38;
    }}
    .threat-item {{
        background: {CARD_BG};
        border-left: 4px solid {ACCENT_BLUE};
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([0.08, 0.92])
with col_logo:
    st.markdown("# 🛡️")
with col_title:
    st.markdown(f"## {APP_NAME}")
    st.caption(f"{APP_TAGLINE} · v{APP_VERSION}")

st.divider()

kpi_data = {
    "Events Analysed": "1,247",
    "Threats Detected": "89",
    "Critical / High": "23",
    "Active Incidents": "7",
}

cols = st.columns(4)
for i, (label, value) in enumerate(kpi_data.items()):
    with cols[i]:
        color = ACCENT_BLUE if i < 2 else "#EF4444"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:{color};">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-header">📈 Attack Timeline — Last 7 Days</div>', unsafe_allow_html=True)

dates = pd.date_range(end=datetime.now(), periods=7, freq="D")
timeline_df = pd.DataFrame({
    "Date": dates,
    "Phishing": [12, 18, 9, 22, 15, 28, 19],
    "Deepfake": [3, 5, 2, 7, 4, 9, 6],
    "Anomaly": [7, 11, 8, 14, 10, 16, 13],
})

fig = px.bar(
    timeline_df, x="Date", y=["Phishing", "Deepfake", "Anomaly"],
    barmode="stack",
    color_discrete_map={
        "Phishing": ACCENT_BLUE,
        "Deepfake": "#8B5CF6",
        "Anomaly": "#06B6D4",
    },
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=TEXT_MUTED,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=10, b=0),
    height=320,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">🚨 Recent Threat Feed</div>', unsafe_allow_html=True)

demo_threats = [
    {"scenario": "Phishing", "detail": "Fake SBI SMS — 'KYC expiry, click link'", "risk": "High", "time": "2 min ago"},
    {"scenario": "Deepfake", "detail": "AI-generated voice call impersonating CEO", "risk": "Critical", "time": "14 min ago"},
    {"scenario": "Anomaly", "detail": "Login from impossible travel — Odisha → Russia", "risk": "High", "time": "32 min ago"},
    {"scenario": "Phishing", "detail": "Look-alike domain: icicibank-secure[.]com", "risk": "Medium", "time": "1 hr ago"},
    {"scenario": "Anomaly", "detail": "Password spraying — 47 failed logins, same IP", "risk": "Medium", "time": "2 hr ago"},
]

for t in demo_threats:
    emoji = RISK_EMOJI.get(t["risk"], "⚪")
    st.markdown(f"""
    <div class="threat-item" style="border-left-color:{RISK_COLORS.get(t['risk'], '#9CA3AF')};">
        <strong>{t['scenario']}</strong> · {t['detail']}<br>
        <span style="color:{RISK_COLORS.get(t['risk'], '#9CA3AF')}; font-size:0.9rem;">
            {emoji} {t['risk']}
        </span>
        <span style="color:#9CA3AF; font-size:0.8rem; float:right;">{t['time']}</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption(f"© {datetime.now().year} {APP_NAME} — BPUT Hackathon 2026")