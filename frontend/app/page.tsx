"use client";

import RankingTable from "../components/RankingTable";
import UploadBox from "../components/UploadBox";
import { useRanking } from "../hooks/useRanking";
import { useUpload } from "../hooks/useUpload";
import type { Candidate } from "../services/api";

const seedCandidates: Candidate[] = [
  {
    id: 1,
    rank: 1,
    name: "Sarah Chen",
    filename: "sarah_chen_resume.pdf",
    score: 92,
    evidence: "Strong"
  },
  {
    id: 2,
    rank: 2,
    name: "Alex Morgan",
    filename: "alex_morgan_resume.pdf",
    score: 84,
    evidence: "Medium"
  },
  {
    id: 3,
    rank: 3,
    name: "Candidate 42",
    filename: "candidate_42_projects.pdf",
    score: 78,
    evidence: "Medium"
  }
];

export default function Home() {
  const { candidates, error: rankingError, isRanking, refreshRanking } = useRanking(seedCandidates);
  const { error: uploadError, isUploading, uploadFiles } = useUpload();
  const isWorking = isRanking || isUploading;

  async function analyze(jobFile: File | null, candidateFiles: FileList | null) {
    try {
      await uploadFiles(jobFile, candidateFiles);
    } catch {
      return;
    }

    await refreshRanking();
  }

  return (
    <main className="page-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-title">EVIDIQ</div>
          <div className="brand-subtitle">Candidate Intelligence Platform</div>
        </div>

        <div className="status-chip">
          <span className="status-dot" />
          Day 2 demo
        </div>
      </header>

      <div className="workspace">
        <UploadBox disabled={isWorking} onAnalyze={analyze} />

        <section className="dashboard">
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Job</span>
              <span className="summary-value">Senior AI Engineer</span>
              <span className="summary-note">Active role</span>
            </div>

            <div className="summary-item">
              <span className="summary-label">Candidates</span>
              <span className="summary-value">{candidates.length}</span>
              <span className="summary-note">Loaded shortlist</span>
            </div>

            <div className="summary-item">
              <span className="summary-label">Ranking</span>
              <span className="summary-value">{isWorking ? "Running" : "Ready"}</span>
              <span className="summary-note">Semantic similarity</span>
            </div>
          </div>

          <div className="section-header">
            <h1 className="section-title">Top Recommendations</h1>
            <button
              className="secondary-button"
              disabled={isWorking}
              onClick={refreshRanking}
              type="button"
            >
              Refresh
            </button>
          </div>

          {(uploadError || rankingError) && (
            <div className="status-chip">{uploadError ?? rankingError}</div>
          )}

          <RankingTable candidates={candidates} />
        </section>
      </div>
    </main>
  );
}
