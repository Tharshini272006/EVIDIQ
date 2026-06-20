"""Confidence Engine.

Separates "how good is this candidate" (fit score, computed elsewhere via
cosine similarity) from "how sure are we that this fit score is reliable"
(confidence, computed here).

Every signal used below is traceable to something real and inspectable:
no learned model, no invented constant pulled from nowhere. If you add a
new signal, it must come from an actual measurable property of the parsed
resume or the score itself — see EVIDIQ Copilot instructions.

Signals used:
  1. Evidence volume   — word count of parsed resume text. A 40-word resume
                          gives the embedding model almost nothing to match
                          against; low volume means low confidence regardless
                          of what score comes out.
  2. Parse quality      — whether extraction used the clean format-specific
                          parser (PDF/DOCX) or fell back to raw byte
                          decoding. Fallback text can be incomplete or
                          garbled, so it's weighted down.
  3. Score ambiguity     — fit scores near the decision boundary (neither
                          clearly strong nor clearly weak) are inherently
                          less certain than scores far from that boundary,
                          independent of how much evidence exists.
"""

from dataclasses import dataclass


# Word-count thresholds for evidence volume. These are deliberately coarse
# and documented as judgment calls, not derived from a dataset — a resume
# under ~80 words is very unlikely to contain enough signal to trust a
# similarity score against; above ~250 words, more length adds little
# additional certainty.
MIN_RELIABLE_WORD_COUNT = 80
FULL_CONFIDENCE_WORD_COUNT = 250

# Fit-score band considered "ambiguous": not confidently strong, not
# confidently weak. This intentionally does NOT use the same boundaries as
# the Strong/Medium/Needs-review label in rank_engine — confidence is about
# certainty, not about the quality verdict itself.
AMBIGUOUS_SCORE_LOW = 55
AMBIGUOUS_SCORE_HIGH = 75


@dataclass(frozen=True)
class ConfidenceResult:
    confidence: int  # 0-100
    reasons: list[str]  # human-readable, traceable to the signals above


def _evidence_volume_factor(word_count: int) -> tuple[float, str | None]:
    """Returns a 0.0-1.0 multiplier based on how much resume text exists."""
    if word_count < MIN_RELIABLE_WORD_COUNT:
        return 0.4, f"Only {word_count} words extracted — limited evidence to evaluate."

    if word_count >= FULL_CONFIDENCE_WORD_COUNT:
        return 1.0, None

    # Linear ramp between the low and high thresholds.
    span = FULL_CONFIDENCE_WORD_COUNT - MIN_RELIABLE_WORD_COUNT
    progress = (word_count - MIN_RELIABLE_WORD_COUNT) / span
    factor = 0.4 + (0.6 * progress)
    return factor, None


def _parse_quality_factor(clean_parse: bool) -> tuple[float, str | None]:
    if clean_parse:
        return 1.0, None
    return 0.6, "Resume required fallback text extraction — content may be incomplete."


def _score_certainty_factor(fit_score: int) -> tuple[float, str | None]:
    """Scores in the ambiguous band reduce confidence even with good evidence."""
    if AMBIGUOUS_SCORE_LOW <= fit_score <= AMBIGUOUS_SCORE_HIGH:
        return 0.75, "Fit score sits in an ambiguous range — not clearly strong or weak."
    return 1.0, None


def compute_confidence(
    *,
    resume_text: str,
    clean_parse: bool,
    fit_score: int,
) -> ConfidenceResult:
    """Compute a 0-100 confidence score for a single candidate's fit score.

    Args:
        resume_text: the parsed resume text actually used for embedding.
        clean_parse: True if format-specific parsing succeeded (see
            resume_parser.ParseResult.clean); False if the fallback
            raw-byte path was used.
        fit_score: the 0-100 similarity-based fit score from rank_engine.

    Returns:
        ConfidenceResult with a 0-100 confidence value and the specific
        reasons that pulled confidence down (empty list if none did).
    """
    word_count = len(resume_text.split())

    volume_factor, volume_reason = _evidence_volume_factor(word_count)
    parse_factor, parse_reason = _parse_quality_factor(clean_parse)
    certainty_factor, certainty_reason = _score_certainty_factor(fit_score)

    combined_factor = volume_factor * parse_factor * certainty_factor
    confidence = round(combined_factor * 100)
    confidence = max(0, min(confidence, 100))

    reasons = [r for r in (volume_reason, parse_reason, certainty_reason) if r]

    return ConfidenceResult(confidence=confidence, reasons=reasons)