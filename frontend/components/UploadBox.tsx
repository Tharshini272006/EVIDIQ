"use client";

import { type FormEvent, useRef } from "react";

type UploadBoxProps = {
  disabled?: boolean;
  onAnalyze: (jobFile: File | null, candidateFiles: FileList | null) => Promise<void>;
};

const pipelineSteps = [
  "Parsing",
  "Understanding Role",
  "Evaluating Evidence",
  "Ranking Candidates"
];

export default function UploadBox({ disabled = false, onAnalyze }: UploadBoxProps) {
  const jobInput = useRef<HTMLInputElement>(null);
  const candidateInput = useRef<HTMLInputElement>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await onAnalyze(
      jobInput.current?.files?.[0] ?? null,
      candidateInput.current?.files ?? null
    );
  }

  return (
    <section className="panel">
      <h2 className="panel-title">Upload</h2>

      <form className="upload-stack" onSubmit={handleSubmit}>
        <div className="upload-field">
          <label htmlFor="job-file">Job Description</label>
          <input id="job-file" ref={jobInput} type="file" accept=".txt,.pdf,.docx" />
        </div>

        <div className="upload-field">
          <label htmlFor="candidate-files">Candidate Dataset</label>
          <input
            id="candidate-files"
            multiple
            ref={candidateInput}
            type="file"
            accept=".pdf,.docx,.txt,.csv,.zip"
          />
        </div>

        <p className="microcopy">PDF / CSV / Resume ZIP</p>

        <button className="primary-button" disabled={disabled} type="submit">
          {disabled ? "Analyzing" : "Analyze"}
        </button>
      </form>

      <div className="pipeline" aria-label="Analysis pipeline">
        {pipelineSteps.map((step) => (
          <div className="pipeline-step" key={step}>
            {step}
          </div>
        ))}
      </div>
    </section>
  );
}
