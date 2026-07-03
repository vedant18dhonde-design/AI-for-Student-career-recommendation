"""Email utility — logs to console when SMTP is disabled."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.config.settings import settings

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, body_html: str) -> bool:
    """Send an email or log it to console based on EMAIL_ENABLED setting."""
    if not settings.EMAIL_ENABLED:
        logger.info(
            "📧 [EMAIL CONSOLE LOG]\nTo: %s\nSubject: %s\nBody:\n%s",
            to, subject, body_html,
        )
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to, msg.as_string())

        logger.info("✅ Email sent to %s", to)
        return True
    except Exception as exc:
        logger.error("❌ Failed to send email to %s: %s", to, exc)
        return False


async def send_password_reset_email(to: str, reset_token: str) -> bool:
    reset_url = f"http://localhost:5173/reset-password?token={reset_token}"
    subject = "Password Reset — AI Career Platform"
    body = f"""
    <h2>Password Reset Request</h2>
    <p>Click the link below to reset your password. This link expires in
    {settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes.</p>
    <a href="{reset_url}" style="background:#6366f1;color:#fff;padding:12px 24px;
    border-radius:8px;text-decoration:none;">Reset Password</a>
    <p>If you did not request this, please ignore this email.</p>
    """
    return await send_email(to, subject, body)


async def send_welcome_email(to: str, name: str) -> bool:
    subject = "Welcome to AI Student Career Analysis Platform!"
    body = f"""
    <h2>Welcome, {name}! 🎓</h2>
    <p>Your account has been created successfully.</p>
    <p>You can now access career recommendations, salary predictions, and more.</p>
    <a href="http://localhost:5173/login" style="background:#6366f1;color:#fff;
    padding:12px 24px;border-radius:8px;text-decoration:none;">Get Started</a>
    """
    return await send_email(to, subject, body)
