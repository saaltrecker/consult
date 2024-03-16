from celery import shared_task
from .services.process_consultation import ProcessConsultation


@shared_task
def process_consultation(consultation_id):
    return ProcessConsultation(consultation_id).run()
