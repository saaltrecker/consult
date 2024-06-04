# generated by datamodel-codegen:
#   filename:  public_schema.yaml
#   timestamp: 2024-06-04T16:10:44+00:00

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class MultipleChoiceItem(BaseModel):
    """
    A multiple choice question and its available (or selected, according to context) options
    """

    question_text: str
    options: List[str]


class MultipleChoice(RootModel[List[MultipleChoiceItem]]):
    """
    A list of multiple choice questions with arrays of options or arrays of answers
    """

    root: List[MultipleChoiceItem] = Field(
        ...,
        description="A list of multiple choice questions with arrays of options or arrays of answers",
    )


class Theme(BaseModel):
    """
    A theme, assigned by AI
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    id: UUID
    topic_id: int
    topic_keywords: List[str] = Field(..., description="The keywords in the theme")
    short_description: str = Field(
        ...,
        examples=[
            "Concern about the price of sugar",
            "Risk to wildlife habitats",
            "Overall quality of outdoor space in the area",
        ],
    )
    summary: str = Field(
        ...,
        description="A free-text summary of the theme",
        examples=[
            "Respondents identified potential impact on the price of sugar, noting that proposed new legislation was very likely to drive it higher",
            "Respondents flagged concerns around the conservation of habitats in the area and local biodiversity in general",
        ],
    )


class Question(BaseModel):
    """
    Questions can be free text, multiple choice or both. The presence of multiple_choice_options implies that the question has a multiple choice part.

    """

    model_config = ConfigDict(
        extra="forbid",
    )
    id: str = Field(
        ...,
        description="The number or other unique identifier for this question",
        examples=["1", "2", "3", "vii", "Question 1", "q1.2"],
    )
    text: str = Field(
        ...,
        description="The question text",
        examples=[
            "Should it happen on Tuesdays?",
            "Should it happen in the month of May?",
            "Should it happen on a full moon?",
            "Should it happen on Fridays?",
            "Should it be forbidden on Sunday?",
        ],
    )
    has_free_text: bool = Field(..., description="Does this question have a free text component?")
    multiple_choice: Optional[MultipleChoice] = None


class Answer(BaseModel):
    """
    Each Answer is associated with a Question and belongs to a ConsultationResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    question_id: str = Field(
        ...,
        description="The number or other unique identifier for the answered question",
        examples=["1", "2", "3", "vii", "Question 1", "q1.2"],
    )
    theme_id: Optional[UUID] = Field(
        None, description="The associated Theme, if any. Omit if uploading."
    )
    multiple_choice: Optional[MultipleChoice] = None
    free_text: Optional[str] = Field(
        None,
        description="The answer to the free text part of the question, if any",
        examples=[
            "I don't think this is a good idea at all",
            "I would like to point out a few things",
            "I would like clarification on a few key points",
        ],
    )


class ConsultationResponse(BaseModel):
    """
    A ConsultationResponse groups answers. For now it is also a placeholder for response-level information such as demographics, responding-in-the-capacity-of, etc.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    submitted_at: AwareDatetime = Field(
        ..., description="The submission date and time of the response"
    )
    answers: List[Answer] = Field(..., description="The answers in this response", min_length=1)


class Section(BaseModel):
    """
    A Section contains a group of Questions. Consultations that do not have multiple sections should group all Questions under a single Section.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(
        ...,
        description="The name of the section",
        examples=[
            "When to enforce a Kit Kat ban",
            "When to encourage the eating of Kit Kats",
            "When Kit Kats are consumed",
        ],
    )
    questions: List[Question] = Field(
        ..., description="The questions in the consultation", min_length=1
    )


class Consultation(BaseModel):
    """
    Consultation is the top-level object describing a consultation. It contains one or more Sections, which in turn contain Questions.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(
        ...,
        description="The name of the consultation",
        examples=[
            "Consultation on Kit Kats",
            "How should Kit Kats change",
            "What shall we do about Kit Kats",
        ],
    )
    sections: List[Section] = Field(
        ..., description="The sections of the consultation", min_length=1
    )


class ConsultationWithResponses(BaseModel):
    """
    A Consultation and its ConsultationResponses
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    consultation: Consultation = Field(..., description="The consultation")
    consultation_responses: List[ConsultationResponse] = Field(
        ..., description="The responses", min_length=1
    )


class ConsultationWithResponsesAndThemes(BaseModel):
    """
    A Consultation and its ConsultationResponses, plus Themes assigned by the tool
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    consultation: Consultation = Field(..., description="The consultation")
    consultation_responses: List[ConsultationResponse] = Field(
        ..., description="The responses", min_length=1
    )
    themes: List[Theme] = Field(..., description="The themes", min_length=1)
