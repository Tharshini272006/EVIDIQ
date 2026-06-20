"""Hidden Talent Engine.

Identifies candidates whose semantic fit score is mediocre but whose
literal skill-overlap (from explanation_engine) is strong — meaning the
embedding similarity may be undersold by resume wording/length/structure,
not by an actual lack of relevant skills.

This is NOT a separate model and does NOT invent a new "potential" score
from nothing. It is a deterministic re-read of two numbers that already
exist for every candidate:
  - fit score (cosine similarity, from rank_engine)
  - matched_skills / missing_skills (literal overlap, from explanation_engine)

A candidate qualifies as "hidden talent" only if BOTH are true:
  1. Their fit score sits below the "Strong" threshold (so they would NOT
     already be surfaced as a top recommendation).
  2. Their literal skill-match ratio (matched / (matched + missing)) is
     notably higher than what their fit score alone would suggest.

This surfaces a real, explainable mismatch between "how similar the whole
resume reads" and "how many required skills are actually present" — which
is exactly the gap a keyword-only ATS or a single opaque score would miss.
"""

from dataclasses import dataclass


# A candidate is even considered for hidden-talent review only if their
# score is below this — candidates already ranked "Strong" don't need to
# be "discovered," they're already visible at the top of the list.
HIDDEN_TALENT_SCORE_CEILING = 80

# Minimum number of total skills (matched + missing) required before we'll
# trust the match ratio at all — with very few skills mentioned in the job,
# a single match/miss swings the ratio wildly and isn't a reliable signal.
MIN_TOTAL_SKILLS_FOR_SIGNAL = 3

# How much higher the skill-match ratio (0-100) must be than the fit score
# for the gap to be worth flagging. This is a judgment call, documented as
# such — not derived from a labeled dataset.
MIN_GAP_TO_FLAG = 20


@dataclass(frozen=True)
class HiddenTalentResult:
    candidate_id: int
    name: str
    fit_score: int
    skill_match_ratio: int  # 0-100, literal skill overlap
    gap: int  # skill_match_ratio - fit_score
    matched_skills: list[str]
    missing_skills: list[str]


def _skill_match_ratio(matched_skills: list[str], missing_skills: list[str]) -> int | None:
    total = len(matched_skills) + len(missing_skills)

    if total < MIN_TOTAL_SKILLS_FOR_SIGNAL:
        return None

    return round((len(matched_skills) / total) * 100)


def find_hidden_talent(ranked_candidates: list[dict]) -> list[HiddenTalentResult]:
    """Scan an already-ranked candidate list for undersold candidates.

    Args:
        ranked_candidates: the list of dicts produced by
            rank_engine.rank_candidates() — must include "score",
            "explanation.matched_skills", "explanation.missing_skills".

    Returns:
        HiddenTalentResult entries, sorted by gap size (largest first) —
        i.e. the candidates whose resume wording most understates their
        actual skill coverage relative to the job.
    """
    results = []

    for candidate in ranked_candidates:
        score = candidate["score"]

        if score >= HIDDEN_TALENT_SCORE_CEILING:
            continue  # already a visible top recommendation

        explanation = candidate.get("explanation", {})
        matched = explanation.get("matched_skills", [])
        missing = explanation.get("missing_skills", [])

        ratio = _skill_match_ratio(matched, missing)
        if ratio is None:
            continue  # not enough skill signal to trust the comparison

        gap = ratio - score
        if gap < MIN_GAP_TO_FLAG:
            continue  # fit score already reflects the skill match reasonably well

        results.append(
            HiddenTalentResult(
                candidate_id=candidate["id"],
                name=candidate["name"],
                fit_score=score,
                skill_match_ratio=ratio,
                gap=gap,
                matched_skills=matched,
                missing_skills=missing,
            )
        )

    results.sort(key=lambda r: r.gap, reverse=True)
    return results