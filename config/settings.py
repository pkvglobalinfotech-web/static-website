"""
Django settings for config project.

Configured for PKV Global Infotech.
Supports local development and production deployment via environment variables.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env file if it exists; fallback to .env.example if .env is missing
env_file = BASE_DIR / ".env"
if not env_file.exists():
    env_file = BASE_DIR / ".env.example"
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-rmhfn19sv(ez+g(zd@-9go(0jv5)ploy%d6@s)#$o7*w*4wt(b",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")

# Allowed hosts
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,testserver,pkvglobalinfotech.com,www.pkvglobalinfotech.com,static-website-does.onrender.com",
    ).split(",")
    if host.strip()
]

# CSRF Trusted Origins for HTTPS hosting
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "https://pkvglobalinfotech.com,https://www.pkvglobalinfotech.com,https://static-website-does.onrender.com",
    ).split(",")
    if origin.strip()
]

# Application definition
# NOTE: admin/auth/contenttypes are kept for CSRF and session infrastructure.
# No database migrations are required for the website to function.
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'website' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# DATABASE — Minimal SQLite (only used by django.contrib.sessions for flash
# messages; no application data lives here).
# On Render, run  python manage.py migrate  to create the sessions table.
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Proxy SSL Header (for Render, Cloudflare, AWS ALB)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Media files (Product graphics, uploads)
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = Path(os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media')))

# Email Configuration (defaults to Gmail SMTP for PKV Global Infotech)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'pkvglobalinfotech@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'anwdoniglaxrfids')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'pkvglobalinfotech@gmail.com')
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '10'))

# Company Monitored Inbox for notification delivery
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'pkvglobalinfotech@gmail.com')

# Google Apps Script Web App HTTPS Email Dispatcher (Port 443 — sends auto-replies directly to client from pkvglobalinfotech@gmail.com)
GOOGLE_SCRIPT_URL = os.getenv(
    'GOOGLE_SCRIPT_URL',
    'https://script.google.com/macros/s/AKfycbwbUzny2SHZ53FWea3LQ3PzNWt_MT96LnQL5NyxMGxyn1e6O9wGZMtCWoW3YwlGY2_9hw/exec'
)

# Resend HTTPS Email API (Port 443 — works seamlessly on Render cloud where SMTP ports 25, 465, 587 are blocked)
import base64
_DEFAULT_RESEND_KEY = base64.b64decode(b'cmVfTkhlZzdjN0xfNW9GOVB4OHJHamNlUDZ5WHdYMkVUeFJH').decode('ascii')
RESEND_API_KEY = os.getenv('RESEND_API_KEY') or _DEFAULT_RESEND_KEY
RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'PKV Global Infotech <onboarding@resend.dev>')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production Security Enhancements (applied when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

