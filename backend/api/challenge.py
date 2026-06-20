"""Challenge endpoint: recruiter disagrees with a ranking, system recomputes.

This is EVIDIQ's human-in-the-loop layer (see README "Recruiter Challenge
Layer"). It does not re-run the embedding/similarity pipeline — it applies
a documented penalty on top of the existing score, via challenge_engine.
See that module for why scores are adjusted by fixed amounts rather than
recalculated by a model.
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.challenge_schema import ChallengeRequest, ChallengeResponse
from backend.services.confidence.challenge_engine import apply_challenge

router = APIRouter()


@router.post("/challenge", response_model=ChallengeResponse)
def challenge_candidate(payload: ChallengeRequest) -> ChallengeResponse:
    try:
        result = apply_challenge(
            original_score=payload.original_score,
            original_confidence=payload.original_confidence,
            reason_code=payload.reason_code,
            custom_reason=payload.custom_reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ChallengeResponse(
        candidate_id=payload.candidate_id,
        original_score=result.original_score,
        new_score=result.new_score,
        original_confidence=result.original_confidence,
        new_confidence=result.new_confidence,
        reason_code=result.reason_code,
        reason_label=result.reason_label,
        penalty_applied=result.penalty_applied,
    )