"""Request/response schemas for the Challenge endpoint."""

from pydantic import BaseModel, Field


class ChallengeRequest(BaseModel):
    candidate_id: int = Field(..., description="The candidate's id from /rank.")
    original_score: int = Field(..., ge=0, le=100)
    original_confidence: int = Field(..., ge=0, le=100)
    reason_code: str = Field(
        ...,
        description=(
            "One of: portfolio_weak, missing_leadership, too_much_experience, "
            "missing_production_scale, resume_overoptimized, custom"
        ),
    )
    custom_reason: str | None = Field(
        default=None,
        description="Required free-text reason if reason_code is 'custom'.",
    )


class ChallengeResponse(BaseModel):
    candidate_id: int
    original_score: int
    new_score: int
    original_confidence: int
    new_confidence: int
    reason_code: str
    reason_label: str
    penalty_applied: int