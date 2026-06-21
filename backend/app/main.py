import asyncio
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.database import engine, Base, SessionLocal
from app.models.agent import Agent
from app.models.log import TelemetryLog

Base.metadata.create_all(bind=engine)

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

# Background Task to simulate active agents writing to database
async def telemetry_generator():
    db = SessionLocal()
    try:
        # Seed agents if empty
        if db.query(Agent).count() == 0:
            db.add_all([
                Agent(name="Research-Alpha", role="Deep Web Researcher", status="Processing", tokens="45.2k"),
                Agent(name="Coder-Bot-X", role="Frontend Developer", status="Idle", tokens="12.8k"),
                Agent(name="Data-Analyzer-01", role="Data Scientist", status="Processing", tokens="89.1k"),
                Agent(name="QA-Tester-Prime", role="Quality Assurance", status="Offline", tokens="0.0k"),
            ])
            db.commit()

        LOG_MESSAGES = [
            ("Executed Google Search API", "blue-400"),
            ("Parsed 4,200 tokens from top 3 results", "blue-400"),
            ("Invoked via IPC from Research-Alpha", "purple-400"),
            ("Editing frontend/src/app/page.tsx", "purple-400"),
            ("File saved successfully. HMR triggered", "green-400"),
            ("Idling...", "zinc-400"),
            ("Warning: High memory usage in Pandas frame", "yellow-400"),
            ("Garbage collection forced.", "blue-400"),
            ("Connected to Postgres Database", "green-400"),
            ("Generating embeddings for document chunk", "purple-400")
        ]
        
        while True:
            await asyncio.sleep(2)
            msg, color = random.choice(LOG_MESSAGES)
            agent_name = random.choice(["Research-Alpha", "Coder-Bot-X", "Data-Analyzer-01", "System"])
            
            new_log = TelemetryLog(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                agent=agent_name,
                message=msg,
                color=color
            )
            db.add(new_log)
            
            # Keep logs table small for POC
            if db.query(TelemetryLog).count() > 50:
                oldest = db.query(TelemetryLog).order_by(TelemetryLog.id.asc()).first()
                if oldest:
                    db.delete(oldest)
                    
            db.commit()
    except Exception as e:
        print(f"Generator error: {e}")
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_generator())

class HealthCheck(BaseModel):
    status: str
    version: str

@app.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="healthy", version="1.0.0")

from app.api.v1 import auth, ingest, governance, dashboard

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Telemetry Ingestion"])
app.include_router(governance.router, prefix="/api/v1/governance", tags=["Active Governance"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to AgentWatch Enterprise API. Visit /docs for the API reference."}
