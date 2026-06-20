from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.upload import router as upload_router
from backend.api.rank import router as rank_router
from backend.api.challenge import router as challenge_router
from backend.api.hidden_talent import router as hidden_talent_router

app = FastAPI(title="EVIDIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(rank_router)
app.include_router(challenge_router)
app.include_router(hidden_talent_router)

@app.get("/")
def home():
    return {
        "status":"running"
    }