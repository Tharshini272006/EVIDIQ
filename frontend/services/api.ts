export type Explanation = {
  positives: string[];
  negatives: string[];
  matched_skills: string[];
  missing_skills: string[];
};

export type Candidate = {
  id: number;
  rank?: number;
  name: string;
  filename: string;
  score: number;
  confidence: number;
  confidence_reasons: string[];
  evidence: "Strong" | "Medium" | "Needs review" | string;
  explanation: Explanation;
};

// Mirrors backend/services/confidence/challenge_engine.py CHALLENGE_PENALTIES
// keys exactly. If you add a reason on the backend, add it here too.
export type ChallengeReasonCode =
  | "portfolio_weak"
  | "missing_leadership"
  | "too_much_experience"
  | "missing_production_scale"
  | "resume_overoptimized"
  | "custom";

export type ChallengeResult = {
  candidate_id: number;
  original_score: number;
  new_score: number;
  original_confidence: number;
  new_confidence: number;
  reason_code: string;
  reason_label: string;
  penalty_applied: number;
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function uploadJob(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload/job`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    throw new Error("Job upload failed");
  }

  return response.json();
}

export async function uploadCandidates(files: FileList) {
  const formData = new FormData();

  Array.from(files).forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    throw new Error("Candidate upload failed");
  }

  return response.json();
}

export async function getRanking(topK = 20): Promise<Candidate[]> {
  const response = await fetch(`${API_BASE}/rank?top_k=${topK}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error("Ranking request failed");
  }

  return response.json();
}

export async function challengeCandidate(params: {
  candidateId: number;
  originalScore: number;
  originalConfidence: number;
  reasonCode: ChallengeReasonCode;
  customReason?: string;
}): Promise<ChallengeResult> {
  const response = await fetch(`${API_BASE}/challenge`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      candidate_id: params.candidateId,
      original_score: params.originalScore,
      original_confidence: params.originalConfidence,
      reason_code: params.reasonCode,
      custom_reason: params.customReason ?? null
    })
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Challenge request failed");
  }

  return response.json();
}