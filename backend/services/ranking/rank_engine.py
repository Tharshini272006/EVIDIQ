from pathlib import Path

from backend.services.embeddings.generate_embeddings import embed
from backend.services.parser.resume_parser import parse_resume
from backend.services.ranking.batch_embed import batch_embed
from backend.services.scoring.candidate_score import similarity


RESUME_DIR = Path("data/resumes")
JOB_PATH = Path("data/jobs/job.txt")
SUPPORTED_RESUME_TYPES = {".pdf", ".docx", ".txt", ".md", ".csv"}


def _candidate_name(path: Path) -> str:
    cleaned = path.stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(cleaned.split()).title() or f"Candidate {path.name}"


def _evidence_label(score: int) -> str:
    if score >= 85:
        return "Strong"
    if score >= 70:
        return "Medium"
    return "Needs review"


def _load_job_text(job_path: Path = JOB_PATH) -> str:
    if not job_path.exists():
        return "Senior AI Engineer with Python, machine learning, embeddings, backend APIs, and production systems experience."

    return job_path.read_text(encoding="utf-8", errors="ignore").strip()


def _resume_files(resume_dir: Path = RESUME_DIR) -> list[Path]:
    if not resume_dir.exists():
        return []

    return sorted(
        path
        for path in resume_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_RESUME_TYPES
    )


def rank_candidates(top_k: int | None = None) -> list[dict]:
    job_text = _load_job_text()
    resume_files = _resume_files()

    if not job_text or not resume_files:
        return []

    parsed_candidates = [
        {
            "id": index,
            "name": _candidate_name(path),
            "filename": path.name,
            "text": parse_resume(path),
        }
        for index, path in enumerate(resume_files, start=1)
    ]

    job_vector = embed(job_text)
    candidate_vectors = batch_embed([candidate["text"] for candidate in parsed_candidates])

    ranked = []
    for candidate, candidate_vector in zip(parsed_candidates, candidate_vectors):
        score = int(round(float(similarity(candidate_vector, job_vector)) * 100))
        score = max(0, min(score, 100))

        ranked.append(
            {
                "id": candidate["id"],
                "name": candidate["name"],
                "filename": candidate["filename"],
                "score": score,
                "evidence": _evidence_label(score),
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)

    for rank, candidate in enumerate(ranked, start=1):
        candidate["rank"] = rank

    if top_k is not None:
        return ranked[:top_k]

    return ranked
