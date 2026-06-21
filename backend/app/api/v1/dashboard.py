from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

router = APIRouter()

class Metric(BaseModel):
    label: str
    value: str
    change: str
    trend: str

class Agent(BaseModel):
    name: str
    role: str
    status: str
    tokens: str

class LogEntry(BaseModel):
    timestamp: str
    agent: str
    message: str
    color: str

@router.get("/metrics", response_model=List[Metric])
async def get_metrics():
    # Simulate slightly shifting numbers
    base_tasks = 8400 + random.randint(0, 100)
    error_rate = 0.04 + (random.randint(-1, 2) / 100.0)
    
    return [
        {"label": "Active Agents", "value": str(random.randint(10, 15)), "change": "+2", "trend": "up"},
        {"label": "Tasks Processed (24h)", "value": f"{base_tasks:,}", "change": "+14%", "trend": "up"},
        {"label": "System Error Rate", "value": f"{error_rate:.2f}%", "change": "-0.01%", "trend": "down"},
    ]

@router.get("/agents", response_model=List[Agent])
async def get_agents():
    statuses = ["Processing", "Idle", "Offline"]
    
    return [
        {"name": "Research-Alpha", "role": "Deep Web Researcher", "status": random.choices(statuses, weights=[70, 20, 10])[0], "tokens": f"{random.uniform(40, 50):.1f}k"},
        {"name": "Coder-Bot-X", "role": "Frontend Developer", "status": random.choices(statuses, weights=[30, 60, 10])[0], "tokens": f"{random.uniform(10, 20):.1f}k"},
        {"name": "Data-Analyzer-01", "role": "Data Scientist", "status": random.choices(statuses, weights=[80, 10, 10])[0], "tokens": f"{random.uniform(80, 95):.1f}k"},
        {"name": "QA-Tester-Prime", "role": "Quality Assurance", "status": random.choices(statuses, weights=[10, 30, 60])[0], "tokens": f"{random.uniform(0, 5):.1f}k"},
    ]

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

AGENTS = ["Research-Alpha", "Coder-Bot-X", "Data-Analyzer-01", "System"]

@router.get("/logs", response_model=List[LogEntry])
async def get_logs():
    logs = []
    now = datetime.now()
    # Generate 8 random logs
    for i in range(8):
        msg, color = random.choice(LOG_MESSAGES)
        agent = random.choice(AGENTS)
        time_str = now.strftime("%H:%M:%S")
        logs.append({
            "timestamp": time_str,
            "agent": agent,
            "message": msg,
            "color": color
        })
    return logs
