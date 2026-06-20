"use client";

import { useState } from "react";

import type { Candidate, ChallengeResult } from "../services/api";
import ChallengePanel from "./ChallengePanel";
import ConfidenceMeter from "./ConfidenceMeter";

type CandidateCardProps = {
  candidate: Candidate;
};

function evidenceClass(evidence: string) {
  return `evidence-${evidence.toLowerCase().replace(/\s+/g, "-")}`;
}

export default function CandidateCard({ candidate }: CandidateCardProps) {
  const rank = candidate.rank ?? candidate.id;
  const hasExplanation =
    candidate.explanation &&
    (candidate.explanation.positives.length > 0 || candidate.explanation.negatives.length > 0);

  // Challenge results are applied locally on top of the original API
  // response, not by re-fetching /rank. This keeps the original score
  // visible alongside the adjusted one (see challengeLog), matching the
  // README's "89 -> 76" display, not a silent overwrite.
  const [challengeLog, setChallengeLog] = useState<ChallengeResult | null>(null);

  const displayedScore = challengeLog?.new_score ?? candidate.score;
  const displayedConfidence = challengeLog?.new_confidence ?? candidate.confidence;

  return (
    <article className="candidate-card">
      <div className="rank-badge">#{rank}</div>

      <div className="candidate-main">
        <div className="candidate-name">{candidate.name}</div>
        <div className="candidate-file">{candidate.filename}</div>
        <div className="candidate-meta">
          <span className="meta-pill">
            <span className={`evidence-dot ${evidenceClass(candidate.evidence)}`} />
            Evidence: {candidate.evidence}
          </span>
          <span className="meta-pill">Semantic match</span>
        </div>

        {hasExplanation && (
          <div className="explanation-block">
            {candidate.explanation.positives.length > 0 && (
              <ul className="explanation-positives">
                {candidate.explanation.positives.map((point) => (
                  <li key={point}>+ {point}</li>
                ))}
              </ul>
            )}
            {candidate.explanation.negatives.length > 0 && (
              <ul className="explanation-negatives">
                {candidate.explanation.negatives.map((point) => (
                  <li key={point}>− {point}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        {challengeLog && (
          <div className="challenge-log">
            Challenged: {challengeLog.reason_label} — Score {challengeLog.original_score} →{" "}
            {challengeLog.new_score}, Confidence {challengeLog.original_confidence} →{" "}
            {challengeLog.new_confidence}
          </div>
        )}

        <ChallengePanel
          candidateId={candidate.id}
          currentScore={displayedScore}
          currentConfidence={displayedConfidence}
          onChallenged={setChallengeLog}
        />
      </div>

      <div className="score-block">
        <span className="score-label">Fit</span>
        <span className="score-value">{displayedScore}</span>
      </div>

      <ConfidenceMeter value={displayedConfidence} reasons={candidate.confidence_reasons} />
    </article>
  );
}