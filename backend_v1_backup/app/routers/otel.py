from fastapi import APIRouter, Request, HTTPException
import logging

router = APIRouter(prefix="/otel/v1", tags=["OpenTelemetry"])

@router.post("/traces")
async def ingest_otlp_traces(request: Request):
    """
    Accepts standard OTLP/HTTP trace data.
    Allows standard OTEL agents to send telemetry directly to AgentWatch.
    """
    try:
        # In a real implementation we would parse the protobuf or JSON OTLP payload
        # payload = await request.body()
        return {"status": "accepted"}
    except Exception as e:
        logging.error(f"OTLP parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid OTLP format")
