import httpx
import logging
import json
import hmac
import hashlib
import time
from sqlalchemy.orm import Session
from ..models.webhooks import Webhook

logger = logging.getLogger(__name__)

class WebhookService:
    @staticmethod
    async def dispatch(webhooks: list, event_type: str, payload: dict):
        """
        Dispatch the event payload asynchronously to a list of webhooks.
        `webhooks` should be a list of objects with `url` and `secret`.
        """
        try:
            if not webhooks:
                return

            # Construct the final webhook payload
            webhook_payload = {
                "event_type": event_type,
                "timestamp": int(time.time()),
                "data": payload
            }
            body = json.dumps(webhook_payload).encode("utf-8")

            # Fire off HTTP POST requests using async httpx client
            async with httpx.AsyncClient(timeout=5.0) as client:
                for wh in webhooks:
                    try:
                        # Generate HMAC signature if secret is provided
                        headers = {"Content-Type": "application/json"}
                        if wh.secret:
                            signature = hmac.new(
                                wh.secret.encode("utf-8"), 
                                body, 
                                hashlib.sha256
                            ).hexdigest()
                            headers["X-AgentWatch-Signature"] = f"sha256={signature}"

                        response = await client.post(
                            wh.url,
                            content=body,
                            headers=headers
                        )
                        logger.info(f"Webhook dispatched to {wh.url} (Status: {response.status_code})")
                    except Exception as e:
                        logger.error(f"Failed to dispatch webhook to {wh.url}: {e}")
        except Exception as e:
            logger.error(f"Error in WebhookService.dispatch: {e}")
