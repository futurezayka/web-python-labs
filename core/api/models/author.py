from django.db import models
from core.api.models.base import BaseModel


class Author(BaseModel):
    name = models.CharField(max_length=255)
    pseudonym = models.CharField(max_length=255, blank=True, null=True)
