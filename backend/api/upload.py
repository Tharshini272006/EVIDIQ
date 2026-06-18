from fastapi import APIRouter, UploadFile
import os

router = APIRouter()

UPLOAD_DIR="data/resumes"

os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload")

async def upload(file:UploadFile):

    path=f"{UPLOAD_DIR}/{file.filename}"

    with open(path,"wb") as f:
        f.write(await file.read())

    return {
        "uploaded":file.filename
    }
