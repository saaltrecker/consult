from dataclasses import dataclass
import pytest
from urllib.parse import urlencode

from consultation_analyser.factories import ConsultationBuilder, UserFactory
from consultation_analyser.consultations import models
from consultation_analyser.authentication.models import User


@dataclass
class QuestionForFiltering:
    user: User
    question_url: str
    responses_url: str
    answer1: models.Answer
    answer2: models.Answer
    theme1: models.Theme
    theme2: models.Theme


@pytest.fixture
def question_for_filtering():
    user = UserFactory()

    consultation_builder = ConsultationBuilder(user=user)
    question = consultation_builder.add_question()
    section = consultation_builder.get_section()

    answer1 = consultation_builder.add_answer(question, free_text="I love bunnies")
    theme1 = consultation_builder.add_theme(answer1, short_description="bunny theme")

    answer2 = consultation_builder.add_answer(question, free_text="I love kittens")
    theme2 = consultation_builder.add_theme(answer2, short_description="kitten theme")

    question_url = f"/consultations/{consultation_builder.consultation.slug}/sections/{section.slug}/questions/{question.slug}/"
    responses_url = f"/consultations/{consultation_builder.consultation.slug}/sections/{section.slug}/responses/{question.slug}/"

    return QuestionForFiltering(
        user=user,
        question_url=question_url,
        responses_url=responses_url,
        answer1=answer1,
        answer2=answer2,
        theme1=theme1,
        theme2=theme2,
    )


@pytest.mark.django_db
def test_filter_by_theme(client, question_for_filtering):
    client.force_login(question_for_filtering.user)

    page = str(client.get(question_for_filtering.question_url).content)

    # No filters applied
    assert "bunny theme" in page
    assert "kitten theme" in page

    # Filter by theme 1
    filter_theme1 = urlencode({"theme": question_for_filtering.theme1.id})

    page = str(client.get(f"{question_for_filtering.question_url}?{filter_theme1}").content)

    assert "bunny theme" in page
    assert "kitten theme" not in page


@pytest.mark.django_db
def test_filter_responses_by_keyword(client, question_for_filtering):
    client.force_login(question_for_filtering.user)

    page = str(client.get(question_for_filtering.responses_url).content)

    assert "I love bunnies" in page
    assert "I love kittens" in page

    filter = urlencode({"keyword": "bunnies"})

    page = str(client.get(f"{question_for_filtering.responses_url}?{filter}").content)

    assert "I love bunnies" in page
    assert "I love kittens" not in page

    filter = urlencode({"keyword": "micropigs"})

    page = str(client.get(f"{question_for_filtering.responses_url}?{filter}").content)

    assert "I love bunnies" not in page
    assert "I love kittens" not in page


@pytest.mark.django_db
def test_filter_responses_by_theme(client, question_for_filtering):
    client.force_login(question_for_filtering.user)

    filter_theme1 = urlencode({"theme": question_for_filtering.theme1.id})

    page = str(client.get(f"{question_for_filtering.responses_url}?{filter_theme1}").content)

    assert "I love bunnies" in page
    assert "I love kittens" not in page
