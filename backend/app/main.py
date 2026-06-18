import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import activities, alignment, alerts, policies, observability, ingestion, auth, team, keys
from .services import activity_service
from .websockets import manager
from jose import jwt, JWTError
from .services.auth_service import SECRET_KEY, ALGORITHM
from fastapi import WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Watch B2B API",
    description="Multi-tenant Agent Observability Platform",
    version="3.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication and Account Creation"},
        {"name": "team", "description": "Team & RBAC Management"},
        {"name": "keys", "description": "API Keys and Agent Registration"},
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

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        company_id = payload.get("company_id")
        if not company_id:
            await websocket.close(code=1008)
            return
            
        await manager.connect(websocket, company_id)
        try:
            while True:
                data = await websocket.receive_text()
                # We don't really expect to receive data from dashboard, just push to it
        except WebSocketDisconnect:
            manager.disconnect(websocket, company_id)
    except JWTError:
        await websocket.close(code=1008)

app.include_router(auth.router)
app.include_router(team.router)
app.include_router(keys.router)
app.include_router(ingestion.router)
app.include_router(observability.router)


@app.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(get_db)):
    return activity_service.get_stats(db)


@app.get("/health", tags=["stats"])
def health():
    return {"status": "ok"}
