from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, render

from .. import models
from .consultations import NO_THEMES_YET_MESSAGE
from .decorators import user_can_see_consultation
from .filters import get_filter_params, ThemeFilter, AnswerFilter


@user_can_see_consultation
@login_required
def index(
    request: HttpRequest,
    consultation_slug: str,
    section_slug: str,
    question_slug: str,
    processing_run_slug: Optional[str] = None,
):
    consultation = get_object_or_404(models.Consultation, slug=consultation_slug)
    try:
        processing_run = consultation.get_processing_run(processing_run_slug=processing_run_slug)
    except models.ProcessingRun.DoesNotExist:
        return Http404

    question = models.Question.objects.get(
        slug=question_slug,
        section__slug=section_slug,
        section__consultation__slug=consultation_slug,
    )

    # this will never run
    if not consultation.has_processing_run():
        messages.info(request, NO_THEMES_YET_MESSAGE)

    total_answers = models.Answer.objects.filter(question=question).count()

    # TODO - for now, get themes from latest processing run
    filter_params = get_filter_params(request)

    # TODO: check will we crash if no themes
    theme_filter = ThemeFilter(id=filter_params.theme)
    themes = theme_filter.apply(processing_run.themes)

    answers = models.Answer.objects.filter(themes__in=themes)
    answer_filter = AnswerFilter(keyword=filter_params.keyword)
    answers = answer_filter.apply(answers)

    # pagination
    pagination = Paginator(answers, 5)
    page_index = request.GET.get("page", "1")
    current_page = pagination.page(page_index)
    paginated_responses = current_page.object_list

    context = {
        "consultation_name": consultation.name,
        "consultation_slug": consultation_slug,
        "processing_run": processing_run,
        "question": question,
        "responses": paginated_responses,
        "total_responses": total_answers,
        "applied_filters": filter_params,
        "themes": themes,
        "all_themes": processing_run.themes,
        "pagination": current_page,
    }

    return render(request, "consultations/responses/index.html", context)
