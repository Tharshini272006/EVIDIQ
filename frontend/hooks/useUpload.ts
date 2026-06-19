"use client";

import { useState } from "react";
import { uploadCandidates, uploadJob } from "../services/api";

export function useUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function uploadFiles(jobFile: File | null, candidateFiles: FileList | null) {
    setIsUploading(true);
    setError(null);

    try {
      if (jobFile) {
        await uploadJob(jobFile);
      }

      if (candidateFiles?.length) {
        await uploadCandidates(candidateFiles);
      }
    } catch {
      setError("Upload failed");
      throw new Error("Upload failed");
    } finally {
      setIsUploading(false);
    }
  }

  return {
    error,
    isUploading,
    uploadFiles
  };
}
