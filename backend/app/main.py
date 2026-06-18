import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import activities, alignment, alerts, policies, observability, ingestion
from .services import activity_service

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Watch B2B API",
    description="Multi-tenant Agent Observability Platform",
    version="3.0.0",
    openapi_tags=[
        {"name": "ingestion", "description": "Universal telemetry ingestion"},
        {"name": "observability", "description": "Observability and Execution Timeline"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router)
app.include_router(observability.router)


@app.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(get_db)):
    return activity_service.get_stats(db)


@app.get("/health", tags=["stats"])
def health():
    return {"status": "ok"}
