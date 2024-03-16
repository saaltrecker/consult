from celery import Celery

import environ

environ.Env.read_env(".env", overwrite=False)
env = environ.Env()
env("DJANGO_SETTINGS_MODULE")  # will raise if this is undefined

app = Celery("consultation_analyser")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
