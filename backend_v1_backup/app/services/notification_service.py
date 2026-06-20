import logging
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import httpx
from ..core.config import settings

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=4)


def _send_email_sync(to_email: str, subject: str, body: str) -> bool:
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured; skipping email notification")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
        msg["To"] = to_email
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg["From"], [to_email], msg.as_string())
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}")
        return False


def send_email_async(to_email: str, subject: str, body: str) -> None:
    _executor.submit(_send_email_sync, to_email, subject, body)


def send_webhook(url: str, payload: dict, retries: int = 3, backoff: float = 1.0) -> bool:
    if not url:
        return False
    for attempt in range(1, retries + 1):
        try:
            response = httpx.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Webhook delivered to {url}")
            return True
        except Exception as exc:
            logger.warning(f"Webhook attempt {attempt}/{retries} to {url} failed: {exc}")
            if attempt < retries:
                time.sleep(backoff * attempt)
    logger.error(f"Webhook permanently failed after {retries} attempts: {url}")
    return False


def notify_alert(alert_title: str, alert_description: str, severity: str, activity_id: Optional[int]) -> None:
    subject = f"[AgenticWatch] {severity.upper()} Alert: {alert_title}"
    body = (
        f"Alert: {alert_title}\n"
        f"Severity: {severity}\n"
        f"Description: {alert_description or 'N/A'}\n"
        f"Activity ID: {activity_id or 'N/A'}\n"
    )
    if settings.ALERT_EMAIL_TO:
        send_email_async(settings.ALERT_EMAIL_TO, subject, body)
    if settings.WEBHOOK_URL:
        payload = {
            "title": alert_title,
            "description": alert_description,
            "severity": severity,
            "activity_id": activity_id,
        }
        _executor.submit(send_webhook, settings.WEBHOOK_URL, payload)
