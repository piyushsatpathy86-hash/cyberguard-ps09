"""
modules/response_engine.py
Maps a scored DetectionResult (scenario + risk_level) to a recommended
action string, per the PS's Component E (Intelligent Response
Recommendation): block URL, quarantine email, warn user, require re-auth,
revoke session, flag for manual review, notify admin/SOC, escalate.

Shared across all 3 scenarios -- written once, reused everywhere, per the
DetectionResult contract in schemas/detection_result.py.

Owner: Sai
"""

from schemas.detection_result import DetectionResult

# Action text per (scenario, risk_level). Deepfake is included even though
# it's not Sai's detector, since this engine is shared across all 3 scenarios.
ACTION_MAP = {
    "phishing": {
        "Low": "No action needed; log for monitoring.",
        "Medium": "Flag for manual review; warn user about the suspicious message.",
        "High": "Quarantine email / block URL immediately; warn user; notify admin/SOC.",
    },
    "deepfake": {
        "Low": "No action needed; log for monitoring.",
        "Medium": "Flag for manual review; warn user the media may be manipulated.",
        "High": "Block/remove content; warn affected user; escalate to admin/SOC.",
    },
    "anomaly": {
        "Low": "No action needed; log for monitoring.",
        "Medium": "Require re-authentication; flag account for review.",
        "High": "Revoke active session; require re-authentication; notify admin/SOC; escalate incident.",
    },
}

DEFAULT_ACTION = "Flag for manual review -- no mapped action for this scenario/risk_level."


def recommend_action(result: DetectionResult) -> DetectionResult:
    """
    Fill in recommended_action on a DetectionResult in place, and return it.
    Assumes risk_scorer.score_detection() has already run (risk_level is set).
    Always sets action_status to "pending" -- an admin/SOC analyst actions
    or dismisses it later via the dashboard.
    """
    scenario_actions = ACTION_MAP.get(result.scenario, {})
    result.recommended_action = scenario_actions.get(result.risk_level, DEFAULT_ACTION)
    result.action_status = "pending"
    return result


if __name__ == "__main__":
    # Quick manual check -- run `python -m modules.response_engine` from app/.
    from schemas.detection_result import Indicator
    from modules.risk_scorer import score_detection

    example = DetectionResult(
        scenario="anomaly",
        event_id="evt_test",
        is_threat=True,
        confidence=0.85,
        indicators=[
            Indicator(name="impossible travel", weight=0.5),
            Indicator(name="new device", weight=0.3),
        ],
        source_type="synthetic",
    )
    scored = score_detection(example)
    actioned = recommend_action(scored)
    print(f"scenario={actioned.scenario}  risk_level={actioned.risk_level}")
    print(f"recommended_action={actioned.recommended_action}")
    print(f"action_status={actioned.action_status}")
