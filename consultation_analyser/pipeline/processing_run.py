from uuid import UUID
import logging
from datetime import datetime

from consultation_analyser.consultations import models
from consultation_analyser.consultations.public_schema import ProcessingRunMetadata

from .backends.types import ThemeSummary
from .backends.topic_backend import TopicBackend
from .backends.llm_backend import LLMBackend

logger = logging.getLogger("pipeline")


class ProcessingRun:
    def __init__(self, topic_backend: TopicBackend, llm_backend: LLMBackend):
        self.topic_backend = topic_backend
        self.llm_backend = llm_backend
        self.started_at = None
        self.completed_at = None

    def metadata(self):
        metadata = {
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "topic_model": self.topic_backend.metadata(),
            "llm": self.llm_backend.metadata(),
        }

    def run(self, consultation: models.Consultation):
        self.started_at = datetime.now()
        self.__save_themes_for_consultation(consultation.id, self.topic_backend)
        self.__create_llm_summaries_for_consultation(consultation, self.llm_backend)
        self.completed_at = datetime.now()

    def __save_themes_for_question(
        self, question: models.Question, topic_backend: TopicBackend
    ) -> None:
        logging.info(f"Get topics for question: {question.text}")
        assignments = topic_backend.get_topics(question)

        for assignment in assignments:
            assignment.answer.save_theme_to_answer(
                topic_keywords=assignment.topic_keywords, topic_id=assignment.topic_id
            )

    def __save_themes_for_consultation(
        self, consultation_id: UUID, topic_backend: TopicBackend
    ) -> None:
        logging.info(f"Starting topic modelling for consultation_id: {consultation_id}")
        questions = models.Question.objects.filter(
            section__consultation__id=consultation_id, has_free_text=True
        )

        for question in questions:
            self.__save_themes_for_question(question, topic_backend=topic_backend)

    def __create_llm_summaries_for_consultation(self, consultation, llm_backend: LLMBackend):
        logger.info(
            f"Starting LLM summarisation for consultation: {consultation.name} with backend {llm_backend.__class__.__name__}"
        )
        themes = models.Theme.objects.filter(question__section__consultation=consultation).filter(
            question__has_free_text=True
        )

        theme: ThemeSummary
        for theme in themes:
            logger.info(
                f"Starting LLM summarisation for theme with keywords: {theme.topic_keywords}"
            )
            theme_summary_data = llm_backend.summarise_theme(theme)
            theme.summary = theme_summary_data.summary
            theme.short_description = theme_summary_data.short_description
            logger.info(f"Theme description: {theme.short_description}")
            theme.save()
