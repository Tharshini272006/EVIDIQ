from fastapi import APIRouter, Query

from backend.services.ranking.rank_engine import rank_candidates

router = APIRouter()


@router.get("/rank")
def rank(top_k: int | None = Query(default=None, ge=1, le=100)):
    return rank_candidates(top_k=top_k)


@router.get("/rank/top")
def top_candidates(limit: int = Query(default=5, ge=1, le=25)):
    return rank_candidates(top_k=limit)
