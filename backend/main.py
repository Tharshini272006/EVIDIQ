from fastapi import FastAPI
from backend.api.upload import router as upload_router
from backend.api.rank import router as rank_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(rank_router)

@app.get("/")
def home():
    return {
        "status":"running"
    }