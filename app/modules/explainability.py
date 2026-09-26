"""
modules/explainability.py
Fills in a DetectionResult's `evidence` (deterministic, built from indicators)
and `explanation` (a plain-language reasoning paragraph from Groq). Only
runs for Medium/High risk results — Low risk is skipped to conserve
Groq's free-tier rate limit (per the PS's own guidance).

Owner: Sai
Design decisions:
  - evidence list is built directly from indicator names, not from the LLM,
    so the dashboard always has something to show even if Groq is down/slow
  - Groq is only asked to write the reasoning paragraph, not structured
    JSON, to avoid fragile parsing right before a live demo
  - if the Groq call fails for any reason, a template-based fallback
    sentence is used instead of leaving `explanation` empty
"""

from groq import Groq

from schemas.detection_result import DetectionResult
from config import get_groq_api_key, GROQ_MODEL

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=get_groq_api_key())
    return _client


def _build_evidence(result: DetectionResult) -> list[str]:
    """Deterministic, always-available list of indicator names for the dashboard."""
    return [ind.name for ind in result.indicators]


def _build_prompt(result: DetectionResult, evidence: list[str]) -> str:
    evidence_text = "; ".join(evidence) if evidence else "no specific indicators logged"
    return (
        f"A cybersecurity system flagged a '{result.scenario}' event as "
        f"{result.risk_level} risk (confidence {result.confidence:.0%}). "
        f"Evidence found: {evidence_text}. "
        "In 1-2 plain-language sentences, explain to a non-technical "
        "administrator why this was flagged and what it means. "
        "Do not repeat the raw evidence list verbatim -- explain its "
        "significance instead. Frame this as decision-support, not a "
        "certified diagnosis."
    )


def _fallback_explanation(result: DetectionResult, evidence: list[str]) -> str:
    """Used if the Groq call fails -- keeps the demo from breaking on a rate limit/timeout."""
    if evidence:
        return (
            f"This {result.scenario} event was flagged as {result.risk_level} risk "
            f"based on: {', '.join(evidence)}. Recommend manual review."
        )
    return (
        f"This {result.scenario} event was flagged as {result.risk_level} risk "
        "by the detection model. Recommend manual review."
    )


def explain_detection(result: DetectionResult) -> DetectionResult:
    """
    Fill in evidence + explanation on a DetectionResult in place, and return it.
    Assumes risk_scorer.score_detection() has already run (risk_level is set).
    """
    if result.risk_level == "Low":
        return result  # skip -- conserve Groq quota, nothing notable to explain

    evidence = _build_evidence(result)
    result.evidence = evidence

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": _build_prompt(result, evidence)}],
            max_completion_tokens=400,
            temperature=0.3,
            reasoning_effort="low",  # gpt-oss models reason internally; keep it brief
        )
        result.explanation = response.choices[0].message.content.strip()
    except Exception as exc:  # network issue, rate limit, bad key, etc.
        print(f"[explainability] Groq call failed ({exc}); using fallback explanation.")
        result.explanation = _fallback_explanation(result, evidence)

    return result


if __name__ == "__main__":
    # Quick manual check -- run `python -m modules.explainability` from app/.
    # Requires GROQ_API_KEY in .streamlit/secrets.toml or as an env var.
    from schemas.detection_result import Indicator
    from modules.risk_scorer import score_detection

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
    explained = explain_detection(scored)
    print(f"risk_level={explained.risk_level}")
    print(f"evidence={explained.evidence}")
    print(f"explanation={explained.explanation}")
