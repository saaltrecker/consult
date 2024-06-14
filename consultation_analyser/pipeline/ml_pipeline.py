import logging
from uuid import UUID

from consultation_analyser.consultations import models

from .backends.topic_backend import TopicBackend

logger = logging.getLogger("pipeline")


