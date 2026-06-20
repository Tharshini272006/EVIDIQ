"use client";

import { useEffect } from "react";

import RankingTable from "../components/RankingTable";
import UploadBox from "../components/UploadBox";
import { useRanking } from "../hooks/useRanking";
import { useUpload } from "../hooks/useUpload";

export default function Home() {
  const { candidates, error: rankingError, isRanking, refreshRanking } = useRanking([]);
  const { error: uploadError, isUploading, uploadFiles } = useUpload();
  const isWorking = isRanking || isUploading;

  useEffect(() => {
    refreshRanking();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
          Live ranking
        </div>
      </header>

      <div className="workspace">
        <UploadBox disabled={isWorking} onAnalyze={analyze} />

        <section className="dashboard">
          <div className="summary-grid">
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