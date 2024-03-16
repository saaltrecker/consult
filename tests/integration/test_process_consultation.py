import pytest

from tests.factories import ConsultationFactory
from consultation_analyser.consultations.models import Answer
from consultation_analyser.consultations.tasks import process_consultation


@pytest.mark.django_db(transaction=True)
def test_process_consultation(celery_worker):
    # given there's a consultation with a question and answer in the database
    consultation_to_process = ConsultationFactory(with_question=True, with_question__with_answer=True)
    answer_to_process = Answer.objects.filter(question__section__consultation_id=consultation_to_process.id).first()
    assert answer_to_process.theme is None

    # when I trigger processing (actual action TBD)
    assert process_consultation.delay(consultation_to_process.id).get() is True

    # then I should see a theme created for that question
    answer_to_process.refresh_from_db()  # this thread didn't know it changed
    assert answer_to_process.theme is not None
