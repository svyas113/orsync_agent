"""Send demo-request notifications to the Or-sync inbox."""

from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import EmailMessage

import fastworkflow


DEFAULT_TO = "orsyncagents@gmail.com"


@dataclass
class DemoLead:
    name: str
    email: str
    company: str = ""
    message: str = ""
    interest: str = "general demo"


@dataclass
class EmailResult:
    ok: bool
    detail: str


def _env(name: str, default: str = "") -> str:
    """Read from FastWorkflow env (loaded from .env files) then os.environ."""
    try:
        value = fastworkflow.get_env_var(name, default=None)
        if value is not None and str(value).strip():
            return str(value).strip()
    except Exception:
        pass
    return (os.environ.get(name) or default).strip()


def _smtp_settings() -> dict[str, str | int]:
    return {
        "host": _env("SMTP_HOST", "smtp.gmail.com"),
        "port": int(_env("SMTP_PORT", "587") or "587"),
        "user": _env("SMTP_USER"),
        "password": _env("SMTP_PASSWORD"),
        "to": _env("DEMO_REQUEST_TO", DEFAULT_TO),
        "from_addr": _env("SMTP_FROM") or _env("SMTP_USER") or DEFAULT_TO,
    }


def send_demo_request_email(lead: DemoLead) -> EmailResult:
    """Email the demo lead to orsyncagents@gmail.com (or DEMO_REQUEST_TO)."""
    settings = _smtp_settings()
    if not settings["user"] or not settings["password"]:
        return EmailResult(
            ok=False,
            detail=(
                "Email is not configured yet (missing SMTP_USER / SMTP_PASSWORD). "
                "Please email orsyncagents@gmail.com directly, or try again later."
            ),
        )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = (
        "New demo request from the Or-sync website visitor agent.\n\n"
        f"Name: {lead.name}\n"
        f"Email: {lead.email}\n"
        f"Company: {lead.company or '(not provided)'}\n"
        f"Interest: {lead.interest}\n"
        f"Message: {lead.message or '(not provided)'}\n"
        f"Received: {stamp}\n"
    )

    msg = EmailMessage()
    msg["Subject"] = f"Website agent — demo request from {lead.name}"
    msg["From"] = str(settings["from_addr"])
    msg["To"] = str(settings["to"])
    msg["Reply-To"] = lead.email
    msg.set_content(body)

    try:
        with smtplib.SMTP(str(settings["host"]), int(settings["port"]), timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(str(settings["user"]), str(settings["password"]))
            smtp.send_message(msg)
    except Exception as exc:  # noqa: BLE001 — surface failure to the chat user
        return EmailResult(
            ok=False,
            detail=(
                f"Could not send the demo request email ({exc}). "
                "Please email orsyncagents@gmail.com directly."
            ),
        )

    return EmailResult(
        ok=True,
        detail=(
            f"Thanks {lead.name}! I notified the Or-sync team at {settings['to']}. "
            "Someone will follow up within about 24 hours."
        ),
    )
