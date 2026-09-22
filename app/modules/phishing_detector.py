"""
Task 6: Phishing / SMS / URL detection.

Plan (per architecture doc):
    - Pretrained/fine-tuned NLP classifier (DistilBERT/RoBERTa)
    - Supplement with self-collected Odia/Hindi scam SMS dataset for
      local-language differentiation
    - Indicators to surface: sender domain mismatch, urgency language,
      look-alike domains, suspicious redirect targets, OTP/credential
      requests

Must return a schemas.detection_result.DetectionResult with scenario="phishing".
"""

from app.schemas.detection_result import DetectionResult


def detect_phishing(event_id: str, text: str) -> DetectionResult:
    """
    Run the phishing classifier on `text` (email/SMS/URL body) and return
    a DetectionResult. Owner: fill in model loading + inference below.
    """
    raise NotImplementedError("Task 6 owner: implement phishing_detector.detect_phishing")
