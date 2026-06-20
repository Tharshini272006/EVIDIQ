"use client";

import { useState } from "react";

import type { ChallengeReasonCode, ChallengeResult } from "../services/api";
import { challengeCandidate } from "../services/api";

type ChallengePanelProps = {
  candidateId: number;
  currentScore: number;
  currentConfidence: number;
  onChallenged: (result: ChallengeResult) => void;
};

// Labels shown to the recruiter. Keys must match backend
// challenge_engine.CHALLENGE_PENALTIES exactly.
const REASON_OPTIONS: { code: ChallengeReasonCode; label: string }[] = [
  { code: "portfolio_weak", label: "Portfolio weak" },
  { code: "missing_leadership", label: "Missing leadership" },
  { code: "too_much_experience", label: "Too much experience" },
  { code: "missing_production_scale", label: "Missing production scale" },
  { code: "resume_overoptimized", label: "Resume unusually optimized" }
];

export default function ChallengePanel({
  candidateId,
  currentScore,
  currentConfidence,
  onChallenged
}: ChallengePanelProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [customReason, setCustomReason] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submitChallenge(reasonCode: ChallengeReasonCode, customText?: string) {
    setIsSubmitting(true);
    setError(null);

    try {
      const result = await challengeCandidate({
        candidateId,
        originalScore: currentScore,
        originalConfidence: currentConfidence,
        reasonCode,
        customReason: customText
      });

      onChallenged(result);
      setIsOpen(false);
      setCustomReason("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Challenge failed");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (!isOpen) {
    return (
      <button className="challenge-trigger" onClick={() => setIsOpen(true)} type="button">
        Challenge
      </button>
    );
  }

  return (
    <div className="challenge-panel">
      <div className="challenge-header">
        <span>Why do you disagree?</span>
        <button
          className="challenge-close"
          onClick={() => setIsOpen(false)}
          type="button"
          aria-label="Close challenge panel"
        >
          ×
        </button>
      </div>

      <div className="challenge-options">
        {REASON_OPTIONS.map((option) => (
          <button
            className="challenge-option"
            disabled={isSubmitting}
            key={option.code}
            onClick={() => submitChallenge(option.code)}
            type="button"
          >
            {option.label}
          </button>
        ))}
      </div>

      <div className="challenge-custom">
        <input
          disabled={isSubmitting}
          onChange={(event) => setCustomReason(event.target.value)}
          placeholder="Custom reason..."
          type="text"
          value={customReason}
        />
        <button
          disabled={isSubmitting || !customReason.trim()}
          onClick={() => submitChallenge("custom", customReason)}
          type="button"
        >
          Submit
        </button>
      </div>

      {error && <div className="challenge-error">{error}</div>}
    </div>
  );
}