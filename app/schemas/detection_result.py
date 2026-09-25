"""
schemas/detection_result.py
The shared contract every detection engine (phishing_detector.py,
deepfake_detector.py, anomaly_detector.py) returns. Lock this first —
it's what lets risk_scorer.py, explainability.py, and response_engine.py
each be written once and reused across all three scenarios.

Owner: Sai
Team decisions baked into this schema:
  - risk_level is 3-stage: Low / Medium / High (not the PS's 5-stage scale)
  - indicators are weighted objects, not plain strings, so risk_scorer.py
    can sum weights into a 0-100 score instead of just counting them
"""

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class Indicator(BaseModel):
    """One piece of evidence a detector found, with a weight risk_scorer.py sums."""

    name: str  # e.g. "sender domain mismatch", "urgent tone", "impossible travel"
    weight: float = Field(ge=0.0, le=1.0)  # contribution to the risk score, 0-1


class DetectionResult(BaseModel):
    """
    Returned by phishing_detector.py, deepfake_detector.py, and
    anomaly_detector.py. Fields below the divider are filled in later
    in the pipeline (risk_scorer.py, explainability.py, response_engine.py) —
    detectors themselves leave them as None.
    """

    # --- set by the detector ---
    scenario: Literal["phishing", "deepfake", "anomaly"]
    event_id: str
    is_threat: bool
    confidence: float = Field(ge=0.0, le=1.0)  # model confidence
    indicators: list[Indicator] = Field(default_factory=list)
    source_type: Literal["live", "public_dataset", "self_collected", "synthetic"]
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

    # --- set later in the pipeline ---
    risk_level: Optional[Literal["Low", "Medium", "High"]] = None
    risk_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    explanation: Optional[str] = None          # plain-language reasoning (explainability.py)
    evidence: Optional[list[str]] = None       # supporting evidence shown in dashboard
    recommended_action: Optional[str] = None   # set by response_engine.py
    action_status: Literal["pending", "actioned", "dismissed"] = "pending"


if __name__ == "__main__":
    # Quick manual check — run `python schemas/detection_result.py` to sanity-check the model.
    example = DetectionResult(
        scenario="phishing",
        event_id="evt_001",
        is_threat=True,
        confidence=0.87,
        indicators=[
            Indicator(name="look-alike domain", weight=0.4),
            Indicator(name="urgent OTP request", weight=0.35),
        ],
        source_type="self_collected",
    )
    print(example.model_dump_json(indent=2))
