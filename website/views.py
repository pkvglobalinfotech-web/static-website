


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import *
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages


def home(request):
    services = Service.objects.all()
    projects = Project.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = Blog.objects.all()
    # production: do not seed data here

    return render(
        request,
        "home.html",
        {
            "services": services,
            "projects": projects,
            "testimonials": testimonials,
            "blogs": blogs,
        },
    )


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def portfolio(request):
    projects = Project.objects.all()
    return render(request, "portfolio.html", {"projects": projects})


def blog(request):
    posts = Blog.objects.all()
    return render(request, "blog.html", {"posts": posts})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save()
            # Send notification email (console backend in dev)
            try:
                send_mail(
                    f"New contact from {contact.name}",
                    contact.message + "\n\nReply to: " + contact.email,
                    'no-reply@example.com',
                    ['hello@techstart.example'],
                    fail_silently=False,
                )
            except Exception:
                # don't break on email errors in dev
                pass

            messages.success(request, 'Thanks — your message was received.')
            return redirect("contact")

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def privacy(request):
    return render(request, "privacy.html")

def terms(request):
    return render(request, "terms.html")

@login_required
def dashboard(request):
    user_posts = Blog.objects.filter(author=request.user).order_by('-created')[:5]
    blog_count = user_posts.count()
    profile_name = request.user.get_full_name() or request.user.username

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "profile_name": profile_name,
            "blog_count": blog_count,
            "user_posts": user_posts,
        },
    )
