"""
modules/risk_scorer.py
Takes a DetectionResult already filled in by a detector (phishing_detector.py,
deepfake_detector.py, or anomaly_detector.py) and sets its risk_score (0-100)
and risk_level (Low / Medium / High).

Shared across all 3 scenarios — written once, reused everywhere, per the
DetectionResult contract in schemas/detection_result.py.

Owner: Sai
Team decision: score blends model confidence and summed indicator weights
(averaged), rather than using either alone.
"""

from schemas.detection_result import DetectionResult
from config import score_to_level


def score_detection(result: DetectionResult) -> DetectionResult:
    """
    Fill in risk_score and risk_level on a DetectionResult in place, and
    return it (for convenient chaining).

    If the detector already decided this isn't a threat, we don't run it
    through the blend — it's scored 0 / Low directly. This also keeps
    false-positive-prone detectors from accidentally scoring a "safe" event
    into Medium/High just because of a couple of low-weight indicators.
    """
    if not result.is_threat:
        result.risk_score = 0.0
        result.risk_level = "Low"
        return result

    # Sum indicator weights, capped at 1.0 so one detector emitting many
    # indicators doesn't blow the scale past what confidence alone would give.
    indicator_sum = sum(ind.weight for ind in result.indicators)
    indicator_component = min(indicator_sum, 1.0)

    blended = (result.confidence + indicator_component) / 2
    result.risk_score = round(blended * 100, 1)
    result.risk_level = score_to_level(result.risk_score)
    return result


if __name__ == "__main__":
    # Quick manual check — run `python modules/risk_scorer.py` from app/.
    from schemas.detection_result import Indicator

    example = DetectionResult(
        scenario="phishing",
        event_id="evt_test",
        is_threat=True,
        confidence=0.9,
        indicators=[
            Indicator(name="look-alike domain", weight=0.4),
            Indicator(name="urgent OTP request", weight=0.35),
        ],
        source_type="synthetic",
    )
    scored = score_detection(example)
    print(f"risk_score={scored.risk_score}  risk_level={scored.risk_level}")

    safe_example = DetectionResult(
        scenario="phishing",
        event_id="evt_test_safe",
        is_threat=False,
        confidence=0.05,
        indicators=[],
        source_type="synthetic",
    )
    scored_safe = score_detection(safe_example)
    print(f"risk_score={scored_safe.risk_score}  risk_level={scored_safe.risk_level}")
