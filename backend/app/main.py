from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import activities, alignment
from .services import activity_service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Watch API",
    description="AI oversight and governance platform API for monitoring agent actions.",
    version="1.0.0"
)

app.include_router(activities.router)
app.include_router(alignment.router)

@app.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(get_db)):
    return activity_service.get_stats(db)
