from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

router = APIRouter()

UPLOAD_DIR = Path("data/resumes")
JOB_DIR = Path("data/jobs")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
JOB_DIR.mkdir(parents=True, exist_ok=True)


async def _save_upload(upload: UploadFile, directory: Path, filename: str | None = None) -> dict:
    filename = Path(filename or upload.filename or "candidate.txt").name
    path = directory / filename

    content = await upload.read()
    if not content:
        raise HTTPException(status_code=400, detail=f"{filename} is empty.")

    path.write_bytes(content)

    return {
        "filename": filename,
        "path": str(path),
        "bytes": len(content),
    }


@router.post("/upload")
async def upload(request: Request):
    form = await request.form()
    files = [
        value
        for _, value in form.multi_items()
        if isinstance(value, StarletteUploadFile)
    ]

    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one resume file.")

    uploaded = [await _save_upload(file, UPLOAD_DIR) for file in files]
    return {
        "count": len(uploaded),
        "uploaded": uploaded,
    }


@router.post("/upload/job")
async def upload_job(file: UploadFile):
    saved = await _save_upload(file, JOB_DIR, filename="job.txt")

    return {
        "uploaded": saved["filename"],
        "active_job": saved["path"],
    }
