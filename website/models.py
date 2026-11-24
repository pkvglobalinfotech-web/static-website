from django.db import models
from django.contrib.auth.models import User


# Company / Site Settings (Singleton)
class CompanySetting(models.Model):
    company_name = models.CharField(max_length=150, default="PKV Global Infotech Pvt Ltd")
    headline = models.CharField(max_length=200, default="Build Digital Products That Scale")
    supporting_text = models.TextField(
        default=(
            "PKV Global Infotech develops hospital software, HR applications, and multi-module ERP solutions. "
            "We also help businesses build and maintain websites, connect their software systems, and get ongoing IT support."
        )
    )
    email = models.EmailField(blank=True, default="contact@pkvglobalinfotech.com")
    phone = models.CharField(max_length=50, blank=True, default="+91 93455 96961", help_text="Official phone number.")
    address = models.TextField(blank=True, default="23(1)/190, puduchery, Pennaluripeta, Tiruvallur, Tiruvallur- 602026, Tamil Nadu")
    business_hours = models.CharField(max_length=100, blank=True, help_text="e.g. Mon–Fri 9am–6pm IST. Leave empty until confirmed.")

    # Social links - only shown if non-empty
    linkedin_url = models.URLField(blank=True, help_text="Company LinkedIn URL (leave empty if none)")
    twitter_url = models.URLField(blank=True, help_text="X / Twitter URL (leave empty if none)")
    github_url = models.URLField(blank=True, help_text="GitHub URL (leave empty if none)")
    facebook_url = models.URLField(blank=True, help_text="Facebook URL (leave empty if none)")
    instagram_url = models.URLField(blank=True, help_text="Instagram URL (leave empty if none)")
    youtube_url = models.URLField(blank=True, help_text="YouTube URL (leave empty if none)")

    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


# Services Section
class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi bi-code-slash")
    support_hours = models.CharField(
        max_length=120,
        blank=True,
        help_text="e.g. Mon–Fri 9:00 AM – 6:00 PM IST. Leave empty until confirmed."
    )
    response_commitment = models.CharField(
        max_length=120,
        blank=True,
        help_text="e.g. Response within 24 business hours. Leave empty until confirmed."
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lowest first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


# Products & Projects
class Project(models.Model):
    STAGE_CHOICES = [
        ('planning', 'Planned'),
        ('in_development', 'In Development'),
        ('ready_to_demo', 'Ready to Demonstrate'),
        ('live', 'Live / Available'),
    ]

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True, help_text="Short category or tagline")
    technology = models.CharField(max_length=150, blank=True)
    description = models.TextField(help_text="Product description and intended scope")
    modules = models.TextField(
        blank=True,
        help_text="Enter scope items or module names, one per line. Specify stage if helpful (e.g. 'Pharmacy Management - In Development')."
    )
    stage = models.CharField(
        max_length=30,
        choices=STAGE_CHOICES,
        default='in_development',
        help_text="Current development stage"
    )
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True, help_text="Optional screenshot or product visual")
    github = models.URLField(blank=True)
    live_demo = models.URLField(blank=True, help_text="Show 'View Demo' only when a working demo URL is supplied")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lowest first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Product / Project"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def get_modules_list(self):
        if not self.modules:
            return []
        return [m.strip() for m in self.modules.splitlines() if m.strip()]


# Blog CMS
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blogs/")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Testimonials (preserved in DB, hidden on public pages for new company)
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to="testimonial/", blank=True)

    def __str__(self):
        return self.name


# Contact Enquiries
class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    topic = models.CharField(
        max_length=150,
        default="General Enquiry",
        help_text="Product or Service enquiry topic"
    )
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    email_sent = models.BooleanField(
        default=False,
        help_text="Whether notification email was successfully dispatched"
    )
    email_error = models.TextField(
        blank=True,
        null=True,
        help_text="Details of email dispatch error, if any"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.topic} ({self.get_status_display()})"


# Newsletter
class Newsletter(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
