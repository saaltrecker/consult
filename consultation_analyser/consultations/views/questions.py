from typing import Dict, List, Optional, Tuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, QuerySet
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, render

from .. import models
from .consultations import NO_THEMES_YET_MESSAGE
from .decorators import user_can_see_consultation
from .filters import ThemeFilter, get_filter_params


def filter_scatter_plot_data(filtered_themes: QuerySet) -> List[Dict]:
    if not filtered_themes:
        return []
    theme = filtered_themes.first()  # metadata same for all themes for question
    topic_model_metadata = theme.topic_model_metadata
    data = topic_model_metadata.scatter_plot_data
    if not data:  # Old consultations - didn't calculate scatter data when generating themes
        return []
    data = data["data"]
    topic_ids = [theme.topic_id for theme in filtered_themes]
    filtered_scatter_data = [
        coordinate for coordinate in data if coordinate["topic_id"] in topic_ids
    ]
    return filtered_scatter_data


def get_outliers_info(processing_run: models.ProcessingRun, question: models.Question) -> Tuple:
    outlier_theme = None
    outliers_count = 0
    if not processing_run:
        return outlier_theme, outliers_count
    outlier_themes = processing_run.get_themes_for_question(question_id=question.id).filter(
        is_outlier=True
    )
    if outlier_themes:
        outlier_theme = outlier_themes.first()
        outliers_count = models.Answer.objects.filter(themes=outlier_theme).count()
    return outlier_theme, outliers_count


@user_can_see_consultation
@login_required
def show(
    request: HttpRequest,
    consultation_slug: str,
    section_slug: str,
    question_slug: str,
    processing_run_slug: Optional[str] = None,
):
    consultation = get_object_or_404(models.Consultation, slug=consultation_slug)
    try:
        processing_run = consultation.get_processing_run(processing_run_slug)
    except models.ProcessingRun.DoesNotExist:
        raise Http404

    question = models.Question.objects.get(
        slug=question_slug,
        section__slug=section_slug,
        section__consultation__slug=consultation_slug,
    )

    # this will never run bc processingrun has already 404'd
    if not processing_run:
        messages.info(request, NO_THEMES_YET_MESSAGE)

    # TODO - for now default to latest processing run
    filter_params = get_filter_params(request)

    theme_filter = ThemeFilter(id=filter_params.theme)
    themes = theme_filter.apply(processing_run.themes)
    answers = models.Answer.objects.filter(themes__in=themes)

    if themes:
        scatter_plot_data = filter_scatter_plot_data(themes)
    else:
        scatter_plot_data = []

    # Get counts
    total_responses = answers.count()
    multiple_choice_stats = question.multiple_choice_stats()
    highest_theme_count = themes.aggregate(Max("answer_count"))["answer_count__max"]

    blank_free_text_count = (
        models.Answer.objects.filter(question=question).filter(free_text="").count()
    )

    outlier_theme, outliers_count = get_outliers_info(
        processing_run=processing_run, question=question
    )

    context = {
        "consultation_slug": consultation_slug,
        "consultation_name": consultation.name,
        "question": question,
        "multiple_choice_stats": multiple_choice_stats,
        "responses": answers,
        "themes": themes,
        "highest_theme_count": highest_theme_count,
        "total_responses": total_responses,
        "applied_filters": filter_params,
        "blank_free_text_count": blank_free_text_count,
        "outliers_count": outliers_count,
        "outlier_theme_id": outlier_theme.id if outlier_theme else None,
        "scatter_plot_data": scatter_plot_data,
        "processing_run": processing_run,
    }
    return render(request, "consultations/questions/show.html", context)
