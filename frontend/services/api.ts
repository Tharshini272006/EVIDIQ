export type Candidate = {
  id: number;
  rank?: number;
  name: string;
  filename: string;
  score: number;
  evidence: "Strong" | "Medium" | "Needs review" | string;
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
