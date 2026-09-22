# CyberGuard — PS09

**AI-Powered Cyber Threat, Phishing & Digital Impersonation Detection and Response System**
BPUT Hackathon 2026 · Domain: Cybersecurity + Artificial Intelligence

## Overview

CyberGuard analyses emails, SMS, URLs, media, and auth/system logs across three scenarios —
phishing/social engineering, digital impersonation/deepfake, and account-takeover/anomaly
detection — and runs every detection through a shared pipeline:

```
Ingestion → Detection → Risk Scoring → Explanation → Response Recommendation → Dashboard → Action
```

Full research, architecture, and build-order rationale: `docs/problem_statement.pdf` (add the
original PS09 PDF here) and the team's architecture doc.

## Tech Stack

| Layer | Tool |
|---|---|
| App framework | Streamlit |
| Phishing NLP | DistilBERT/RoBERTa (HuggingFace) + self-collected Odia/Hindi scam corpus |
| Deepfake/audio detection | Pretrained HuggingFace model (used as-is, no fine-tuning) |
| Anomaly detection | scikit-learn IsolationForest + rules |
| Explainability | Groq API (non-Safe detections only) |
| Storage | SQLite |
| Hosting | Streamlit Community Cloud |

## Repo Structure

```
app/
├── Home.py                          # Dashboard entry point + KPI counters
├── pages/
│   ├── 1_Phishing.py
│   ├── 2_Deepfake.py
│   └── 3_Anomaly.py
├── modules/
│   ├── data_loader.py                # ingestion + local model-weight cache
│   ├── phishing_detector.py
│   ├── deepfake_detector.py
│   ├── anomaly_detector.py
│   ├── risk_scorer.py                # shared across all 3 scenarios
│   ├── explainability.py             # Groq API call
│   └── response_engine.py
├── data/
│   ├── raw/                          # public + self-collected + synthetic samples
│   │   └── README.md                 # provenance log
│   └── synthetic_login_generator.py
├── schemas/
│   └── detection_result.py           # CRITICAL: shared contract — lock this first
└── config.py
docs/
├── assumptions.md
├── performance_report.md
└── pitch_deck/
```

## Build Order

See `docs/BUILD_ORDER.md` for the full dependency-ordered task list and current owner per module.
**Task 4 (`schemas/detection_result.py`) is the unlock point** — once the shared `DetectionResult`
contract is agreed, the three detection-engine owners (phishing / deepfake / anomaly) can work
fully in parallel.

## Setup

```bash
git clone <repo-url>
cd cyberguard-ps09
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/Home.py
```

Add your Groq API key to `.streamlit/secrets.toml` (not committed — see `.gitignore`):

```toml
GROQ_API_KEY = "your-key-here"
```

## Status

Scaffold only — modules are stubbed with docstrings marking scope and owner. Fill in per
`docs/BUILD_ORDER.md`.
