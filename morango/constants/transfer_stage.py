"""
This module contains constants representing the possible stages of a transfer session.
"""
from django.utils.translation import ugettext_lazy as _

SERIALIZING = "serializing"
QUEUING = "queuing"
DEQUEUING = "dequeuing"
DESERIALIZING = "deserializing"
PUSHING = "pushing"
PULLING = "pulling"

CHOICES = (
    (SERIALIZING, _("Serializing")),
    (QUEUING, _("Queuing")),
    (DEQUEUING, _("Dequeuing")),
    (DESERIALIZING, _("Deserializing")),
    (PUSHING, _("Pushing")),
    (PULLING, _("Pulling")),
)

PRECEDENCE = {
    SERIALIZING: 1,
    QUEUING: 2,
    PULLING: 3,
    PUSHING: 3,
    DEQUEUING: 4,
    DESERIALIZING: 5,
}


def precedence(stage_key):
    """
    :param stage_key: The stage constant
    """
    try:
        return PRECEDENCE[stage_key]
    except KeyError:
        return None


class stage(str):
    """
    Modeled after celery's status utilities
    """

    def __gt__(self, other):
        return precedence(self) < precedence(other)

    def __ge__(self, other):
        return precedence(self) <= precedence(other)

    def __lt__(self, other):
        return precedence(self) > precedence(other)

    def __le__(self, other):
        return precedence(self) >= precedence(other)
