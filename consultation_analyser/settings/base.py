"""
Django settings for consultation_analyser project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import logging
import os
import sys
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=False)

env = environ.Env(DEBUG=(bool, False))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ENVIRONMENT = env("ENVIRONMENT")


ALLOWED_HOSTS: list[str] = [os.getenv("DOMAIN_NAME", "0.0.0.0"), "*"]  # nosec

# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.admin",
    "waffle",  # feature flags
    "magic_link",
    "consultation_analyser.authentication",
    "consultation_analyser.consultations",
    "consultation_analyser.support_console",
    "consultation_analyser.error_pages",
    "consultation_analyser.email",
    "compressor",
    "crispy_forms",
    "crispy_forms_gds",
    "django.contrib.humanize",
]


# TODO: steal code from this blog post to add a health check endpoint: https://testdriven.io/blog/deploying-django-to-ecs-with-terraform/#django-health-check

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "waffle.middleware.WaffleMiddleware",
]

ROOT_URLCONF = "consultation_analyser.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "consultation_analyser.jinja2.environment",
            "context_processors": [
                "consultation_analyser.context_processors.app_config",
                "consultation_analyser.context_processors.version",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [BASE_DIR / "consultation_analyser/templates"],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ]
        },
    },
]

WSGI_APPLICATION = "consultation_analyser.wsgi.application"

AUTH_USER_MODEL = "authentication.User"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATIC_URL = "static/"
STATIC_ROOT = "frontend/"
STATICFILES_DIRS = [
    ("govuk-assets", BASE_DIR / "node_modules/govuk-frontend/dist/govuk/assets"),
    ("iai-assets", BASE_DIR / "node_modules/i.ai-design-system/dist/"),
]
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "pipeline": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "pipeline",
        }
    },
    "loggers": {
        "pipeline": {"handlers": ["stdout"], "level": "INFO", "propagate": False},
        "upload": {"handlers": ["stdout"], "level": "INFO", "propagate": False},
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django URL format
APPEND_SLASH = True

# Feature flags
WAFFLE_SWITCH_DEFAULT = False
WAFFLE_CREATE_MISSING_SWITCHES = True
WAFFLE_LOG_MISSING_SWITCHES = logging.INFO

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "gds"
CRISPY_TEMPLATE_PACK = "gds"

# Email
EMAIL_BACKEND = "django_gov_notify.backends.NotifyEmailBackend"
GOVUK_NOTIFY_API_KEY = env("GOVUK_NOTIFY_API_KEY")
GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID = env("GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID")

# AWS variables
BATCH_JOB_QUEUE = env("BATCH_JOB_QUEUE", default=None)
BATCH_JOB_DEFINITION = env("BATCH_JOB_DEFINITION", default=None)
AWS_REGION = env("AWS_REGION")

# ML pipeline
LLM_BACKEND = env("LLM_BACKEND")
BERTOPIC_DEFAULT_EMBEDDING_MODEL = "thenlper/gte-small"

# Authentication
LOGIN_URL = "/sign-in/"

# version info
GIT_SHA = env("GIT_SHA", default=None)
