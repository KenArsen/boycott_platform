import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreModel(models.Model):
    """
    Abstract base model with common fields for all models.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk}"
