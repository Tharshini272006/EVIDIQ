from fastapi import APIRouter
from backend.services.parser.resume_parser import parse_resume
from backend.services.embeddings.generate_embeddings import embed
from backend.services.scoring.candidate_score import similarity

router = APIRouter()


@router.get("/rank")

def rank():

    resume = parse_resume(
        r"data/resumes/THARSHINI.resume (2).pdf"
    )

    with open(r"data/jobs/job.txt",
encoding="utf-8" ) as f:

     job = f.read()

    resume_vec = embed(resume)

    job_vec = embed(job)

    score = similarity(
        resume_vec,
        job_vec
    )

    return {
        "score": float(score)
    }