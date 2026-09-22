"""
Task 9: Shared risk-scoring logic — used by ALL three scenarios.

Converts confidence + indicator count/type into risk_level
(Safe -> Low -> Medium -> High -> Critical) and logs contributing_factors.

Write this ONCE against the DetectionResult contract — do not fork per
scenario unless a scenario genuinely needs different thresholds.
"""

from app.schemas.detection_result import RISK_LEVELS, DetectionResult


def score_risk(result: DetectionResult) -> DetectionResult:
    """
    Populate result.risk_level and result.risk_contributing_factors based
    on result.confidence and result.indicators, then return the updated
    result. Owner: define the actual thresholds below.

    Suggested starting point (tune during testing):
        confidence < 0.3            -> Safe
        0.3 <= confidence < 0.5     -> Low
        0.5 <= confidence < 0.7     -> Medium
        0.7 <= confidence < 0.9     -> High
        confidence >= 0.9           -> Critical
    (Adjust by scenario / indicator count as needed.)
    """
    raise NotImplementedError("Task 9 owner: implement risk_scorer.score_risk")
