from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AgentWatch Enterprise API",
    description="Real-time AI agent observability and governance platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheck(BaseModel):
    status: str
    version: str

@app.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="healthy", version="1.0.0")

from app.api.v1 import auth, ingest, governance

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Telemetry Ingestion"])
app.include_router(governance.router, prefix="/api/v1/governance", tags=["Active Governance"])

@app.get("/")
async def root():
    return {"message": "Welcome to AgentWatch Enterprise API. Visit /docs for the API reference."}
