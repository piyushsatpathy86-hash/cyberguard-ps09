# Build Order

Numbers = dependency order. Task 4 is the unlock point — once
`schemas/detection_result.py` is agreed, Tasks 6–8 run fully in parallel.

| Task | What | File(s) | Owner |
|---|---|---|---|
| 0–1 | Read PS, set up config/env, gather datasets | `app/config.py`, `requirements.txt`, `app/data/raw/README.md` | Whole team |
| 2–3 | Data ingestion + DB schema | `app/modules/data_loader.py` | |
| 4 | **Lock `DetectionResult` schema** | `app/schemas/detection_result.py` | |
| 5 | Home.py entry point + KPI shell | `app/Home.py` | |
| 6 | Phishing detector | `app/modules/phishing_detector.py`, `app/pages/1_Phishing.py` | |
| 7 | Deepfake detector | `app/modules/deepfake_detector.py`, `app/pages/2_Deepfake.py` | |
| 8 | Anomaly detector | `app/modules/anomaly_detector.py`, `app/pages/3_Anomaly.py` | |
| 9 | Risk scorer | `app/modules/risk_scorer.py` | |
| 10 | Explainability + response engine + dashboard integration | `app/modules/explainability.py`, `app/modules/response_engine.py` | |
| 11–13 | Performance evaluation, assumptions doc, README, pitch deck | `docs/performance_report.md`, `docs/assumptions.md`, `docs/pitch_deck/` | |

Fill in the Owner column and assign in your first team sync.
