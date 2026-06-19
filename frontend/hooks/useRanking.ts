"use client";

import { useState } from "react";
import type { Candidate } from "../services/api";
import { getRanking } from "../services/api";

export function useRanking(initialCandidates: Candidate[] = []) {
  const [candidates, setCandidates] = useState<Candidate[]>(initialCandidates);
  const [isRanking, setIsRanking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refreshRanking() {
    setIsRanking(true);
    setError(null);

    try {
      const ranked = await getRanking();
      setCandidates(ranked);
    } catch {
      setError("Ranking service unavailable");
    } finally {
      setIsRanking(false);
    }
  }

  return {
    candidates,
    error,
    isRanking,
    refreshRanking
  };
}
