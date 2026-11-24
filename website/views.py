from datetime import timedelta
import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Service, Project, Contact, CompanySetting
from .forms import ContactForm

logger = logging.getLogger(__name__)


def home(request):
    """
    Homepage showcasing:
    1. Introduction / Hero
    2. Products in Development
    3. IT Services
    4. Contact / Inquiry CTA
    """
    products = Project.objects.filter(is_active=True).order_by('order', 'id')
    services = Service.objects.filter(is_active=True).order_by('order', 'id')

    return render(
        request,
        "home.html",
        {
            "products": products,
            "services": services,
        },
    )


def products_view(request):
    """
    Product catalogue view.
    Preserves both /portfolio/ and /products/ URLs.
    """
    products = Project.objects.filter(is_active=True).order_by('order', 'id')
    return render(
        request,
        "portfolio.html",
        {
            "products": products,
            "projects": products,  # backwards-compatible context key
        },
    )


def services_view(request):
    """
    IT Services view showcasing active offerings and enquiry links.
    """
    services = Service.objects.filter(is_active=True).order_by('order', 'id')
    return render(
        request,
        "services.html",
        {
            "services": services,
        },
    )


def about(request):
    """About page for PKV Global Infotech."""
    return render(request, "about.html")


def contact(request):
    """
    Enquiry form handler.
    Pre-selects requested product or service topic from URL parameters.
    Saves enquiry to DB, attempts notification dispatch with Reply-To header,
    and logs any email failure while preserving database record.
    """
    selected_topic = (
        request.GET.get("topic")
        or request.GET.get("service")
        or request.GET.get("product")
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            topic = form.cleaned_data.get("topic")

            # Prevent duplicate submissions at the same time (within 60 seconds)
            one_minute_ago = timezone.now() - timedelta(seconds=60)
            if Contact.objects.filter(
                email__iexact=email,
                topic=topic,
                created__gte=one_minute_ago
            ).exists():
                logger.warning("Duplicate enquiry prevented for %s on topic %s", email, topic)
                messages.info(
                    request,
                    "Your enquiry has already been received. Our team will review your requirement and follow up shortly."
                )
                return redirect("contact")

            enquiry = form.save(commit=False)
            enquiry.status = "new"
            enquiry.save()

            # Attempt notification email with configured sender, company inbox, and visitor Reply-To
            recipient = getattr(settings, "NOTIFICATION_EMAIL", "pkvglobalinfotech@gmail.com")
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@pkvglobalinfotech.com")

            subject = f"[Website Enquiry] {enquiry.topic} from {enquiry.name}"
            body = (
                f"A new enquiry has been submitted on the PKV Global Infotech website:\n\n"
                f"Topic: {enquiry.topic}\n"
                f"Name: {enquiry.name}\n"
                f"Email: {enquiry.email}\n"
                f"Phone: {enquiry.phone or 'Not provided'}\n\n"
                f"Message:\n{enquiry.message}\n\n"
                f"--------------------------------------------------\n"
                f"Status: New\n"
                f"Submitted at: {enquiry.created}\n"
            )

            try:
                email_msg = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=from_email,
                    to=[recipient],
                    reply_to=[enquiry.email],
                )
                email_msg.send(fail_silently=False)
                enquiry.email_sent = True
                enquiry.email_error = None
            except Exception as e:
                logger.error("Failed to send enquiry notification email: %s", e)
                enquiry.email_sent = False
                enquiry.email_error = str(e)

            # Automated acknowledgment / auto-reply to the visitor's submitted email
            try:
                company_setting = CompanySetting.get_settings()
                company_email = company_setting.email or recipient
                company_phone = company_setting.phone or "+91 93455 96961"

                ack_subject = f"Thank you for contacting PKV Global Infotech - We've received your enquiry"
                ack_body = (
                    f"Dear {enquiry.name},\n\n"
                    f"Thank you for reaching out to PKV Global Infotech!\n\n"
                    f"We have received your enquiry regarding \"{enquiry.topic}\". "
                    f"Our team is reviewing your requirement and will reply to you shortly.\n\n"
                    f"--------------------------------------------------\n"
                    f"Summary of Your Submitted Details:\n"
                    f"Topic: {enquiry.topic}\n"
                    f"Phone: {enquiry.phone or 'Not provided'}\n\n"
                    f"Your Message:\n{enquiry.message}\n"
                    f"--------------------------------------------------\n\n"
                    f"If you have any clarifications, questions, or additional details to share, "
                    f"please feel free to reply directly to this email or reach us at:\n"
                    f"• Email: {company_email}\n"
                    f"• Phone: {company_phone}\n\n"
                    f"Best regards,\n"
                    f"PKV Global Infotech Team\n"
                    f"23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu\n"
                )

                ack_msg = EmailMessage(
                    subject=ack_subject,
                    body=ack_body,
                    from_email=from_email,
                    to=[enquiry.email],
                    reply_to=[company_email],
                )
                ack_msg.send(fail_silently=False)
            except Exception as e:
                logger.error("Failed to send auto-reply acknowledgment email to %s: %s", enquiry.email, e)

            enquiry.save()

            messages.success(
                request,
                "Thank you! Your enquiry has been received. Our team will review your requirement and follow up shortly."
            )
            return redirect("contact")
    else:
        form = ContactForm(initial_topic=selected_topic)

    return render(
        request,
        "contact.html",
        {
            "form": form,
            "selected_topic": selected_topic,
        },
    )


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")
