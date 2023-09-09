from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    edited_at = models.DateTimeField('editado em', auto_now=True)

    class Meta:
        abstract = True
