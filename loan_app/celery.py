import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loan_app.settings")
app = Celery("loan_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
