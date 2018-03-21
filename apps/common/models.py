from django.db import models
from uuid import uuid4


class TimeStampedModel(models.Model):
    """Model that provides self-managed created and modified fields"""

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']


class UniquePrimaryKeyModel(models.Model):
    """Model that provides unique non-editable primary key"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UniquePrimaryKeyModel):
    """Template class with `all benefits` """

    class Meta:
        abstract = True
