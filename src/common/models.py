import datetime

from dirtyfields import DirtyFieldsMixin
from django.db import models


class BaseModel(DirtyFieldsMixin, models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID записи")

    created_at = models.DateTimeField("Время создания записи", db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField("Время изменения записи", db_index=True, auto_now=True)

    class Meta:
        abstract = True

    @property
    def dirty_fields(self) -> dict:
        return self.get_dirty_fields(check_relationship=True)


def tomorrow_date() -> datetime.datetime:
    return datetime.datetime.now() + datetime.timedelta(days=1)
