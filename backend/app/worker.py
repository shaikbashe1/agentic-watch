import asyncio
import asyncpg
import os
import json
from datetime import datetime
from app.core.celery_app import celery_app

POSTGRES_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://agentwatch:agentwatchpassword@localhost:5432/agentwatch"
)

async def _bulk_insert_events(events_data):
    """Async bulk insert into TimescaleDB using asyncpg."""
    # Convert string dates to datetime objects
    records = []
    for evt in events_data:
        try:
            started_at = datetime.fromisoformat(evt["started_at"].replace("Z", "+00:00"))
            ended_at = datetime.fromisoformat(evt["ended_at"].replace("Z", "+00:00")) if evt.get("ended_at") else None
            
            records.append((
                evt["id"],
                evt["workspace_id"],
                evt["trace_id"],
                evt["span_id"],
                evt.get("parent_span_id"),
                evt["session_id"],
                evt.get("agent_id"),
                evt["event_type"],
                evt["framework"],
                started_at,
                ended_at,
                evt.get("latency_ms"),
                evt.get("payload") and json.dumps(evt.get("payload"))
            ))
        except Exception as e:
            print(f"Skipping malformed event {evt.get('id')}: {e}")

    if not records:
        return

    conn = await asyncpg.connect(POSTGRES_URL)
    try:
        await conn.copy_records_to_table(
            "events",
            records=records,
            columns=[
                "id", "workspace_id", "trace_id", "span_id", "parent_span_id",
                "session_id", "agent_id", "event_type", "framework", 
                "started_at", "ended_at", "latency_ms", "payload"
            ]
        )
    finally:
        await conn.close()

@celery_app.task(name="ingest_batch_task", bind=True, max_retries=3)
def ingest_batch_task(self, events_data: list):
    """
    Celery task to take a batch of events from Redis and bulk insert them
    into TimescaleDB using asyncpg for extreme high throughput.
    """
    try:
        asyncio.run(_bulk_insert_events(events_data))
        return f"Successfully inserted {len(events_data)} events"
    except Exception as exc:
        # If DB is temporarily down, retry the task
        raise self.retry(exc=exc, countdown=5)
