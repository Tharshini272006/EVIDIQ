import type { Candidate } from "../services/api";
import CandidateCard from "./CandidateCard";

type RankingTableProps = {
  candidates: Candidate[];
};

export default function RankingTable({ candidates }: RankingTableProps) {
  if (!candidates.length) {
    return <div className="empty-state">Upload candidates and run analysis.</div>;
  }

  return (
    <div className="candidate-list">
      {candidates.map((candidate) => (
        <CandidateCard candidate={candidate} key={`${candidate.id}-${candidate.filename}`} />
      ))}
    </div>
  );
}
