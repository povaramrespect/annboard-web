from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import register_routers

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routers(app)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}









