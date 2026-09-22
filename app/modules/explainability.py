"""
Task 10: Explainable AI via Groq — Component D of the PS, and the single
biggest differentiator most teams will skip.

Rule: only call Groq for non-Safe detections (see config.EXPLAIN_MIN_RISK_LEVEL)
to conserve free-tier rate limits.

Rehearse the live demo with a fallback: cache Groq responses for exact demo
inputs in case of live API rate-limit or timeout during judging.
"""

from app.config import EXPLAIN_MIN_RISK_LEVEL, GROQ_API_KEY, GROQ_MODEL
from app.schemas.detection_result import RISK_LEVELS, DetectionResult


def explain(result: DetectionResult) -> DetectionResult:
    """
    If result.risk_level is above EXPLAIN_MIN_RISK_LEVEL, call Groq to turn
    result.indicators into a plain-language reasoning paragraph + evidence
    list, and populate result.explanation / result.evidence_list.

    If risk_level is "Safe", skip the API call entirely and return result
    unchanged — this is intentional, not a bug.

    Owner: implement the Groq chat-completion call below. Frame the prompt
    to produce decision-support language, not a certified diagnosis
    (e.g. "indicators suggest..." not "this IS phishing").
    """
    raise NotImplementedError("Task 10 owner: implement explainability.explain")
