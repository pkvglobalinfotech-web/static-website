"""
Resend HTTPS Email Dispatcher for PKV Global Infotech
======================================================
Sends emails via Resend's REST API over HTTPS (Port 443).
Since Render Free Tier blocks outbound SMTP (ports 25, 465, 587),
this module ensures 100% reliable email delivery from Render cloud.
Uses Python's standard library (urllib.request) — zero external dependencies.
"""
import json
import logging
import urllib.error
import urllib.request
from django.conf import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


def send_resend_email(to, subject, text, reply_to=None, from_email=None, html=None):
    """
    Send an email via Resend's HTTPS API (port 443).
    Returns (success: bool, response_or_error: str).
    """
    api_key = getattr(settings, "RESEND_API_KEY", None)
    if not api_key:
        logger.warning("RESEND_API_KEY is not configured; skipping Resend email.")
        return False, "RESEND_API_KEY not configured"

    if isinstance(to, str):
        to = [to]

    sender = from_email or getattr(
        settings, "RESEND_FROM_EMAIL", "PKV Global Infotech <onboarding@resend.dev>"
    )

    payload = {
        "from": sender,
        "to": to,
        "subject": subject,
        "text": text,
    }

    if reply_to:
        payload["reply_to"] = reply_to
    if html:
        payload["html"] = html

    body_bytes = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        RESEND_API_URL,
        data=body_bytes,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "PKVGlobalInfotech/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp_body = resp.read().decode("utf-8")
            logger.info("Resend email sent successfully to %s: %s", to, resp_body)
            return True, resp_body
    except urllib.error.HTTPError as exc:
        err_msg = exc.read().decode("utf-8")
        logger.error("Resend HTTPError (%s): %s", exc.code, err_msg)
        return False, f"HTTP {exc.code}: {err_msg}"
    except Exception as exc:
        logger.error("Resend network error: %s", exc)
        return False, str(exc)
