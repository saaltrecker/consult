import sys

from django.utils.log import RequireDebugTrue

from consultation_analyser.settings.base import *  # noqa

INSTALLED_APPS.append("django_extensions")  # noqa F405
