"""Challenge Engine.

Lets a recruiter disagree with a candidate's fit score for a stated reason,
and recomputes the score + confidence accordingly.

Design constraint: this must NOT call an LLM to "decide" a new score, and
must NOT silently overwrite the original ranking. Every challenge reason
maps to a fixed, documented penalty — so the same challenge on the same
candidate always produces the same result, and the recruiter can see
exactly what changed and why.

A challenge is also itself a signal: a human disagreeing with the system
is evidence the original score was less certain than it looked, so
confidence is reduced on every challenge, regardless of which reason was
selected.
"""

from dataclasses import dataclass


# Fixed penalty per challenge reason, applied as points subtracted from
# the original fit score. These are judgment calls, documented as such —
# not learned from data. Extend this list as real recruiter feedback
# patterns emerge; keep every entry traceable to a specific, named reason.
CHALLENGE_PENALTIES: dict[str, int] = {
    "portfolio_weak": 13,
    "missing_leadership": 10,
    "too_much_experience": 8,
    "missing_production_scale": 12,
    "resume_overoptimized": 15,
}

CHALLENGE_REASON_LABELS: dict[str, str] = {
    "portfolio_weak": "Portfolio depth insufficient",
    "missing_leadership": "Missing leadership signal",
    "too_much_experience": "Overqualified for role scope",
    "missing_production_scale": "Missing production-scale evidence",
    "resume_overoptimized": "Resume appears unusually optimized",
}

# Custom reasons (free text from the recruiter) get a smaller, fixed
# penalty since we have no specific signal to attach it to — large enough
# to move the ranking, small enough not to pretend we understood intent
# we can't actually verify.
CUSTOM_REASON_PENALTY = 8

# Every challenge reduces confidence by this many points, on top of
# whatever reason-specific score penalty applies. A human disagreeing is
# itself evidence the system's certainty should drop.
CHALLENGE_CONFIDENCE_PENALTY = 20


@dataclass(frozen=True)
class ChallengeResult:
    original_score: int
    new_score: int
    original_confidence: int
    new_confidence: int
    reason_code: str
    reason_label: str
    penalty_applied: int


def apply_challenge(
    *,
    original_score: int,
    original_confidence: int,
    reason_code: str,
    custom_reason: str | None = None,
) -> ChallengeResult:
    """Recompute a candidate's score/confidence after a recruiter challenge.

    Args:
        original_score: the candidate's current fit score (0-100).
        original_confidence: the candidate's current confidence (0-100).
        reason_code: one of CHALLENGE_PENALTIES' keys, or "custom".
        custom_reason: required if reason_code == "custom"; the
            recruiter's free-text disagreement, used only for the
            response label, not for scoring (we don't invent a penalty
            from free text we can't actually evaluate).

    Returns:
        ChallengeResult with both the original and recalculated values,
        so callers can show "89 -> 76" rather than silently replacing it.

    Raises:
        ValueError: if reason_code is unrecognized, or if reason_code is
            "custom" but no custom_reason text was provided.
    """
    if reason_code == "custom":
        if not custom_reason or not custom_reason.strip():
            raise ValueError("custom_reason is required when reason_code is 'custom'.")
        penalty = CUSTOM_REASON_PENALTY
        label = custom_reason.strip()
    elif reason_code in CHALLENGE_PENALTIES:
        penalty = CHALLENGE_PENALTIES[reason_code]
        label = CHALLENGE_REASON_LABELS[reason_code]
    else:
        valid = ", ".join(list(CHALLENGE_PENALTIES.keys()) + ["custom"])
        raise ValueError(f"Unknown reason_code '{reason_code}'. Valid options: {valid}")

    new_score = max(0, original_score - penalty)
    new_confidence = max(0, original_confidence - CHALLENGE_CONFIDENCE_PENALTY)

    return ChallengeResult(
        original_score=original_score,
        new_score=new_score,
        original_confidence=original_confidence,
        new_confidence=new_confidence,
        reason_code=reason_code,
        reason_label=label,
        penalty_applied=penalty,
    )