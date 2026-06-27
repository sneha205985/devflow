from app.workers.celery_app import celery_app
from app.core.config import settings


@celery_app.task
def send_verification_email(email: str, token: str) -> str:
    link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    # TODO: wire real SMTP. For now log to worker stdout.
    print(f"[EMAIL] verify -> {email}: {link}")
    return email


@celery_app.task
def send_notification_email(email: str, subject: str, body: str) -> str:
    print(f"[EMAIL] {subject} -> {email}: {body}")
    return email
