import logging

from consultation_analyser.consultations import models

from .backends.topic_backend import TopicBackend
from .backends.types import TopicAssignment
from .processing import summarise_with_llm

logger = logging.getLogger("pipeline")


def topic_assignment_to_dict(assignment: TopicAssignment) -> dict[str, str | int | float]:
    output = {
        "answer_id": str(assignment.answer.id),
        "answer_free_text": assignment.answer.free_text,
        "topic_id": assignment.topic_id,
        "x_coordinate": assignment.x_coordinate,
        "y_coordinate": assignment.y_coordinate,
    }
    return output


def get_scatter_plot_data(assignments: list[TopicAssignment]) -> dict[str, list]:
    scatter_plot_coords = [topic_assignment_to_dict(assignment) for assignment in assignments]
    scatter_plot_data = {"data": scatter_plot_coords}
    return scatter_plot_data


def save_themes_for_question(
    question: models.Question,
    topic_backend: TopicBackend,
    processing_run: models.ProcessingRun,
    llm_backend
) -> None:
    logging.info(f"Get topics for question: {question.text}")
    assignments = topic_backend.get_topics(question)

    # Get LLM summary for theme (needs consultation)
    # Unfortunately this doesn't return the labels which we need here! 
    summarise_with_llm(consultation, processing_run, llm_backend)
    
    
    # Merge similiar themes (Michael's code)
    

    data = get_scatter_plot_data(assignments)
    topic_model_metadata = models.TopicModelMetadata(scatter_plot_data=data)
    topic_model_metadata.save()

    for assignment in assignments:
        # This needs to be updated with the labels too 
        assignment.answer.save_theme_to_answer(
            topic_keywords=assignment.topic_keywords,
            topic_id=assignment.topic_id,
            processing_run=processing_run,
            topic_model_metadata=topic_model_metadata,
        )


def save_themes_for_processing_run(
    topic_backend: TopicBackend, processing_run: models.ProcessingRun, llm_backend
) -> None:
    consultation = processing_run.consultation
    logging.info(f"Starting topic modelling for consultation: {consultation.name}")
    questions = models.Question.objects.filter(
        section__consultation=consultation, has_free_text=True
    )

    for question in questions:
        save_themes_for_question(
            question, topic_backend=topic_backend, processing_run=processing_run, llm_backend
        )
