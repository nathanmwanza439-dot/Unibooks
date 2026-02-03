"""
Example production settings for UniBooks.

Usage:
- Copy this file to `unibooks/settings_production.py` (do NOT commit secrets).
- Set the environment variable DJANGO_SETTINGS_MODULE to `unibooks.settings_production` when running the site.
- Ensure you set DJANGO_SECRET_KEY and other env vars described below.

This file imports all settings from the default `unibooks.settings` and overrides
security-sensitive values for production.

Important: never commit your real SECRET_KEY or credentials to source control.
"""

from .settings import *  # noqa: F401,F403
import os

# Require a SECRET_KEY from env in production
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # will KeyError if not set

# Disable debug in production
DEBUG = False

# Fill allowed hosts (space-separated) e.g. "unibooks.example.com www.unibooks.example.com"
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'yourdomain.example').split()

# Database: example using PostgreSQL. Set env vars appropriately.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'unibooks'),
        'USER': os.environ.get('POSTGRES_USER', 'unibooks'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Security (recommended)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static & media: in production serve via CDN / S3
# Example: configure django-storages with S3; below are placeholders
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email: configure SMTP or a transactional provider
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '1') == '1'
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'noreply@yourdomain')

# Logging: send errors to stderr and optionally to Sentry
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'WARNING'),
    },
}

# Additional advice:
# - Run `python manage.py collectstatic` during deploy
# - Use a process manager (gunicorn/uvicorn) behind a reverse proxy (nginx)
# - Configure backups for DB and MEDIA
# - Set environment variables securely (secrets manager, CI/CD pipeline)
