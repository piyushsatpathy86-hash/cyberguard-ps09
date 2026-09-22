"""
Task 10: Recommended response mapping — Component E of the PS.

Maps (scenario, risk_level) -> recommended_action, e.g.:
    Block URL | Quarantine email | Warn user | Require re-auth |
    Revoke session | Flag for manual review | Notify admin/SOC | Escalate

Write once, reused across all three scenarios via the DetectionResult
contract.
"""

from app.schemas.detection_result import DetectionResult


def recommend_action(result: DetectionResult) -> DetectionResult:
    """
    Populate result.recommended_action based on result.scenario and
    result.risk_level, then return the updated result.
    Owner: define the actual (scenario, risk_level) -> action mapping below.
    """
    raise NotImplementedError("Task 10 owner: implement response_engine.recommend_action")
