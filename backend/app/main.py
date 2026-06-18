import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import activities, alignment, alerts, policies, observability
from .services import activity_service

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Watch API",
    description="AI oversight and governance platform API for monitoring agent actions.",
    version="2.0.0",
    openapi_tags=[
        {"name": "activities", "description": "Activity capture and management"},
        {"name": "policies", "description": "Policy engine — define and evaluate action policies"},
        {"name": "alerts", "description": "Alert engine — manage and query alerts"},
        {"name": "stats", "description": "Aggregate statistics"},
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

app.include_router(activities.router)
app.include_router(alignment.router)
app.include_router(alerts.router)
app.include_router(policies.router)
app.include_router(observability.router)


@app.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(get_db)):
    return activity_service.get_stats(db)


@app.get("/health", tags=["stats"])
def health():
    return {"status": "ok"}
