"""
Task 8: Account takeover / login-session anomaly detection.

Plan (per architecture doc):
    - Rule + ML hybrid: IsolationForest (scikit-learn) on login/session logs
    - Rule layer catches obvious cases fast: impossible travel, password
      spraying (many failed logins across accounts), new device + new
      location combos
    - ML layer catches subtler multivariate anomalies

Must return a schemas.detection_result.DetectionResult with scenario="anomaly".
"""

from app.schemas.detection_result import DetectionResult


def detect_anomaly(event_id: str, login_record: dict) -> DetectionResult:
    """
    Run rule checks + IsolationForest on a login/session record and return
    a DetectionResult. login_record: {timestamp, user_id, ip, device_id, ...}.
    Owner: fill in rule logic + model inference below.
    """
    raise NotImplementedError("Task 8 owner: implement anomaly_detector.detect_anomaly")
