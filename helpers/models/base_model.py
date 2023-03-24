from datetime import datetime
from django.db import models
from model_fields import GG_ShortUUIDField
from django.contrib.auth import get_user_model
from django.conf import settings


class BaseModel(models.Model):
    idx = GG_ShortUUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="%(class)s_created_by"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        unique_together = ("is_deleted", "deleted_at")

    def save(self, *args, **kwargs):
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = datetime.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.is_active = False
        super().save(*args, **kwargs)

    @classmethod
    def default_system_user(cls):
        return get_user_model().objects.get(username=settings.DEFAULT_SYSTEM_USERNAME)
