from django.db import models


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_deleted=False)


class QueryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
