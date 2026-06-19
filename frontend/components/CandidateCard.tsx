import type { Candidate } from "../services/api";
import ConfidenceMeter from "./ConfidenceMeter";

type CandidateCardProps = {
  candidate: Candidate;
};

function evidenceClass(evidence: string) {
  return `evidence-${evidence.toLowerCase().replace(/\s+/g, "-")}`;
}

export default function CandidateCard({ candidate }: CandidateCardProps) {
  const rank = candidate.rank ?? candidate.id;

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
      </div>

      <div className="score-block">
        <span className="score-label">Fit</span>
        <span className="score-value">{candidate.score}</span>
        <ConfidenceMeter value={candidate.score} />
      </div>
    </article>
  );
}
