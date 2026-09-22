"""
Shared contract for all three detection engines (phishing, deepfake, anomaly).

CRITICAL: This file is Task 4 in the build order. Once this shape is agreed
by the team, risk_scorer.py, explainability.py, and response_engine.py can
each be written ONCE and reused across all scenarios, and the three
detector owners can work fully in parallel.

Do not change field names after the team has started building against this
contract without a re-sync — every downstream module depends on this shape.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    scenario: str  # "phishing" | "deepfake" | "anomaly"
    event_id: str
    is_threat: bool
    confidence: float = Field(ge=0.0, le=1.0)  # model confidence 0-1
    indicators: list[str] = Field(default_factory=list)  # e.g. ["sender domain mismatch", "urgent tone"]

    # Set downstream by risk_scorer.py
    risk_level: Optional[str] = None  # "Safe" | "Low" | "Medium" | "High" | "Critical"
    risk_contributing_factors: Optional[list[str]] = None

    # Set downstream by explainability.py (Groq) — only populated for non-Safe results
    explanation: Optional[str] = None
    evidence_list: Optional[list[str]] = None

    # Set downstream by response_engine.py
    recommended_action: Optional[str] = None

    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "phishing",
                "event_id": "evt_00123",
                "is_threat": True,
                "confidence": 0.91,
                "indicators": ["urgent OTP request", "look-alike bank domain"],
                "risk_level": "High",
                "risk_contributing_factors": ["confidence > 0.85", "2+ indicators"],
                "explanation": "This message impersonates a bank and pressures immediate action...",
                "evidence_list": ["sender domain: bank-secure-login.co vs bankofindia.co.in"],
                "recommended_action": "Warn user, do not click link",
                "evaluated_at": "2026-09-22T10:00:00Z",
            }
        }


# Allowed risk levels, in ascending severity order — import this instead of
# hardcoding strings so risk_scorer.py stays the single source of truth.
RISK_LEVELS = ["Safe", "Low", "Medium", "High", "Critical"]

# Allowed scenario names — import this instead of hardcoding strings.
SCENARIOS = ["phishing", "deepfake", "anomaly"]
