from urllib.parse import urlencode
from dataclasses import dataclass
from typing import Optional

from django.db.models import Count
from django.http import HttpRequest


@dataclass
class FilterParams:
    theme: str
    keyword: str

    def as_querystring(self):
        qvs = {
            "theme": self.theme,
            "keyword": self.keyword,
        }

        return urlencode(qvs, doseq=True)


def get_filter_params(request: HttpRequest) -> FilterParams:
    return FilterParams(
        theme=request.GET.get("theme"),
        keyword=request.GET.get("keyword"),
    )


class ThemeFilter:
    def __init__(self, id: Optional[str] = None):
        self.id = id

    def apply(self, themeset):
        # TODO: move this unrelated code
        themeset = themeset.annotate(answer_count=Count("answer")).order_by("-answer_count")

        if self.id:
            themeset = themeset.filter(id=self.id)

        return themeset


class AnswerFilter:
    def __init__(self, keyword: Optional[str] = None):
        self.keyword = keyword

    def apply(self, answerset):
        if self.keyword:
            answerset = answerset.filter(free_text__contains=self.keyword)

        return answerset
