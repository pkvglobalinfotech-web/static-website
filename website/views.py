"""
PKV Global Infotech — Views
All data comes from website/static_data.py (no database needed).
Enquiry submissions are sent as email only.
"""
import logging
import threading
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from .forms import ContactForm
from .static_data import COMPANY, get_active_products, get_active_services
from .resend_client import send_resend_email

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------

def home(request):
    return render(request, "home.html", {
        "products": get_active_products(),
        "services": get_active_services(),
    })


def products_view(request):
    products = get_active_products()
    return render(request, "portfolio.html", {
        "products": products,
        "projects": products,          # backwards-compatible key
    })


def services_view(request):
    return render(request, "services.html", {
        "services": get_active_services(),
    })


def about(request):
    return render(request, "about.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")


# ---------------------------------------------------------------------------
# EMAIL HELPERS
# ---------------------------------------------------------------------------

def _send_enquiry_emails(data: dict):
    """
    Send emails in a background thread:
      1. Staff notification to pkvglobalinfotech@gmail.com
      2. Auto-reply acknowledgment to the visitor

    Uses Resend HTTPS API (Port 443) first, which works 100% reliably on Render
    cloud where outbound SMTP ports (25, 465, 587) are blocked.
    Falls back to Django SMTP if Resend is not configured or fails.
    """
    recipient = getattr(settings, "NOTIFICATION_EMAIL", COMPANY["email"])
    from_email = (
        getattr(settings, "DEFAULT_FROM_EMAIL", None)
        or getattr(settings, "EMAIL_HOST_USER", None)
        or COMPANY["email"]
    )

    subject = f"New Enquiry: {data['topic']} — {data['name']}"
    body = (
        f"You have received a new enquiry from the PKV Global Infotech website:\n\n"
        f"Name:    {data['name']}\n"
        f"Email:   {data['email']}\n"
        f"Phone:   {data.get('phone') or 'Not provided'}\n"
        f"Topic:   {data['topic']}\n\n"
        f"Message:\n{data['message']}\n\n"
        f"---\n"
        f"Submitted on: {data.get('submitted_at', '')}\n"
    )

    # 1 — Staff notification (Resend HTTPS first, then fallback to SMTP)
    staff_sent = False
    if getattr(settings, "RESEND_API_KEY", None):
        success, res = send_resend_email(
            to=recipient,
            subject=subject,
            text=body,
            reply_to=data["email"],
        )
        if success:
            staff_sent = True
            logger.info("Enquiry notification delivered via Resend HTTPS to %s", recipient)
        else:
            logger.warning("Resend HTTPS notification failed (%s); trying fallback SMTP", res)

    if not staff_sent:
        try:
            EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[recipient],
                reply_to=[data["email"]],
            ).send(fail_silently=False)
            logger.info("Enquiry notification sent via fallback SMTP to %s", recipient)
        except Exception as exc:
            logger.error("Failed to send enquiry notification via SMTP: %s", exc)

    # 2 — Auto-reply to visitor (SMTP if available; Resend if verified domain)
    ack_subject = "Thank you for contacting PKV Global Infotech — We've received your enquiry"
    ack_body = (
        f"Dear {data['name']},\n\n"
        f"Thank you for reaching out to PKV Global Infotech!\n\n"
        f"We have received your enquiry regarding \"{data['topic']}\". "
        f"Our team is reviewing your requirement and will reply to you shortly.\n\n"
        f"--------------------------------------------------\n"
        f"Summary of Your Submitted Details:\n"
        f"Topic:   {data['topic']}\n"
        f"Phone:   {data.get('phone') or 'Not provided'}\n\n"
        f"Your Message:\n{data['message']}\n"
        f"--------------------------------------------------\n\n"
        f"If you have any clarifications or additional details to share, please "
        f"feel free to reply to this email or reach us at:\n"
        f"  • Email: {COMPANY['email']}\n"
        f"  • Phone: {COMPANY['phone']}\n\n"
        f"Best regards,\n"
        f"PKV Global Infotech Team\n"
        f"{COMPANY['address']}\n"
    )

    # Attempt visitor auto-reply via Resend HTTPS
    visitor_sent = False
    if getattr(settings, "RESEND_API_KEY", None):
        success, res = send_resend_email(
            to=data["email"],
            subject=ack_subject,
            text=ack_body,
            reply_to=COMPANY["email"],
        )
        if success:
            visitor_sent = True
            logger.info("Auto-reply delivered via Resend HTTPS to %s", data["email"])
        else:
            logger.debug("Resend auto-reply to %s skipped or not allowed on test domain: %s", data["email"], res)

    if not visitor_sent:
        try:
            EmailMessage(
                subject=ack_subject,
                body=ack_body,
                from_email=from_email,
                to=[data["email"]],
                reply_to=[COMPANY["email"]],
            ).send(fail_silently=True)
            logger.info("Auto-reply sent via SMTP to %s", data["email"])
        except Exception as exc:
            logger.debug("Auto-reply via SMTP skipped: %s", exc)



# ---------------------------------------------------------------------------
# CONTACT VIEW
# ---------------------------------------------------------------------------

def contact(request):
    """
    Enquiry form — no database.
    On valid POST: immediately shows success message, dispatches emails in background.
    """
    selected_topic = (
        request.GET.get("topic")
        or request.GET.get("service")
        or request.GET.get("product")
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["submitted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

            # Fire emails in a non-blocking background thread
            threading.Thread(
                target=_send_enquiry_emails,
                args=(dict(data),),
                daemon=True,
            ).start()

            messages.success(
                request,
                "Thank you! Your enquiry has been received. "
                "Our team will review your requirement and follow up shortly.",
            )
            return redirect("contact")
    else:
        form = ContactForm(initial_topic=selected_topic)

    return render(request, "contact.html", {
        "form": form,
        "selected_topic": selected_topic,
    })
