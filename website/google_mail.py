"""
Google Apps Script Web App HTTPS Email Dispatcher for PKV Global Infotech
========================================================================
Sends emails via Google Apps Script Web App over HTTPS (Port 443).
Enables sending automated acknowledgments and notifications directly from
pkvglobalinfotech@gmail.com to any client email without SMTP port blocking.
"""
import json
import logging
import urllib.error
import urllib.request
from django.conf import settings

logger = logging.getLogger(__name__)

DEFAULT_GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwbUzny2SHZ53FWea3LQ3PzNWt_MT96LnQL5NyxMGxyn1e6O9wGZMtCWoW3YwlGY2_9hw/exec"


def send_google_mail(to, subject, body, name="PKV Global Infotech"):
    """
    Send an email via Google Apps Script Web App over HTTPS (port 443).
    Returns (success: bool, response_or_error: str).
    """
    script_url = getattr(settings, "GOOGLE_SCRIPT_URL", None) or DEFAULT_GOOGLE_SCRIPT_URL
    if not script_url:
        return False, "GOOGLE_SCRIPT_URL not configured"

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "name": name,
    }

    body_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        script_url,
        data=body_bytes,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "PKVGlobalInfotech/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp_text = resp.read().decode("utf-8")
            logger.info("Google Mail sent successfully via HTTPS to %s: %s", to, resp_text)
            return True, resp_text
    except Exception as exc:
        logger.error("Google Mail dispatch error to %s: %s", to, exc)
        return False, str(exc)
