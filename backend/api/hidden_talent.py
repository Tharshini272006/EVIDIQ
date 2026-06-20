"""Hidden Talent endpoint.

Re-reads the existing ranking (does not re-run embeddings) to surface
candidates whose fit score may understate their actual skill coverage.
See backend/services/ranking/hidden_talent_engine.py for the exact,
documented criteria used.
"""

from fastapi import APIRouter

from backend.services.ranking.hidden_talent_engine import find_hidden_talent
from backend.services.ranking.rank_engine import rank_candidates

router = APIRouter()


@router.get("/rank/hidden-talent")
def hidden_talent():
    ranked = rank_candidates()
    flagged = find_hidden_talent(ranked)

    return [
        {
            "candidate_id": result.candidate_id,
            "name": result.name,
            "fit_score": result.fit_score,
            "skill_match_ratio": result.skill_match_ratio,
            "gap": result.gap,
            "matched_skills": result.matched_skills,
            "missing_skills": result.missing_skills,
        }
        for result in flagged
    ]